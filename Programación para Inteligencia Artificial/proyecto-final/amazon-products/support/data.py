from pathlib import Path

def ensure_data(directory: Path) -> None:
    for filename in ("reviews.jsonl.gz", "products.jsonl.gz"):
        if not (directory / filename).is_file():
            raise FileNotFoundError(f"Copy the provided datasets folder first: {filename}")


if __name__ == "__main__":
    DATA_DIR = Path("../datasets")

    ensure_data(DATA_DIR)

