# 🚀 AI Background Generation

A production grade FastAPI service for AI Background Generation using fine-tuned diffusion models

## Features
- **Modular Architecture**: Clean package structure with separated concerns
- **Authentication**: Token authentication for secure access
- **Monitoring**: Comprehensive Prometheus metrics for observability
- **Performance**: Pruned-optimized model for fast inference
- **Rate Limiting**: Built-in request throttling
- **Production Ready**: Docker support, error handling, logging


## API Endpoints
- `POST /generate` - Upload an product image files for background generation
<!-- - `POST /generate/url` - Analyze images from URLs -->
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics endpoint
- `GET /docs` - Interactive API documentation


## Architecture
```
ai-background-generation/
├── api/                    # Main package
│   ├── core/               # Core functionality
│   │   ├── auth.py         # Authentication & rate limiting
│   │   ├── config.py       # Configuration settings
│   │   ├── metrics.py      # Prometheus metrics
│   │   └── utils.py        # Utility functions
│   ├── models/             # Data models
│   │   └── models.py       # Pydantic response models
│   └── services/           # Business logic
│       └── inference.py    # ML model inference
├── main.py                 # FastAPI application
├── models/                 # Pre-trained model files
└── scripts/                # Utility scripts
```


## 🛠️ Technical Stack

### Core Dependencies
- **FastAPI** - Modern web framework for APIs
- **Diffusers** - Hugging Face's diffusers library for building image generation models
- **Prometheus Client** - Metrics and monitoring
- **PyTorch** - Deep learning framework with MPS support
- **Uvicorn** - ASGI server

### Development Tools
- **UV** - Fast Python package manager
- **Jupyter** - Interactive development environment
- **Docker** - Containerization support


## ⚡ Setup Instructions

### Prerequisites
- Python 3.11+
- UV package manager (recommended) or pip

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ai-background-generation

# Install dependencies with UV (recommended)
uv sync

# Or with pip
pip install -r requirements.txt
```

### Environment Configuration
```bash
# For ai-background-generation API
export API_KEY="your-secure-api-key"
export MODEL_PATH=""
```

## 📈 Performance Metrics

The API includes comprehensive Prometheus metrics:

### HTTP Metrics
- `http_requests_total` - Request counts by endpoint/method/status
- `http_request_duration_seconds` - Request latency histograms
- `http_requests_active` - Active request gauge

### ML Inference Metrics
- `ai_bg_predictions_total` - Prediction counts by generation
- `ai_bg_inference_duration_seconds` - Inference time distribution
- `ai_bg_prediction_confidence` - Confidence score histograms

### System Metrics
- `ai_bg_model_load_time_seconds` - Model initialization time
- `ai_bg_model_loaded` - Model status indicator
- `rate_limit_hits_total` - Rate limiting statistics

## 🚀 Deployment

### Docker Deployment
```bash
cd ai-background-generation/
docker build -t ai-background-generation .
docker run -p 8000:8000 -e API_KEY=your-key ai-background-generation
```

### Production Considerations
- Use environment variables for configuration
- Set up reverse proxy (nginx) for SSL termination
- Configure monitoring with Prometheus/Grafana
- Implement log aggregation
- Set appropriate rate limits for your use case


## 💡 Use Cases

### Production
- Generating product packshots 
- Automated image generation

### Educational
- Learn customizing image generation models for industrial use-cases
- Understand modern ML API development
- Practice with different model types (NLP, Computer Vision)