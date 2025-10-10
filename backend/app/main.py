from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models, database
from app.routes import auth, reddit, users
from app import sentiment

# Create all tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Reddit Sentiment Analyzer",
    description="API for authentication, users, and reddit sentiment analysis",
    version="1.0.0"
)

# ✅ Allow CORS (for frontend communication)
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or use ["*"] for testing (not secure for production)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers (like Authorization, Content-Type)
)

# ✅ Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(reddit.router)
app.include_router(sentiment.router)

# ✅ Root endpoint
@app.get("/")
def root():
    return {"msg": "Backend running with PostgreSQL and FastAPI!"}
