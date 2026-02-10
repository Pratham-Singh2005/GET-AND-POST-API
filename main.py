from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Union
import math
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="BFHL Combined API",
    description="Production-ready POST /bfhl and GET /health endpoints",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OFFICIAL_EMAIL = os.getenv("OFFICIAL_EMAIL", "pratham3906.beai23@chitkara.edu.in")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# Request Models
class BFHLRequest(BaseModel):
    fibonacci: Optional[int] = None
    prime: Optional[List[int]] = None
    lcm: Optional[List[int]] = None
    hcf: Optional[List[int]] = None
    AI: Optional[str] = None


# Response Models
class SuccessResponse(BaseModel):
    is_success: bool = True
    official_email: str
    data: Union[List[int], int, str]


class ErrorResponse(BaseModel):
    is_success: bool = False
    official_email: str
    error: str


class HealthResponse(BaseModel):
    is_success: bool
    official_email: str
    error: Optional[str] = None


# Helper Functions
def generate_fibonacci(n: int) -> List[int]:
    """Generate Fibonacci series up to N terms"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def is_prime(num: int) -> bool:
    """Check if a number is prime"""
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True


def filter_primes(numbers: List[int]) -> List[int]:
    """Filter prime numbers from array"""
    return [num for num in numbers if is_prime(num)]


def gcd(a: int, b: int) -> int:
    """Calculate GCD of two numbers using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Calculate LCM of two numbers"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def calculate_hcf(numbers: List[int]) -> int:
    """Calculate HCF (GCD) of array of numbers"""
    if not numbers:
        raise ValueError("Array cannot be empty")
    
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result


def calculate_lcm(numbers: List[int]) -> int:
    """Calculate LCM of array of numbers"""
    if not numbers:
        raise ValueError("Array cannot be empty")
    
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result


def get_ai_response(question: str) -> str:
    """Call Google Gemini API and return one-word answer"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured in environment variables")
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"{question}\n\nProvide ONLY a one-word answer. No explanations, no punctuation, just one word."
        response = model.generate_content(prompt)
        
        # Extract and clean the response
        answer = response.text.strip().split()[0]  # Get first word
        # Remove any punctuation
        answer = ''.join(char for char in answer if char.isalnum())
        
        return answer
    except Exception as e:
        raise ValueError(f"AI service error: {str(e)}")


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "BFHL Combined API is running",
        "endpoints": {
            "/health": "GET - Health check endpoint",
            "/bfhl": "POST - Operations endpoint (fibonacci, prime, lcm, hcf, AI)"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


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
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "is_success": True,
                "official_email": OFFICIAL_EMAIL
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in health check: {str(e)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": "Internal server error"
            }
        )


@app.post(
    "/bfhl",
    response_model=SuccessResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="BFHL Operations Endpoint",
    description="Handles fibonacci, prime, lcm, hcf, and AI operations"
)
async def bfhl_endpoint(request: BFHLRequest):
    """
    POST endpoint that handles fibonacci, prime, lcm, hcf, and AI operations.
    Only one key should be provided in the request.
    """
    try:
        # Count how many keys are provided
        provided_keys = []
        if request.fibonacci is not None:
            provided_keys.append("fibonacci")
        if request.prime is not None:
            provided_keys.append("prime")
        if request.lcm is not None:
            provided_keys.append("lcm")
        if request.hcf is not None:
            provided_keys.append("hcf")
        if request.AI is not None:
            provided_keys.append("AI")
        
        # Validate exactly one key
        if len(provided_keys) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Request must contain exactly one key (fibonacci, prime, lcm, hcf, or AI)"
                }
            )
        
        if len(provided_keys) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": f"Only one key allowed. Found: {', '.join(provided_keys)}"
                }
            )
        
        # Process based on the provided key
        if request.fibonacci is not None:
            if request.fibonacci < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "Fibonacci input must be a non-negative integer"
                    }
                )
            data = generate_fibonacci(request.fibonacci)
        
        elif request.prime is not None:
            if not request.prime:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "Prime array cannot be empty"
                    }
                )
            data = filter_primes(request.prime)
        
        elif request.lcm is not None:
            if not request.lcm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "LCM array cannot be empty"
                    }
                )
            if 0 in request.lcm:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "LCM cannot be calculated with zero"
                    }
                )
            data = calculate_lcm(request.lcm)
        
        elif request.hcf is not None:
            if not request.hcf:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "HCF array cannot be empty"
                    }
                )
            data = calculate_hcf(request.hcf)
        
        elif request.AI is not None:
            if not request.AI.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "is_success": False,
                        "official_email": OFFICIAL_EMAIL,
                        "error": "AI question cannot be empty"
                    }
                )
            data = get_ai_response(request.AI)
        
        return SuccessResponse(
            is_success=True,
            official_email=OFFICIAL_EMAIL,
            data=data
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": str(e)
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in /bfhl: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": f"Internal server error: {str(e)}"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
