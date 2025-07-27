# Inventory Management System

A Streamlit-based inventory management platform with Google API integration for bill analysis. Features include:
- View and upload inventory
- Upload purchase bill images for automatic detail extraction
- API-based backend (FastAPI)
- Modular frontend/backend structure
- Uses Gemini API, Streamlit, and python-dotenv

## Setup
- Install dependencies using [uv](https://github.com/astral-sh/uv):
  ```sh
  uv pip install -r requirements.txt
  ```
- Copy `.env.example` to `.env` and fill in your API keys.
- Start backend and frontend as described in respective directories.
