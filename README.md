# ShopeIndia AI Chatbot

A custom AI chatbot built for **ShopeIndia.co.in**, an e-commerce website focused on therapy, wellness, beauty, hijama, cupping therapy, massage tools, derma aesthetic products, physiotherapy equipment, surgical items, and related products.

The chatbot helps customers find products, ask basic product-related questions, view product suggestions, and get support guidance.

---

## Project Overview

This project contains:

* **FastAPI backend**
* **Gemini API integration**
* **Product search system**
* **React chatbot widget**
* **Product card responses**
* **Rate limiting**
* **Caching**
* **CORS protection**
* **Clean customer-facing UI**

The frontend chatbot widget can be integrated into the ShopeIndia website, while the backend is hosted separately and handles AI responses securely.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Google Gemini API
* Pydantic
* Python Dotenv

### Frontend

* React
* Vite
* CSS

---

## How It Works

```txt
ShopeIndia Website
        ↓
React Chatbot Widget
        ↓
FastAPI Backend
        ↓
Product Search + Gemini API
        ↓
AI Response + Product Suggestions
        ↓
Chatbot UI
```

The Gemini API key stays only on the backend server.
It is never exposed in frontend code.

---

## Features

* AI-powered product assistant
* Product recommendations from local product data
* Product cards with price, discount, rating, and product link
* English by default
* Can reply in Hindi, Hinglish, Marathi, or another language if the user uses that language
* Basic e-commerce support guidance
* Contact support guidance
* Rate limiting to reduce abuse
* Response caching for repeated questions
* CORS support for production domain
* Clean floating chatbot UI
* Mobile responsive design

---

## Project Structure

```txt
shopeindia-chatbot/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── gemini_client.py
│   ├── product_data.py
│   ├── product_search.py
│   ├── prompts.py
│   ├── cache.py
│   ├── rate_limiter.py
│   └── schemas.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatWidget.jsx
│   │       └── ChatWidget.css
│   │
│   ├── .env
│   └── package.json
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Backend Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

#### Windows

```bash
.\venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Backend Environment Variables

Create a `.env` file in the project root or backend environment.

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://shopeindia.co.in,https://www.shopeindia.co.in

MAX_GEMINI_CONCURRENT_REQUESTS=20
CACHE_TTL_SECONDS=300
RATE_LIMIT_PER_MINUTE=20
```

---

## Important Security Note

Do not expose the Gemini API key in frontend code.

The API key must only be stored in:

```txt
Render Environment Variables
or
Backend .env file
```

Never put the API key inside:

```txt
React code
JavaScript files
GitHub public repo
Frontend .env deployed publicly
```

---

## Run Backend Locally

Go to the backend folder:

```bash
cd backend
```

Run the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Backend will run at:

```txt
http://127.0.0.1:8000
```

API docs:

```txt
http://127.0.0.1:8000/docs
```

---

## Backend API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "ok",
  "message": "ShopeIndia AI Chatbot backend is running",
  "total_products": 50,
  "uptime_seconds": 100.2
}
```

---

### Chat API

```http
POST /chat
```

Request body:

```json
{
  "message": "Suggest a hijama suction gun under 300"
}
```

Response:

```json
{
  "reply": "Here are some suitable Hijama suction gun options...",
  "products": [
    {
      "id": "hijama-vacuum-gun-premium-abs",
      "name": "Hijama Vacuum Gun | Premium ABS Imported Suction Gun",
      "category": "Hijama Suction Gun",
      "price": 269,
      "old_price": 349,
      "discount": "25% off",
      "rating": 3.0,
      "description": "Hijama vacuum gun for cupping therapy.",
      "keywords": ["hijama", "vacuum gun", "suction gun"],
      "product_url": "/product/hijama-vacuum-gun-premium-abs",
      "image_url": ""
    }
  ]
}
```

---

### Products API

```http
GET /products
```

Get all products.

```http
GET /products?q=derma
```

Search products.

```http
GET /products?category=Hijama Suction Gun
```

Filter by category.

---

### Categories API

```http
GET /categories
```

Returns all available product categories.

---

## Frontend Setup

Go to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend will run at:

```txt
http://localhost:5173
```

---

## Frontend Environment Variable

Create `frontend/.env`:

```env
VITE_CHATBOT_API_URL=http://127.0.0.1:8000/chat
```

For production, replace with hosted backend URL:

```env
VITE_CHATBOT_API_URL=https://your-render-backend-url.onrender.com/chat
```

---

## React Integration Guide

If the main website is built with React, copy these two files:

```txt
ChatWidget.jsx
ChatWidget.css
```

Place them inside:

```txt
src/components/
```

Then import the chatbot:

```jsx
import ChatWidget from "./components/ChatWidget";
```

Use it inside the main layout or App component:

```jsx
function App() {
  return (
    <>
      {/* Existing website content */}
      <ChatWidget />
    </>
  );
}

export default App;
```

