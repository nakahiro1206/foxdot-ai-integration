"""Seed the Milvus CodeEntityRepository with existing scripts in data/."""

from pathlib import Path

from src.repository import CodeEntity, CodeEntityRepository


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def main() -> None:
    repo = CodeEntityRepository()

    py_files = sorted(DATA_DIR.glob("*.py"))
    if not py_files:
        print("No .py files found in data/")
        return

    entities = [
        CodeEntity(
            name=f.stem,
            language="foxdot",
            code_content=f.read_text(),
            intent_description=f"FoxDot music composition script: {f.stem}",
        )
        for f in py_files
    ]

    result = repo.insert_batch(entities)
    print(f"Inserted {len(entities)} scripts: {result}")
    repo.close()


if __name__ == "__main__":
    main()
