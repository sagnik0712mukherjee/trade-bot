from pathlib import Path

# =========================
# Base Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

HOLDINGS_CSV = DATA_DIR / "holdings.csv"
TRADES_CSV = DATA_DIR / "trades.csv"

VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# =========================
# Embedding Configuration
# =========================

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Number of documents to retrieve
TOP_K = 20

# Similarity threshold for refusal
SIMILARITY_THRESHOLD = 0.5

# =========================
# LLM Configuration
# =========================

LLM_PROVIDER = "openai"
LLM_MODEL_NAME = "gpt-5.2"

# NOTE:
# No temperature set on purpose
# We want deterministic, factual answers only

# =========================
# Voice Configuration
# =========================

ENABLE_VOICE_INPUT = True

VOICE_LANGUAGE = "en-US"

# =========================
# Streamlit Configuration
# =========================

APP_TITLE = "Trade Bot – Holdings & Trades Assistant"

# =========================
# Logging
# =========================

LOG_LEVEL = "INFO"
