# API Documentation

Complete API reference for the Blog Brain content generation system.

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response:**
```json
{
  "service": "Blog Brain API",
  "version": "1.0.0",
  "description": "AI-powered content generation system",
  "endpoints": {
    "health": "/health",
    "generate": "/api/v1/generate-post",
    "docs": "/docs"
  }
}
```

---

### 2. Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Blog Brain API",
  "version": "1.0.0"
}
```

---

### 3. Generate Content

**POST** `/api/v1/generate-post`

Generate SEO-optimized blog content.

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | Yes | Article topic (5-200 chars) |
| `target_audience` | string | No | Target reader demographic |
| `tone` | string | No | Writing tone (default: "professional") |
| `exclude_keywords` | array | No | Keywords to avoid (max 20) |

**Valid Tones:**
- `professional`
- `casual`
- `technical`
- `conversational`
- `formal`
- `friendly`

#### Example Request

```json
{
  "topic": "The Future of AI in Healthcare",
  "target_audience": "Healthcare professionals and medical researchers",
  "tone": "professional",
  "exclude_keywords": ["game-changer", "revolutionary"]
}
```

#### Success Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "metadata": {
      "seo_title": "AI Transforming Healthcare: 7 Key Innovations in 2026",
      "meta_description": "Discover how artificial intelligence is revolutionizing healthcare through diagnostics, treatment planning, and patient care...",
      "slug": "ai-transforming-healthcare-innovations-2026",
      "focus_keyword": "AI in healthcare",
      "estimated_read_time": "8 mins",
      "word_count": 2150,
      "published_date": "2026-02-09T14:30:00Z"
    },
    "content": {
      "html_body": "<h2>Introduction</h2><p>Artificial intelligence...</p>",
      "markdown_body": "## Introduction\n\nArtificial intelligence..."
    },
    "sources": [
      "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8285156/",
      "https://www.nature.com/articles/s41591-020-01197-2",
      "https://www.healthcareitnews.com/news/ai-healthcare-2026"
    ],
    "quality_checks": {
      "ai_isms_removed": true,
      "citations_count": 15,
      "readability_score": "8.5/10",
      "seo_compliance": true,
      "human_sounding": true
    },
    "editor_notes": "Content reviewed and optimized for SEO compliance..."
  },
  "execution_metadata": {
    "execution_time": "127.5s",
    "agents_used": 4,
    "tasks_completed": 4,
    "timestamp": "2026-02-09T14:32:07Z"
  }
}
```

#### Error Responses

**422 Validation Error**
```json
{
  "status": "error",
  "message": "Validation failed",
  "details": [
    {
      "field": "topic",
      "message": "Topic must be at least 5 characters long"
    }
  ]
}
```

**500 Server Error**
```json
{
  "status": "error",
  "message": "Content generation failed",
  "error_code": "GENERATION_ERROR",
  "details": "Unable to complete research phase"
}
```

---

## Response Fields Explained

### Metadata
- **seo_title**: Optimized title (55-60 chars) for search engines
- **meta_description**: SEO description (150-160 chars)
- **slug**: URL-friendly version of title
- **focus_keyword**: Primary SEO keyword
- **estimated_read_time**: Reading time estimate
- **word_count**: Total article word count
- **published_date**: ISO 8601 timestamp

### Content
- **html_body**: Full HTML formatted content
- **markdown_body**: Full Markdown formatted content

### Quality Checks
- **ai_isms_removed**: Verification that AI clichés are removed
- **citations_count**: Number of source citations
- **readability_score**: Content readability rating
- **seo_compliance**: SEO best practices verification
- **human_sounding**: Natural language verification

---

## Rate Limiting

Currently, no rate limiting is enforced. Consider implementing rate limiting in production:
- Recommended: 10 requests per minute per IP
- Generation time: 1-3 minutes per article

---

## Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Invalid request parameters |
| `GENERATION_ERROR` | Content generation failed |
| `API_KEY_ERROR` | Invalid or missing API keys |
| `RATE_LIMIT_ERROR` | Too many requests |

---

## cURL Examples

### Basic generation:
```bash
curl -X POST http://localhost:8000/api/v1/generate-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Cloud Computing Best Practices",
    "tone": "technical"
  }'
```

### With all parameters:
```bash
curl -X POST http://localhost:8000/api/v1/generate-post \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Machine Learning for Beginners",
    "target_audience": "Software developers new to ML",
    "tone": "friendly",
    "exclude_keywords": ["AI", "algorithms"]
  }'
```

---

## Python Client Example

```python
import requests

url = "http://localhost:8000/api/v1/generate-post"
data = {
    "topic": "Blockchain Technology in Supply Chain",
    "target_audience": "Enterprise decision makers",
    "tone": "professional"
}

response = requests.post(url, json=data)
result = response.json()

if result["status"] == "success":
    print(f"Title: {result['data']['metadata']['seo_title']}")
    print(f"Word Count: {result['data']['metadata']['word_count']}")
    print(f"\nContent:\n{result['data']['content']['markdown_body']}")
else:
    print(f"Error: {result['message']}")
```

---

## Interactive API Docs

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test endpoints directly in the browser.
