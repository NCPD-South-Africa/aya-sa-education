# Installation Guide

Quick installation guide for SA Edu LLM.

## Prerequisites

### Hardware
- Minimum: 16GB RAM, 8GB VRAM GPU
- Recommended: 32GB RAM, 12GB VRAM GPU

### Software
- Ubuntu 24.04 LTS
- Python 3.11+
- CUDA 12.1+
- Docker (optional)

## Quick Start (Local)

```bash
# Clone repository
git clone https://github.com/[your-org]/aya-sa-education.git
cd aya-sa-education

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download model
python scripts/download_model.py --quantization int8

# Run server
python scripts/run_server.py
```

Visit http://localhost:8000

## Cloud Deployment

See [docs/cloud-deployment-guide.md](docs/cloud-deployment-guide.md) for:
- Google Cloud Platform setup
- AWS deployment
- Azure configuration

## Docker Deployment

```bash
cd deployment/docker
docker-compose up -d
```

## Troubleshooting

### GPU Not Detected
```bash
nvidia-smi
```

### Out of Memory
Use INT8 quantization:
```bash
python scripts/download_model.py --quantization int8
```

## Support

- GitHub Issues

- Email: llm-support@ncpd.org.za
