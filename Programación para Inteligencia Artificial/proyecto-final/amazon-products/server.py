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
product_vectors_for_search, product_ids = build_product_vectors(records, products, model=model,
                                                                batch_size=settings.batch_size)
review_counts_for_search = count_reviews(records)


# Register your tools here with @mcp.tool().

@mcp.tool()
def search_products(query: str, top_k: int = 5) -> list[SearchResult]:
    try:
        return search(query, top_k, model, product_vectors_for_search, product_ids,
                      products, review_counts_for_search)
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def analyze_product(product_id: str) -> ProductAnalysis:
    try:
        return analysis.analyze_product(product_id, records)
    except ValueError as error:
        raise ToolError(str(error)) from error


@mcp.tool()
def compare_products(product_ids: list[str]) -> ProductComparison:
    try:
        return analysis.compare_products(product_ids, records)
    except ValueError as error:
        raise ToolError(str(error)) from error


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
