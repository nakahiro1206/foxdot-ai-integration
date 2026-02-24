from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)

# 1. Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# 2. Define Schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(
        name="description_vector", dtype=DataType.FLOAT_VECTOR, dim=768
    ),  # Semantic Intent
    FieldSchema(
        name="code_content", dtype=DataType.VARCHAR, max_length=5000
    ),  # The actual 100-line code
    FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=50),  # Filter tag
    FieldSchema(
        name="entity_name", dtype=DataType.VARCHAR, max_length=200
    ),  # Function/Class name
]

schema = CollectionSchema(fields, "Code Entity Store for AI Generation")
collection_name = "code_entities"

if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)

code_collection = Collection(collection_name, schema)

# 3. Create Index (IVF_FLAT for balanced speed/accuracy)
index_params = {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}}
code_collection.create_index(field_name="description_vector", index_params=index_params)


# 4. Storage Function (How to store for better retrieval)
def insert_code_entity(vector, code, lang, name):
    """
    Storing the vector of the NATURAL LANGUAGE description
    allows the AI to find 'How to delete users' even if the
    code doesn't contain those exact words.
    """
    data = [
        [vector],  # description_vector
        [code],  # code_content
        [lang],  # language
        [name],  # entity_name
    ]
    code_collection.insert(data)
    code_collection.flush()


print(f"Collection {collection_name} is ready for AI-powered retrieval.")
