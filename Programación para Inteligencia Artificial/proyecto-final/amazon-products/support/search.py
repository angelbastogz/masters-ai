from typing import TypedDict

import torch
from sentence_transformers import SentenceTransformer

from support.data import DATA_DIR, ProductRecord, count_reviews, load
from support.encoder import build_product_vectors, encode_query, load_model
from support.settings import CONFIG_PATH, load_config


class SearchResult(TypedDict):
    product_id: str
    title: str
    similarity: float
    review_count: int


def validate_search(query: str, top_k: int) -> None:
    if not query.strip():
        raise ValueError('Query cannot be empty')

    if not 1 <= top_k <= 20:
        raise ValueError('Top k must be between 1 and 20')


def search(query: str, top_k: int, model: SentenceTransformer, product_vectors: torch.Tensor,
           product_ids: list[str], products: dict[str, ProductRecord], review_counts: dict[str, int]
           ) -> list[SearchResult]:
    validate_search(query, top_k)

    top_k_limited = min(top_k, len(product_ids))

    encoded_query = encode_query(query, model)
    scores = product_vectors @ encoded_query
    topk = torch.topk(scores, k=top_k_limited)

    topk_indices: list[int] = topk.indices.tolist()
    topk_values: list[float] = topk.values.tolist()

    result: list[SearchResult] = []

    for indice, value in zip(topk_indices, topk_values):
        product_id = product_ids[indice]
        result.append(
            SearchResult(
                product_id=product_id,
                title=products[product_id]["title"],
                similarity=value,
                review_count=review_counts[product_id],
            )
        )

    return result


if __name__ == '__main__':
    # validate_search('', 1)
    # validate_search('Product', 21)
    settings = load_config(CONFIG_PATH)
    model_search = load_model(settings)
    records, products = load(DATA_DIR)
    product_vectors_for_search, product_ids = build_product_vectors(records, products, model=model_search,
                                                                    batch_size=settings.batch_size)

    review_counts_for_search = count_reviews(records)
    result = search('A portable waterproof Bluetooth speaker', 3, model_search, product_vectors_for_search, product_ids,
                    products, review_counts_for_search)
    print(result)
