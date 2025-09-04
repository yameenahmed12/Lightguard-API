# LightGuard API

A production-ready LLM safety filter that detects and blocks jailbreak attempts in real-time using a fine-tuned DistilBERT model.

## Features

- Advanced Pattern Recognition: Detects sophisticated manipulation techniques beyond simple keyword matching
- Real-time Jailbreak Detection: Identifies malicious prompts with 90% confidence threshold
- Explainable AI: Shows which linguistic patterns triggered the safety filter
- Production Ready: FastAPI backend with React frontend, containerized with Docker
- Cloud Deployed: Running on Google Cloud Run for scalability
- RESTful API: Simple JSON API for easy integration

## Architecture

- Backend: FastAPI with Python 3.11
- Model: Fine-tuned DistilBERT for sequence classification
- Frontend: React TypeScript with modern UI
- Deployment: Docker container on Google Cloud Run
- Model Hosting: Hugging Face Hub (yahmed124/lightguard-model)

## Technical Specifications

- Model: Fine-tuned DistilBERT (knowledge distillation from BERT)
- Training Data: 1,400+ real-world jailbreak prompts from TrustAIRLab dataset
- Validation Accuracy: 100% on held-out test set
- Model Size: ~268MB (optimized for production deployment)
- Inference Time: <100ms per request
- Threshold: 90% confidence for blocking prompts
- API Response Time: <500ms end-to-end

## Use Cases

### LLM Application Protection
- Protect ChatGPT-style applications from prompt injection
- Block attempts to bypass safety guidelines
- Prevent malicious users from extracting harmful content

### Enterprise AI Systems
- Secure internal AI assistants
- Protect customer-facing chatbots
- Ensure compliance with AI safety policies

### Content Moderation
- Pre-filter user inputs before sending to LLMs
- Reduce costs by blocking malicious requests early
- Provide transparency with explanation features

### Research & Development
- Study jailbreak patterns and techniques
- Develop better safety measures
- Analyze prompt engineering attacks

## Quick Start

### API Usage

```bash
curl -X POST "https://your-api-url/check-safety" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your prompt here"}'
```

### Response Format

```json
{
  "safe": false,
  "jailbreak_score": 0.95,
  "message": "Blocked: High jailbreak probability.",
  "explanation": "'ignore' (0.15) | 'instructions' (0.12) | 'bypass' (0.08)"
}
```

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 16+
- Docker (optional)

### Setup

1. Clone the repository
```bash
git clone https://github.com/yameenahmed12/Lightguard-API.git
cd Lightguard-API
```

2. Install dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run build
cd ..
```

3. Run locally
```bash
python main.py
```

4. Access the application
- Frontend: http://localhost:7860
- API Docs: http://localhost:7860/docs

## Project Structure

```
LightGuard-API/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── cloudbuild.yaml        # Google Cloud Build config
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   └── App.css        # Styling
│   └── build/             # Production build
└── README.md
```

## API Endpoints

- POST /check-safety - Analyze prompt safety
- GET / - Serve React frontend
- GET /docs - Interactive API documentation

## Deployment

### Google Cloud Run
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Docker
```bash
docker build -t lightguard-api .
docker run -p 7860:7860 lightguard-api
```

## Performance

- Model Loading: ~2-3 seconds on cold start
- Memory Usage: ~1-2GB RAM
- Concurrent Requests: Handles 10+ requests/second
- Uptime: 99%+ on Google Cloud Run

## Security Features

- Input validation and sanitization
- Rate limiting ready (can be added)
- Secure model loading from Hugging Face
- No sensitive data logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Model fine-tuned on [Hugging Face](https://huggingface.co/)
- Deployed on [Google Cloud Run](https://cloud.google.com/run)
- Frontend built with [React](https://reactjs.org/)

## Contact

- GitHub: [yameenahmed12](https://github.com/yameenahmed12)
- Model: [yahmed124/lightguard-model](https://huggingface.co/yahmed124/lightguard-model)

---

**Disclaimer**: This tool is designed to help identify potential jailbreak attempts but should not be the only security measure. Always implement multiple layers of security for production AI systems.
