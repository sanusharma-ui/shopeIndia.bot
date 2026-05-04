import hashlib
import json
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from cache import response_cache
from config import settings
from gemini_client import ask_gemini
from groq_client import ask_groq
from product_data import PRODUCTS
from product_search import search_products, format_products_for_prompt
from rate_limiter import check_rate_limit
from schemas import ChatRequest, ChatResponse, ProductCard


START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("ShopeIndia AI Chatbot backend started")
    print(f"Loaded products: {len(PRODUCTS)}")
    yield
    print("ShopeIndia AI Chatbot backend stopped")


app = FastAPI(
    title="ShopeIndia AI Chatbot",
    version="2.1.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def make_cache_key(message: str) -> str:
    normalized = message.lower().strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "ShopeIndia AI Chatbot backend is running",
        "total_products": len(PRODUCTS),
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Backend is alive",
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }


@app.get("/products")
def get_products(category: str | None = None, q: str | None = None):
    if q:
        searched_products = search_products(q, limit=20)
        return {
            "count": len(searched_products),
            "products": searched_products
        }

    if category:
        filtered = [
            product for product in PRODUCTS
            if product["category"].lower() == category.lower()
        ]
        return {
            "count": len(filtered),
            "products": filtered
        }

    return {
        "count": len(PRODUCTS),
        "products": PRODUCTS
    }


@app.get("/categories")
def get_categories():
    categories = sorted(set(product["category"] for product in PRODUCTS))

    return {
        "count": len(categories),
        "categories": categories
    }


async def generate_ai_reply(user_message: str, product_context: str) -> str:
    """
    First try Gemini.
    If Gemini fails/quota ends, try Groq.
    If Groq also fails or key is missing, raise error to main chat handler.
    """

    try:
        print("Trying Gemini...")
        reply = await ask_gemini(
            user_message=user_message,
            product_context=product_context
        )

        if reply and reply.strip():
            return reply

        raise RuntimeError("Gemini returned empty response")

    except Exception as gemini_error:
        print("Gemini error:", str(gemini_error))

        try:
            print("Trying Groq fallback...")
            reply = await ask_groq(
                user_message=user_message,
                product_context=product_context
            )

            if reply and reply.strip():
                return reply

            raise RuntimeError("Groq returned empty response")

        except Exception as groq_error:
            print("Groq error:", str(groq_error))
            raise RuntimeError("All AI providers failed")


@app.post("/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest, request: Request):
    check_rate_limit(request)

    user_message = request_data.message.strip()

    if not user_message:
        return ChatResponse(reply="Please type your question 🙂", products=[])

    cache_key = make_cache_key(user_message)
    cached_response = response_cache.get(cache_key)

    if cached_response:
        return ChatResponse(**cached_response)

    matched_products = search_products(user_message, limit=6)
    product_context = format_products_for_prompt(matched_products)

    try:
        reply = await generate_ai_reply(
            user_message=user_message,
            product_context=product_context
        )

    except Exception as error:
        print("AI fallback error:", str(error))

        if matched_products:
            reply = (
                "AI response abhi available nahi hai 😅\n\n"
                "But maine kuch relevant products dhundh liye hain 👇"
            )
        else:
            reply = (
                "Sorry, abhi AI service temporarily available nahi hai.\n"
                "Please ShopeIndia support se contact karein: +91 7385743121"
            )

    product_cards = [ProductCard(**product) for product in matched_products]

    response_payload = {
        "reply": reply,
        "products": [
            json.loads(card.model_dump_json())
            for card in product_cards
        ]
    }

    response_cache.set(cache_key, response_payload)

    return ChatResponse(**response_payload)