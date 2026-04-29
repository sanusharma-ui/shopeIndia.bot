from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: str | None = None


class ProductCard(BaseModel):
    id: str
    name: str
    category: str
    price: int
    old_price: int | None = None
    discount: str | None = None
    rating: float | None = None
    description: str
    keywords: list[str] = []
    product_url: str | None = None
    image_url: str | None = None


class ChatResponse(BaseModel):
    reply: str
    products: list[ProductCard] = []