The chatbot will appear as a floating button at the bottom-right of the website.

---

## Production Backend URL

In `ChatWidget.jsx`, the API URL is loaded from environment variable:

```js
const API_URL =
  import.meta.env.VITE_CHATBOT_API_URL || "http://127.0.0.1:8000/chat";
```

For production, set:

```env
VITE_CHATBOT_API_URL=https://your-render-backend-url.onrender.com/chat
```

Do not use this in production:

```txt
http://127.0.0.1:8000/chat
```

That only works on the local machine.

---

## Deployment on Render

### Backend Deployment

1. Push backend code to GitHub.
2. Create a new Render Web Service.
3. Connect the GitHub repository.
4. Select Python environment.
5. Add environment variables in Render dashboard.
6. Use the following build command:

```bash
pip install -r requirements.txt
```

7. Use the following start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

If the backend files are inside the `backend/` folder, use:

```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

Or configure Render root directory as:

```txt
backend
```

Then use:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Render Environment Variables

Add these in Render:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
ALLOWED_ORIGINS=https://shopeindia.co.in,https://www.shopeindia.co.in
MAX_GEMINI_CONCURRENT_REQUESTS=20
CACHE_TTL_SECONDS=300
RATE_LIMIT_PER_MINUTE=20
```

For testing, localhost origins can also be added:

```env
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://shopeindia.co.in,https://www.shopeindia.co.in
```

---

## CORS Note

In production, avoid using:

```python
allow_origins=["*"]
```

Use only trusted website domains:

```env
ALLOWED_ORIGINS=https://shopeindia.co.in,https://www.shopeindia.co.in
```

This prevents unknown websites from calling the chatbot backend.

---

## Rate Limiting

The backend includes simple IP-based rate limiting.

Default:

```env
RATE_LIMIT_PER_MINUTE=20
```

This means one IP can send 20 messages per minute.

You can increase or decrease this depending on traffic.

---

## Gemini Concurrency Limit

```env
MAX_GEMINI_CONCURRENT_REQUESTS=20
```

This controls how many Gemini API calls can run at the same time.

This helps prevent sudden traffic spikes from exhausting API quota.

---

## Caching

Repeated questions are cached for a few minutes.

Default:

```env
CACHE_TTL_SECONDS=300
```

This reduces Gemini API usage for repeated queries.

---

## Language Behavior

The chatbot follows this language rule:

* English by default
* Replies in Hindi/Hinglish/Marathi or another language if the user writes in that language
* Switches language if the user asks

---

## Medical and Safety Rules

The chatbot should not:

* Give medical diagnosis
* Claim that a product cures disease
* Give treatment plans
* Invent product stock, price, warranty, delivery date, or offers

For medical, therapy, skin, hair, pain, or wellness-related use, the bot advises the user to consult a certified professional.

---

## Product Data

Product data is stored in:

```txt
backend/product_data.py
```

Each product follows this format:

```python
{
    "id": "product-id",
    "name": "Product Name",
    "category": "Category Name",
    "price": 999,
    "old_price": 1299,
    "discount": "20% off",
    "rating": 4.0,
    "description": "Short product description.",
    "keywords": ["keyword1", "keyword2"],
    "product_url": "/product/product-slug",
    "image_url": ""
}
```

To add a new product, add a new dictionary to the `PRODUCTS` list.

---

## Product Links

If exact product URLs are available, use full product URLs:

```python
"product_url": "https://shopeindia.co.in/product/product-slug"
```

If exact product URL is not available, frontend can redirect users to shop/search page.

---

## Frontend Product Cards

If backend returns products, the chatbot UI can show product cards with:

* Product name
* Category
* Price
* Old price
* Discount
* Rating
* View Product button

If backend returns only text, the chatbot still works normally.

---

## Common Local Errors

### Uvicorn not recognized

Use:

```bash
python -m uvicorn main:app --reload
```

Instead of:

```bash
uvicorn main:app --reload
```

---

### ModuleNotFoundError: websockets

Install:

```bash
pip install websockets
```

Or:

```bash
pip install -r requirements.txt
```

---

### Backend se connect nahi ho pa raha

Check:

1. Backend is running
2. Frontend `.env` has correct API URL
3. CORS allows frontend origin
4. Render backend is awake
5. API URL ends with `/chat`

---

## Recommended Production Setup

```txt
Frontend widget:
Integrated into ShopeIndia website

Backend:
Hosted on Render/Railway/VPS

Gemini API Key:
Stored only in backend environment variables

CORS:
Only ShopeIndia domains allowed

Rate Limit:
Enabled

Caching:
Enabled
```

---

## Ownership and API Key Note

The Gemini API key belongs to the business/client.

The key should be added only in backend hosting environment variables.

The key should never be committed to GitHub or shared inside frontend code.

---

## Built By

Built by **Sanu Sharma**

AI & Python Developer
React • FastAPI • Gemini API • AI Systems

---
