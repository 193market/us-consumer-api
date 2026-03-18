from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from datetime import datetime

app = FastAPI(
    title="US Consumer Data API",
    description="Real-time US consumer spending, confidence, savings, and debt data. Powered by FRED.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
API_KEY = os.environ.get("FRED_API_KEY", "")


async def fetch_fred(series_id: str, limit: int = 12):
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(BASE_URL, params={
            "series_id": series_id,
            "api_key": API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        })
        data = res.json()
        return data.get("observations", [])


@app.get("/")
def root():
    return {
        "api": "US Consumer Data API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "endpoints": ["/summary", "/spending", "/confidence", "/savings-rate", "/debt", "/credit"],
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/summary")
async def summary(limit: int = Query(default=10, ge=1, le=60)):
    """All consumer indicators snapshot"""
    spending, confidence, savings = await asyncio.gather(
        fetch_fred("PCE", limit),
        fetch_fred("UMCSENT", limit),
        fetch_fred("PSAVERT", limit),
    )
    return {
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": {
            "personal_consumption_expenditures": spending,
            "consumer_sentiment": confidence,
            "personal_savings_rate": savings,
        }
    }


@app.get("/spending")
async def spending(limit: int = Query(default=12, ge=1, le=60)):
    """Personal consumption expenditures (PCE)"""
    data = await fetch_fred("PCE", limit)
    return {
        "indicator": "Personal Consumption Expenditures",
        "series_id": "PCE",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/confidence")
async def confidence(limit: int = Query(default=12, ge=1, le=60)):
    """University of Michigan Consumer Sentiment Index"""
    data = await fetch_fred("UMCSENT", limit)
    return {
        "indicator": "University of Michigan: Consumer Sentiment",
        "series_id": "UMCSENT",
        "unit": "Index 1966:Q1=100",
        "frequency": "Monthly",
        "source": "FRED - University of Michigan",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/savings-rate")
async def savings_rate(limit: int = Query(default=12, ge=1, le=60)):
    """Personal saving rate"""
    data = await fetch_fred("PSAVERT", limit)
    return {
        "indicator": "Personal Saving Rate",
        "series_id": "PSAVERT",
        "unit": "Percent",
        "frequency": "Monthly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/debt")
async def debt(limit: int = Query(default=12, ge=1, le=60)):
    """Household debt service payments as percent of disposable income"""
    data = await fetch_fred("TDSP", limit)
    return {
        "indicator": "Household Debt Service Payments as a Percent of Disposable Personal Income",
        "series_id": "TDSP",
        "unit": "Percent",
        "frequency": "Quarterly",
        "source": "FRED - Federal Reserve Board",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/credit")
async def credit(limit: int = Query(default=12, ge=1, le=60)):
    """Revolving consumer credit outstanding"""
    data = await fetch_fred("REVOLSL", limit)
    return {
        "indicator": "Revolving Consumer Credit Owned and Securitized",
        "series_id": "REVOLSL",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Federal Reserve Board",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
