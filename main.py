"""
FastAPI Health Check Endpoint
Production-ready GET /health endpoint with proper error handling
"""

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Health Check API",
    description="Production-ready health check endpoint",
    version="1.0.0"
)

# Response model for type safety and documentation
class HealthResponse(BaseModel):
    is_success: bool
    official_email: str
    error: str | None = None

# Replace with your actual Chitkara email
OFFICIAL_EMAIL = "your.email@chitkara.edu.in"


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check Endpoint",
    description="Returns the health status of the API server"
)
async def health_check():
    """
    Health check endpoint that always responds when the server is running.
    
    Returns:
        JSON response with success status and official email
    """
    try:
        # Health check logic - always returns success if server is running
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "is_success": True,
                "official_email": OFFICIAL_EMAIL
            }
        )
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Unexpected error in health check: {str(e)}")
        
        # Return error response with 500 status
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": "Internal server error"
            }
        )


# Optional: Root endpoint for API documentation redirect
@app.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation"""
    return {
        "message": "Health Check API is running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
