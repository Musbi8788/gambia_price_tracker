# 🚀 Deployment Guide

This guide covers different ways to deploy your Gambia Price Tracker application.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of command line

## 🌐 Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy your app for free.

### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app_v2.py`
   - Click "Deploy"

3. **Configure Environment**
   - Add any environment variables if needed
   - Set Python version to 3.8+

### Benefits:
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Custom domain support
- ✅ Easy scaling

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app_v2.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build image
docker build -t gambia-price-tracker .

# Run container
docker run -p 8501:8501 gambia-price-tracker
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
```

## ☁️ Cloud Platforms

### Heroku
1. Create `Procfile`:
   ```
   web: streamlit run app_v2.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Google Cloud Platform
1. Create `app.yaml`:
   ```yaml
   runtime: python39
   entrypoint: streamlit run app_v2.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   gcloud app deploy
   ```

### AWS
1. Use AWS Elastic Beanstalk
2. Configure environment for Python
3. Deploy using AWS CLI or console

## 🖥️ Local Server

### Production Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app_v2.py --server.port=8501 --server.address=0.0.0.0
```

### Using Gunicorn (Alternative)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 streamlit.web.cli:main -- --server.port=8501 app_v2.py
```

## 🔧 Environment Configuration

### Environment Variables
Create `.env` file:
```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Production Settings
```python
# In config.py
import os

# Production settings
if os.getenv('ENVIRONMENT') == 'production':
    DEBUG = False
    LOG_LEVEL = 'WARNING'
else:
    DEBUG = True
    LOG_LEVEL = 'INFO'
```

## 📊 Database Migration

### From CSV to Database
When ready to upgrade from CSV to database:

1. **Install database dependencies**
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```

2. **Create migration script**
   ```python
   # migrate_to_db.py
   import pandas as pd
   from sqlalchemy import create_engine
   
   # Read CSV data
   df = pd.read_csv('data/prices.csv')
   
   # Create database connection
   engine = create_engine('postgresql://user:pass@localhost/gambia_prices')
   
   # Migrate data
   df.to_sql('prices', engine, if_exists='replace', index=False)
   ```

## 🔒 Security Considerations

### Production Checklist
- [ ] Use HTTPS
- [ ] Set up proper authentication
- [ ] Configure CORS if needed
- [ ] Set up monitoring and logging
- [ ] Regular backups
- [ ] Rate limiting
- [ ] Input validation

### Security Headers
```python
# Add to app configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add security headers
st.markdown("""
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">
""", unsafe_allow_html=True)
```

## 📈 Monitoring & Analytics

### Basic Monitoring
```python
# Add to app
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track usage
def track_usage():
    logger.info(f"App accessed at {time.time()}")
```

### Advanced Monitoring
- Use services like Sentry for error tracking
- Set up Google Analytics for usage insights
- Monitor server performance with tools like New Relic

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Streamlit Cloud
      uses: streamlit/streamlit-cloud-action@v1
      with:
        streamlit-app-path: app_v2.py
```

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8501
   # Kill process
   kill -9 <PID>
   ```

2. **Permission denied**
   ```bash
   # Fix permissions
   chmod +x app_v2.py
   ```

3. **Dependencies not found**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Logs
```bash
# View Streamlit logs
streamlit run app_v2.py --logger.level=debug

# View system logs
journalctl -u streamlit-app
```

## 📞 Support

For deployment issues:
1. Check the [Streamlit documentation](https://docs.streamlit.io)
2. Review error logs
3. Test locally first
4. Ask for help in the community

---

**Happy Deploying! 🚀** 