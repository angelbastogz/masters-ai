from typing import TypedDict

import numpy as np

from support.data import DATA_DIR, ReviewRecord, load


class ProductAnalysis(TypedDict):
    product_id: str
    review_count: int
    rating_counts: dict[int, int]
    rating_proportions: dict[int, float]
    mean: float | None
    median: float | None


class ProductComparison(TypedDict):
    product_summaries: list[ProductAnalysis]
    mean_differences: dict[str, float | None]


def validate_analysis(product_id: str) -> None:
    if not product_id.strip():
        raise ValueError('product_id cannot be empty')


def analyze_product(product_id: str, records: list[ReviewRecord]) -> ProductAnalysis:
    validate_analysis(product_id)

    ratings = [record["rating"] for record in records if record["product_id"] == product_id]
    rating_counts: dict[int, int] = {star: 0 for star in range(1, 6)}
    rating_proportions: dict[int, float] = {star: 0.0 for star in range(1, 6)}

    if not ratings:
        return ProductAnalysis(
            product_id=product_id,
            review_count=0,
            rating_counts=rating_counts,
            rating_proportions=rating_proportions,
            mean=None,
            median=None
        )

    review_count = len(ratings)
    np_ratings = np.array(ratings)

    rating_counts = {key: int((np_ratings == key).sum()) for key in rating_counts}
    rating_proportions = {key: float(rating_counts[key] / review_count) for key in rating_counts}

    return ProductAnalysis(
        product_id=product_id,
        review_count=review_count,
        rating_counts=rating_counts,
        rating_proportions=rating_proportions,
        mean=float(np.mean(np_ratings)),
        median=float(np.median(np_ratings)),
    )


def validate_comparison(product_ids: list[str]) -> None:
    if not product_ids:
        raise ValueError('product_ids cannot be empty')

    if len(product_ids) < 2:
        raise ValueError('product_ids require at least 2 product ids')

    if len(set(product_ids)) != len(product_ids):
        raise ValueError('product_ids must all be unique')

    for product_id_comparison in product_ids:
        validate_analysis(product_id_comparison)


def compare_products(product_ids: list[str], review_records: list[ReviewRecord]) -> ProductComparison:
    validate_comparison(product_ids)

    analysis_products = [analyze_product(product_id, review_records) for product_id in product_ids]

    first_product_mean = analysis_products[0]["mean"]

    if first_product_mean is None:
        return ProductComparison(
            product_summaries=analysis_products,
            mean_differences={product["product_id"]: None for product in analysis_products},
        )

    return ProductComparison(
        product_summaries=analysis_products,
        mean_differences={
            product["product_id"]: None if product["mean"] is None else (product["mean"] - first_product_mean) for
            product in analysis_products},
    )


if __name__ == '__main__':
    records, products = load(DATA_DIR)

    prod_id = "B0BCTJMN63"
    result = analyze_product(prod_id, records)

    prod_ids = [prod_id, "B0B786PFYJ"]
    comparison = compare_products(prod_ids, records)
    print(comparison)
