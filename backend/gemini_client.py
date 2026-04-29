import asyncio
from google import genai
from google.genai import types

from config import settings
from prompts import SYSTEM_PROMPT


if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Please add it in .env file.")


client = genai.Client(api_key=settings.GEMINI_API_KEY)

gemini_semaphore = asyncio.Semaphore(settings.MAX_GEMINI_CONCURRENT_REQUESTS)


async def ask_gemini(user_message: str, product_context: str) -> str:
    prompt = f"""
User message:
{user_message}

Relevant ShopeIndia product context:
{product_context}

Answer as ShopeIndia Assistant.
"""

    async with gemini_semaphore:
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.35,
                max_output_tokens=500,
            ),
        )

    return response.text or "Sorry, I could not generate a proper response. Please try again."