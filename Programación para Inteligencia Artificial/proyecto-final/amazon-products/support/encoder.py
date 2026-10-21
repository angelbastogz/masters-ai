import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

from support.data import (
    DATA_DIR,
    ProductRecord,
    ReviewRecord,
    catalog_text,
    load,
    review_texts,
)
from support.settings import CONFIG_PATH, Settings, load_config


def load_model(settings: Settings) -> SentenceTransformer:
    return SentenceTransformer(settings.model_name, device=settings.device)


def encode(
    texts: list[str], model: SentenceTransformer, batch_size: int
) -> torch.Tensor:
    return model.encode(
        texts,
        batch_size=batch_size,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )


def encode_query(query: str, model: SentenceTransformer) -> torch.Tensor:
    return encode([query], model, batch_size=1)[0]


def build_product_vectors(
    review_records: list[ReviewRecord],
    product_records: dict[str, ProductRecord],
    model: SentenceTransformer,
    batch_size: int,
) -> tuple[torch.Tensor, list[str]]:
    product_ids = list(product_records.keys())
    catalog_texts = [
        catalog_text(product_records[product_id]) for product_id in product_ids
    ]
    catalog_vectors = encode(catalog_texts, model=model, batch_size=batch_size)

    texts, _, review_product_ids = review_texts(review_records)
    review_vectors = encode(texts, model=model, batch_size=batch_size)
    review_summaries: list[torch.Tensor] = []

    for product_id in product_ids:
        positions = [
            index
            for index, review_product_id in enumerate(review_product_ids)
            if product_id == review_product_id
        ]
        rows = review_vectors[positions]
        average = rows.mean(dim=0)
        summary = F.normalize(average, dim=0)
        review_summaries.append(summary)

    review_matrix = torch.stack(review_summaries)
    product_vectors = F.normalize(0.5 * catalog_vectors + 0.5 * review_matrix, dim=1)
    return (product_vectors, product_ids)


if __name__ == "__main__":
    settings = load_config(CONFIG_PATH)

    model_encoder = load_model(settings)

    example_texts = [
        "The package arrived two weeks late.",
        "The headphones feel comfortable.",
        "Customer support answered my question quickly.",
    ]
    # review_vectors = encode(example_texts, model=model, batch_size=settings.batch_size)
    # print("Shape:", review_vectors.shape)

    records, products = load(DATA_DIR)
    product_vectors, product_ids = build_product_vectors(
        records, products, model=model_encoder, batch_size=settings.batch_size
    )

    print("Product vectors shape: ", product_vectors.shape)
    print("Product ids len: ", len(product_ids))
    print("First product id: ", product_ids[0])

    encoded_query = encode_query(
        "A portable waterproof Bluetooth speaker", model=model_encoder
    )
    print("Query shape: ", encoded_query.shape)
