"""
Main FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import routers
from .routers import auth, clients, purchases, stock, dashboard, ai

# Create FastAPI app
app = FastAPI(
    title="LoyalLight API",
    description="Customer Management System with AI Integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for image uploads
uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(purchases.router)
app.include_router(stock.router)
app.include_router(dashboard.router)
app.include_router(ai.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LoyalLight API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

