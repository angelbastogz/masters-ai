from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from support import analysis
from support.analysis import ProductAnalysis, ProductComparison
from support.data import DATA_DIR, count_reviews, load
from support.encoder import build_product_vectors, load_model
from support.search import SearchResult, search
from support.settings import CONFIG_PATH, load_config

mcp = MCPServer("Amazon reviews")

settings = load_config(CONFIG_PATH)
model = load_model(settings)
records, products = load(DATA_DIR)
product_vectors_for_search, product_ids = build_product_vectors(
    records, products, model=model, batch_size=settings.batch_size
)
review_counts_for_search = count_reviews(records)


@mcp.tool()
def search_products(query: str, top_k: int = 5) -> list[SearchResult]:
    """Search products by similarity to a query.

    Search products by similarity between the given query and a vector that is built using 50% catalog and 50%
    reviews, top_k parameter limits the number of products returned.

    Args:
        query (str): query to search products, it cannot be empty. For better results, use English.
        top_k (int, optional): number, between 1 and 20, of products to return. Defaults to 5.

    Returns:
        list[SearchResult]: list of products (product_id, title, similarity, review_count) found ordered by similarity.
        Similarity doesn't mean quality.
    """
    try:
        return search(
            query,
            top_k,
            model,
            product_vectors_for_search,
            product_ids,
            products,
            review_counts_for_search,
        )
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def analyze_product(product_id: str) -> ProductAnalysis:
    """Analyze a product.

    Retrieve product analysis for a given product ID. It only uses the existing reviews in the current dataset.

    Args:
        product_id (str): product ID to analyze, it cannot be empty.
            If it doesn't exist, response will be returned with zeros and None values.

    Returns:
        ProductAnalysis: product analysis of the given product. It includes:
            product_id (str): product ID
            review_count (int): total number of reviews
            rating_counts (dict): rating counts for each star, from 1 to 5.
            rating_proportions (dict): rating proportions (0 to 1) for each star, from 1 to 5.
            mean (float | None): mean of total ratings
            median (float | None): median of total ratings
    """
    try:
        return analysis.analyze_product(product_id, records)
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def compare_products(product_ids: list[str]) -> ProductComparison:
    """Compare a list of product IDs.

    Analyze each product and compare its mean rating with the first product's mean.

    Args:
        product_ids (list[str]): list of product IDs. It cannot be empty, it requires at least 2 product IDs, product IDs cannot be empty.
            It doesn't allow duplicates. If a given product ID doesn't exist, response will be returned with zeros and None values.

    Returns:
        ProductComparison: comparison between product IDs. It includes the product analysis for each of the given products and the
            mean difference for the products.
            product_summaries:
                product_id (str): product ID
                review_count (int): total number of reviews
                rating_counts (dict): rating counts for each star, from 1 to 5.
                rating_proportions (dict): rating proportions (0 to 1) for each star, from 1 to 5.
                mean (float | None): mean of total ratings
                median (float | None): median of total ratings
            mean_differences: dictionary with product ID as key and mean difference as value, mean difference is the
                mean of the product minus the mean of the first given product. The first product's difference is always 0.0.
                It will be None if any of the two products compared doesn't have reviews.
    """
    try:
        return analysis.compare_products(product_ids, records)
    except ValueError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
