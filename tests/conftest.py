import os

# Set env vars BEFORE app modules are imported, since app/config.py reads
# them at import time via os.environ["..."]. These are dummy values for tests
# that don't touch external services.
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost/test")
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest-only")
