import re
from product_data import PRODUCTS


CATEGORY_SYNONYMS = {
    "hijama": ["hijama", "cupping", "cup", "vacuum", "suction"],
    "derma": ["derma", "dermapen", "microneedling", "roller", "zgts", "skin"],
    "massage": ["massage", "massager", "body", "foot", "knee", "gun"],
    "gloves": ["glove", "gloves", "nitrile", "latex", "surgical"],
    "infrared": ["infrared", "infra red", "lamp", "tera", "heat"],
    "serum": ["serum", "retinol", "vitamin", "hyaluronic", "facial"],
    "bed": ["bed", "chair", "portable", "fold"],
    "fitness": ["fitness", "foam", "roller", "exercise", "workout"],
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9₹ ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_budget(query: str) -> int | None:
    query = query.lower()

    patterns = [
        r"under\s*(\d+)",
        r"below\s*(\d+)",
        r"budget\s*(\d+)",
        r"(\d+)\s*ke\s*andar",
        r"(\d+)\s*tak",
        r"₹\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return int(match.group(1))

    return None


def expand_query_words(query: str) -> set[str]:
    normalized = normalize_text(query)
    words = set(normalized.split())

    for key, synonyms in CATEGORY_SYNONYMS.items():
        if key in words:
            words.update(synonyms)

    return words


def product_search_text(product: dict) -> str:
    return normalize_text(
        " ".join(
            [
                product.get("name", ""),
                product.get("category", ""),
                product.get("description", ""),
                " ".join(product.get("keywords", [])),
            ]
        )
    )


def search_products(query: str, limit: int = 6) -> list[dict]:
    query = query.strip()

    if not query:
        return []

    query_normalized = normalize_text(query)
    query_words = expand_query_words(query)
    budget = extract_budget(query)

    scored_products = []

    for product in PRODUCTS:
        text = product_search_text(product)
        score = 0

        if query_normalized and query_normalized in text:
            score += 10

        for word in query_words:
            if len(word) <= 2:
                continue

            if word in text:
                score += 2

            if word in normalize_text(product.get("name", "")):
                score += 3

            if word in normalize_text(product.get("category", "")):
                score += 2

            if word in product.get("keywords", []):
                score += 3

        product_price = product.get("price")

        if budget and product_price:
            if product_price <= budget:
                score += 6
            else:
                score -= 5

        if score > 0:
            scored_products.append((score, product))

    scored_products.sort(
        key=lambda item: (
            item[0],
            item[1].get("rating") or 0,
            -(item[1].get("price") or 0),
        ),
        reverse=True,
    )

    return [product for _, product in scored_products[:limit]]


def format_products_for_prompt(products: list[dict]) -> str:
    if not products:
        return "No matching products found in local product data."

    lines = []

    for index, product in enumerate(products, start=1):
        old_price = product.get("old_price")
        old_price_text = f"₹{old_price}" if old_price else "Not available"

        lines.append(
            f"""
{index}. {product.get("name")}
Category: {product.get("category")}
Price: ₹{product.get("price")}
Old Price: {old_price_text}
Discount: {product.get("discount")}
Rating: {product.get("rating")}
Description: {product.get("description")}
Product URL: {product.get("product_url")}
"""
        )

    return "\n".join(lines)