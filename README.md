# BFHL Combined API - FastAPI

Production-ready REST API with POST `/bfhl` and GET `/health` endpoints built with Python and FastAPI.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Pratham-Singh2005/GET-API.git
cd GET-API
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
OFFICIAL_EMAIL=your.email@chitkara.edu.in
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Note:** Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 4. Run the Server

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

---

## 📋 API Documentation

### 1. GET /health - Health Check

**Endpoint:** `GET /health`

**Description:** Health check endpoint that always responds when the server is running.

**Request:** No parameters required

**Success Response (HTTP 200):**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in"
}
```

**Error Response (HTTP 500):**

```json
{
  "is_success": false,
  "official_email": "your.email@chitkara.edu.in",
  "error": "Internal server error"
}
```

**Test with cURL:**

```bash
curl https://your-deployed-api.com/health
```

**Test with PowerShell:**

```powershell
Invoke-RestMethod -Uri https://your-deployed-api.com/health -Method Get
```

---

### 2. POST /bfhl - Operations Endpoint

**Endpoint:** `POST /bfhl`

**Description:** Performs various mathematical and AI operations. Only one key allowed per request.

**Request Body:** JSON with exactly ONE of the following keys:

#### Operation 1: Fibonacci

```json
{
  "fibonacci": 5
}
```

**Response:**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in",
  "data": [0, 1, 1, 2, 3]
}
```

#### Operation 2: Prime Numbers

```json
{
  "prime": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

**Response:**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in",
  "data": [2, 3, 5, 7]
}
```

#### Operation 3: LCM (Least Common Multiple)

```json
{
  "lcm": [12, 15, 20]
}
```

**Response:**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in",
  "data": 60
}
```

#### Operation 4: HCF (Highest Common Factor)

```json
{
  "hcf": [12, 15, 20]
}
```

**Response:**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in",
  "data": 1
}
```

#### Operation 5: AI Query (Google Gemini)

```json
{
  "AI": "What is the capital of France?"
}
```

**Response:**

```json
{
  "is_success": true,
  "official_email": "your.email@chitkara.edu.in",
  "data": "Paris"
}
```

**Error Response (HTTP 400/500):**

```json
{
  "is_success": false,
  "official_email": "your.email@chitkara.edu.in",
  "error": "Error description"
}
```

**Test with cURL:**

```bash
curl -X POST https://your-deployed-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"fibonacci": 5}'
```

**Test with PowerShell:**

```powershell
$body = @{fibonacci = 5} | ConvertTo-Json
Invoke-RestMethod -Uri https://your-deployed-api.com/bfhl -Method Post -Body $body -ContentType "application/json"
```

---

## 🧪 Testing Locally

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🌐 Deployment Steps (Add After Development)

### Vercel
1. Login → New Project → Import repository
2. Configure runtime
3. Deploy and copy public URL

### Railway
1. New Project → Deploy from GitHub
2. Select repository
3. Configure variables
4. Deploy and copy URL

### Render
1. New Web Service → Select repository
2. Choose runtime
3. Set build & start commands
4. Deploy and copy URL

---

## ✨ Features

✅ **Two Production Endpoints** - POST `/bfhl` and GET `/health`  
✅ **Multiple Operations** - Fibonacci, Prime, LCM, HCF, AI  
✅ **Google Gemini Integration** - AI-powered responses  
✅ **Input Validation** - Comprehensive error handling  
✅ **CORS Enabled** - Cross-origin requests supported  
✅ **Auto Documentation** - Swagger UI & ReDoc  
✅ **Environment Variables** - Secure configuration  
✅ **Never Crashes** - Robust error handling  
✅ **FastAPI Best Practices** - Type hints, response models, logging  

---

## 📦 Project Structure

```
GET-API/
├── main.py              # FastAPI application with both endpoints
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OFFICIAL_EMAIL` | Yes | Your Chitkara University email |
| `GEMINI_API_KEY` | Yes (for AI) | Google Gemini API key for AI operations |

---

## 📝 Sample Requests

### Health Check

```bash
curl https://your-api.com/health
```

### Fibonacci

```bash
curl -X POST https://your-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"fibonacci": 10}'
```

### Prime Numbers

```bash
curl -X POST https://your-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"prime": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}'
```

### LCM

```bash
curl -X POST https://your-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"lcm": [12, 15, 20]}'
```

### HCF

```bash
curl -X POST https://your-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"hcf": [48, 18]}'
```

### AI Query

```bash
curl -X POST https://your-api.com/bfhl \
  -H "Content-Type: application/json" \
  -d '{"AI": "What is the capital of India?"}'
```

---

## 🎯 Submission Requirements (All Met)

✅ **Public GitHub Repository** - Source code publicly available  
✅ **Full Source Code** - Complete `main.py` with both endpoints  
✅ **requirements.txt** - All dependencies listed  
✅ **README with API Usage** - Comprehensive documentation  
✅ **Both APIs in Same Repository** - POST /bfhl + GET /health  
✅ **Deployment Ready** - Instructions for Render/Railway/Vercel  
✅ **Sample Requests** - cURL and PowerShell examples provided  

---

## 📄 License

MIT License - Free to use for educational purposes

---

## 👨‍💻 Author

**Pratham Singh**  
Chitkara University  
GitHub: [@Pratham-Singh2005](https://github.com/Pratham-Singh2005)

---

## 🆘 Support

For issues or questions:
- Open an issue on GitHub
- Check the interactive docs at `/docs`
- Review the API examples above
