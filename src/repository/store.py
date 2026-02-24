from pymilvus import MilvusClient, DataType
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from src.env import env
from .models import CodeEntity, CodeEntitySearchResult, CodeEntitySummary

COLLECTION_NAME = "code_entities"
EMBEDDING_DIM = 1536

uri = Path(__file__).parents[2] / "milvus.db"


class CodeEntityRepository:
    """Milvus-backed repository for semantic code retrieval."""

    def __init__(self, uri: str):
        self.client = MilvusClient(uri=uri)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=lambda: env.OPENAI_API_KEY,
        )
        self._ensure_collection()

    # ── Schema ────────────────────────────────────────────────────────

    def _ensure_collection(self) -> None:
        if self.client.has_collection(COLLECTION_NAME):
            return

        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=False)
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("description_vector", DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
        schema.add_field("code_content", DataType.VARCHAR, max_length=10000)
        schema.add_field("language", DataType.VARCHAR, max_length=50)
        schema.add_field("entity_name", DataType.VARCHAR, max_length=200)
        schema.add_field("intent_description", DataType.VARCHAR, max_length=2000)

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="description_vector",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"nlist": 128},
        )

        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params,
        )

    # ── Insert ────────────────────────────────────────────────────────

    def insert(self, entity: CodeEntity) -> dict:
        vector = self.embeddings.embed_query(entity.intent_description)
        data = {
            "description_vector": vector,
            "code_content": entity.code_content,
            "language": entity.language,
            "entity_name": entity.name,
            "intent_description": entity.intent_description,
        }
        return self.client.insert(collection_name=COLLECTION_NAME, data=[data])

    def insert_batch(self, entities: list[CodeEntity]) -> dict:
        texts = [e.intent_description for e in entities]
        vectors = self.embeddings.embed_documents(texts)
        data = [
            {
                "description_vector": vec,
                "code_content": e.code_content,
                "language": e.language,
                "entity_name": e.name,
                "intent_description": e.intent_description,
            }
            for vec, e in zip(vectors, entities)
        ]
        return self.client.insert(collection_name=COLLECTION_NAME, data=data)

    # ── Search ────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        top_k: int = 5,
        language_filter: str | None = None,
    ) -> list[CodeEntitySearchResult]:
        """Semantic search by natural language intent."""
        query_vec = self.embeddings.embed_query(query)

        filter_expr = ""
        if language_filter:
            filter_expr = f'language == "{language_filter}"'

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            data=[query_vec],
            limit=top_k,
            output_fields=[
                "entity_name",
                "code_content",
                "language",
                "intent_description",
            ],
            search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
            filter=filter_expr,
        )
        return [CodeEntitySearchResult.from_hit(hit) for hit in results[0]]

    # ── Query / Delete ────────────────────────────────────────────────

    def get_by_name(self, name: str) -> list[CodeEntity]:
        rows = self.client.query(
            collection_name=COLLECTION_NAME,
            filter=f'entity_name == "{name}"',
            output_fields=[
                "entity_name",
                "code_content",
                "language",
                "intent_description",
            ],
        )
        return [
            CodeEntity(
                name=r["entity_name"],
                language=r["language"],
                code_content=r["code_content"],
                intent_description=r["intent_description"],
            )
            for r in rows
        ]

    def list_all(self) -> list[CodeEntitySummary]:
        rows = self.client.query(
            collection_name=COLLECTION_NAME,
            filter="id >= 0",
            output_fields=["entity_name", "language", "intent_description"],
        )
        return [CodeEntitySummary.from_row(r) for r in rows]

    def delete(self, entity_ids: list[int]) -> dict:
        return self.client.delete(
            collection_name=COLLECTION_NAME,
            ids=entity_ids,
        )

    def drop_collection(self) -> None:
        self.client.drop_collection(COLLECTION_NAME)

    def close(self) -> None:
        self.client.close()


if __name__ == "__main__":
    from pydantic import ValidationError

    print(uri.name)
    repo = CodeEntityRepository(uri=str(uri))

    # ── Test 1: Pydantic validation on insert ──
    print("=== Test 1: Valid CodeEntity ===")
    entity = CodeEntity(
        name="test_synth",
        language="python",
        code_content="print('hello')",
        intent_description="A simple test synth snippet",
    )
    print(f"  Created: {entity.model_dump()}")

    print("\n=== Test 2: Invalid CodeEntity (missing field) ===")
    try:
        bad = CodeEntity(name="bad", language="python")  # type: ignore
    except ValidationError as e:
        print(f"  Caught ValidationError: {e.error_count()} error(s)")
        for err in e.errors():
            print(f"    - {err['loc']}: {err['msg']}")

    # ── Test 3: Insert & retrieve ──
    print("\n=== Test 3: Insert & get_by_name ===")
    repo.insert(entity)
    results = repo.get_by_name("test_synth")
    for r in results:
        print(f"  type={type(r).__name__}, name={r.name}, lang={r.language}")

    # ── Test 4: list_all returns CodeEntitySummary ──
    print("\n=== Test 4: list_all returns CodeEntitySummary ===")
    summaries = repo.list_all()
    for s in summaries:
        print(f"  type={type(s).__name__}, id={s.id}, name={s.name}")

    # ── Test 5: search returns CodeEntitySearchResult ──
    print("\n=== Test 5: search returns CodeEntitySearchResult ===")
    hits = repo.search("test synth", top_k=3)
    for h in hits:
        print(
            f"  type={type(h).__name__}, id={h.id}, "
            f"distance={h.distance:.4f}, entity_name={h.entity.name}"
        )

    # ── Cleanup ──
    print("\n=== Cleanup ===")
    repo.drop_collection()
    print("  Collection dropped.")
    repo.close()
