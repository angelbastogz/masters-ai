from typing import Any

from mcp import Client


async def demonstrate() -> None:
    calls: list[tuple[str, dict[str, Any]]] = [
        (
            "search_products",
            {"query": "A portable waterproof Bluetooth speaker", "top_k": 3},
        ),
        ("analyze_product", {"product_id": "B0BCTJMN63"}),
        ("compare_products", {"product_ids": ["B0BCTJMN63", "B09MMWM2Y8"]}),
        ("analyze_product", {"product_id": "UNKNOWN_PRODUCT"}),
        ("search_products", {"query": "delivery", "top_k": 0}),
        (
            "search_products",
            {"query": "Comfortable headphones with good sound", "top_k": 2},
        ),
        # (
        #     "search_products",
        #     {"query": "4K HDMI cable for gaming console", "top_k": 3},
        # ),
        # (
        #     "compare_products",
        #     {"product_ids": ["B09YJXSPPW", "B08CZ4KZHN", "B06ZZD1WGJ"]},
        # ),
        # (
        #     "search_products",
        #     {"query": "Fitness tracker with long battery life", "top_k": 3},
        # ),
        # (
        #     "compare_products",
        #     {"product_ids": ["B08L4V3PNJ", "B0BTV39NV3", "B0BJW6R4YX"]},
        # ),
    ]
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print("Tools:", [tool.name for tool in tools.tools])
        for name, arguments in calls:
            print(f"\n{name}: {arguments}")
            result = await client.call_tool(name, arguments)
            print("Tool error:", result.is_error)
            print(result.model_dump_json(indent=2))
