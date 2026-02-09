# Deployment Guide

Complete guide for deploying Blog Brain to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required API Keys

1. **Google Gemini API Key**
   - Sign up at [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Free tier: 60 requests/minute
   - Production recommended: Pay-as-you-go

2. **Serper.dev API Key**
   - Create account at [Serper.dev](https://serper.dev)
   - Free tier: 2,500 searches/month
   - Production: $50/month for 5,000 searches

### System Requirements

- **Python**: 3.11 or higher
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Storage**: 500MB for dependencies
- **Network**: Stable internet connection

---

## Local Development

### 1. Installation

```bash
# Clone repository
git clone https://github.com/hamzakhaliq-404/blog-brain-python.git
cd blog-brain-python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use any text editor
```

Required variables:
```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
GEMINI_MODEL=gemini-3-pro-preview
```

### 3. Run Development Server

```bash
python main.py
```

Server runs at: `http://localhost:8000`

### 4. Test Installation

```bash
# Health check
curl http://localhost:8000/health

# Run tests
pytest tests/ -v
```

---

## Production Deployment

### Option 1: Docker Deployment (Recommended)

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  blog-brain:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
```

#### 3. Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

### Option 2: Cloud Deployment

#### Deploy to Railway

1. Create account at [Railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Add environment variables in Railway dashboard
5. Deploy automatically on push

#### Deploy to Render

1. Create account at [Render.com](https://render.com)
2. New → Web Service
3. Connect repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

#### Deploy to AWS EC2

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 2. Install Python and dependencies
sudo apt update
sudo apt install python3.11 python3-pip -y

# 3. Clone and setup
git clone <your-repo>
cd blog-brain-python
pip3 install -r requirements.txt

# 4. Create systemd service
sudo nano /etc/systemd/system/blog-brain.service
```

Service file:
```ini
[Unit]
Description=Blog Brain API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/blog-brain-python
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# 5. Start service
sudo systemctl start blog-brain
sudo systemctl enable blog-brain

# 6. Check status
sudo systemctl status blog-brain
```

---

## Environment Configuration

### Production .env Template

```env
# API Keys
GEMINI_API_KEY=your_production_gemini_key
SERPER_API_KEY=your_production_serper_key
GEMINI_MODEL=gemini-3-pro-preview

# API Configuration (Production)
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

# CORS (Update with your frontend domains)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Logging
LOG_LEVEL=INFO

# Agent Settings
RESEARCHER_TEMPERATURE=0.2
STRATEGIST_TEMPERATURE=0.4
WRITER_TEMPERATURE=0.7
EDITOR_TEMPERATURE=0.3

# CrewAI Settings
ENABLE_MEMORY=True
ENABLE_DELEGATION=True
MAX_ITERATIONS=3
```

---

## Reverse Proxy Setup

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running requests
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

### SSL with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Monitoring

### Health Check Endpoint

Monitor: `GET /health`

Expected response:
```json
{"status": "healthy", "service": "Blog Brain API"}
```

### Logging

Logs location:
- Development: Console output
- Production: `/var/log/blog-brain/` (configure as needed)

### Performance Metrics

Monitor:
- Response time (expect 60-180s per generation)
- Memory usage (expect 200-500MB)
- API error rates
- LLM token usage

---

## Scaling Considerations

### Horizontal Scaling

- Deploy multiple instances behind load balancer
- Use message queue (RabbitMQ/Redis) for job management
- Consider async/background processing with Celery

### Vertical Scaling

- Increase RAM for concurrent requests
- Use faster CPU for reduced generation time

---

## Security Best Practices

1. **Environment Variables**
   - Never commit `.env` to version control
   - Use secret management (AWS Secrets Manager, Vault)

2. **API Rate Limiting**
   - Implement rate limiting middleware
   - Use API keys for authentication

3. **CORS**
   - Restrict `ALLOWED_ORIGINS` to trusted domains only

4. **HTTPS**
   - Always use SSL/TLS in production
   - Force HTTPS redirects

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>
```

#### 2. Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. API Key Errors
- Verify keys in `.env`
- Check API quotas and limits
- Ensure `GOOGLE_API_KEY` environment variable is set

#### 4. Generation Timeout
- Increase `proxy_read_timeout` in Nginx
- Check network connectivity
- Verify API keys are valid

---

## Cost Optimization

### Production Monthly Costs (100 articles)

| Service | Cost |
|---------|------|
| Gemini API | ~$28 |
| Serper.dev | $50 |
| Hosting (Railway/Render) | $25-40 |
| **Total** | **~$103-118/month** |

### Cost Reduction Tips

1. Cache research results (reduce Serper calls)
2. Use Gemini Flash model for research phase
3. Implement request batching
4. Set up monitoring alerts for quota usage

---

## Backup and Recovery

### Database Backup (if using)
```bash
# Backup (if using SQLite)
cp blog_brain.db blog_brain_backup_$(date +%Y%m%d).db
```

### Configuration Backup
```bash
# Backup .env
cp .env .env.backup
```

---

## Support

For deployment issues:
1. Check logs: `docker-compose logs` or `journalctl -u blog-brain`
2. Verify environment variables
3. Test API endpoints manually
4. Review GitHub issues

---

**Last Updated**: 2026-02-09
