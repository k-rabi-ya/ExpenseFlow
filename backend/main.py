"""
Main FastAPI application
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

from app.services.categorization import CategorizationService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ExpenseFlow API",
    description="Automated expense categorization service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize categorization service
categorization_service = CategorizationService()


# Pydantic models for request/response
class CategorizationRequest(BaseModel):
    """Request model for categorization"""
    description: str


class CategorizationResponse(BaseModel):
    """Response model for categorization"""
    description: str
    category: str
    confidence: float


class BatchCategorizeRequest(BaseModel):
    """Request model for batch categorization"""
    descriptions: List[str]


class BatchCategorizeResponse(BaseModel):
    """Response model for batch categorization"""
    processed: int
    categorized: int
    results: List[CategorizationResponse]


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model_loaded": categorization_service.model_loaded
    }


# Single categorization endpoint
@app.post("/api/categorize", response_model=CategorizationResponse)
async def categorize(request: CategorizationRequest):
    """Categorize a single transaction description"""
    if not categorization_service.model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )

    category, confidence = categorization_service.predict(request.description)

    return CategorizationResponse(
        description=request.description,
        category=category,
        confidence=round(confidence, 4)
    )


# Batch categorization endpoint
@app.post("/api/batch-categorize", response_model=BatchCategorizeResponse)
async def batch_categorize(request: BatchCategorizeRequest):
    """Categorize multiple transaction descriptions"""
    if not categorization_service.model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )

    results = []
    for description in request.descriptions:
        category, confidence = categorization_service.predict(description)
        results.append(CategorizationResponse(
            description=description,
            category=category,
            confidence=round(confidence, 4)
        ))

    return BatchCategorizeResponse(
        processed=len(request.descriptions),
        categorized=len([r for r in results if r.confidence > 0.5]),
        results=results
    )


# CSV import endpoint (placeholder)
@app.post("/api/import")
async def import_csv(file: UploadFile = File(...)):
    """Import and categorize transactions from CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")

    # TODO: Implement CSV parsing and batch categorization
    return {
        "processed": 0,
        "categorized": 0,
        "uncategorized": 0
    }


# OCR endpoint (placeholder)
@app.post("/api/ocr-categorize")
async def ocr_categorize(file: UploadFile = File(...)):
    """Extract text from receipt image and categorize"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # TODO: Implement OCR and categorization
    return {
        "merchant": "",
        "amount": 0.0,
        "category": "Other",
        "confidence": 0.0
    }


# Correction feedback endpoint (placeholder)
@app.post("/api/correct")
async def record_correction(data: dict):
    """Record user correction for retraining"""
    # TODO: Save correction to database and schedule retraining
    return {"status": "recorded", "retraining_scheduled": "tonight"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT, fallback to 5000 locally
    uvicorn.run(app, host="0.0.0.0", port=port)
