# US Consumer Data API

Real-time US consumer spending, confidence, savings, and debt data. Powered by FRED (Federal Reserve Economic Data).

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All consumer indicators snapshot |
| `GET /spending` | Personal consumption expenditures (PCE) |
| `GET /confidence` | University of Michigan Consumer Sentiment |
| `GET /savings-rate` | Personal saving rate (PSAVERT) |
| `GET /debt` | Household debt service payments (TDSP) |
| `GET /credit` | Revolving consumer credit (REVOLSL) |

## Data Source

FRED - Federal Reserve Bank of St. Louis
https://fred.stlouisfed.org/

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
