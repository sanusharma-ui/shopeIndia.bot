from groq import AsyncGroq
from config import settings

groq_client = None

if settings.GROQ_API_KEY:
    groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def ask_groq(user_message: str, product_context: str) -> str:
    if not groq_client:
        raise RuntimeError("Groq client not available")

    prompt = f"""
User message:
{user_message}

Relevant ShopeIndia product context:
{product_context}

Answer as ShopeIndia Assistant.
"""

    last_error = None

    # 🔁 Loop through models
    for model in settings.GROQ_MODEL_PRIORITY:
        try:
            print(f"Trying Groq model: {model}")

            response = await groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are ShopeIndia assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Model failed: {model} → {str(e)}")
            last_error = e
            continue

    # ❌ All models failed
    raise RuntimeError(f"All Groq models failed: {str(last_error)}")