# 🇿🇦 Aya LLM for South African Education

> An open-source, multilingual AI educational assistant built on Aya 23, designed specifically for South African schools and students.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Model-Aya%2023%20(8B)-orange.svg)](https://huggingface.co/CohereForAI/aya-23-8B)

## 🎯 Mission

To democratise access to quality AI-powered education across South Africa by providing a multilingual, curriculum-aligned learning assistant that respects our linguistic diversity and cultural context.

## ✨ Key Features

- **Multilingual Support**: Built on Aya 23 with support for English, Afrikaans, isiZulu, isiXhosa, and expanding
- **CAPS-Aligned**: Curriculum and Assessment Policy Statement (CAPS) aligned content for Grades 8-12
- **Offline-Capable**: Designed to work without constant internet connectivity
- **Privacy-First**: All student data stays on school premises (POPIA compliant)
- **Open Source**: Fully transparent, modifiable, and community-driven
- **Load Shedding Resilient**: Designed for South African power realities

## 🚀 Current Status

**Phase**: Proof of Concept  
**Version**: 0.1.0-alpha  
**Languages**: English (excellent), Afrikaans (good), isiZulu (in development)

We're currently seeking:
- Pilot schools in Gauteng (2-3 willing partners)
- ML engineers and educators to join the core team
- Funding partners (see [Funding](#funding) section)
- Community contributors for language datasets

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Funding](#funding)
- [License](#license)
- [Community](#community)

## 🏁 Quick Start

### For Developers

```bash
# Clone the repository
git clone https://github.com/[your-org]/aya-sa-education.git
cd aya-sa-education

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the Aya 23 model
python scripts/download_model.py

# Run local development server
python scripts/run_server.py
```

Visit `http://localhost:8000` to interact with the model.

### For Educators

See our [Educator's Guide](docs/educators-guide.md) for information on:
- How to use the system in your classroom
- Curriculum alignment details
- Assessment strategies
- Privacy and safety features

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Student/Teacher Interface                │
│                    (Web Browser / Mobile App)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      API Gateway                             │
│              (Authentication, Rate Limiting)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼───────┐ ┌────▼─────┐ ┌──────▼────────┐
│ Content Filter│ │   Aya 23  │ │   Monitoring  │
│  & Safety     │ │   (8B)    │ │  & Analytics  │
└───────────────┘ └───────────┘ └───────────────┘
                        │
                ┌───────┴────────┐
        ┌───────▼────────┐ ┌────▼────────┐
        │ Language Model  │ │ Vector DB   │
        │ (Fine-tuned)    │ │ (Curriculum)│
        └────────────────┘ └─────────────┘
```

**Key Components**:
- **Aya 23 (8B)**: Base multilingual model from Cohere for AI
- **Fine-tuning Layer**: South African curriculum and language adaptations
- **Safety Layer**: Content filtering for age-appropriate responses
- **Vector Database**: CAPS curriculum embeddings for context retrieval

See [docs/architecture.md](docs/architecture.md) for detailed technical documentation.

## 💻 Installation

### Prerequisites

- **Hardware**: 
  - Minimum: 16GB RAM, 8GB VRAM GPU (RTX 4060 or better)
  - Recommended: 32GB RAM, 12GB VRAM GPU (RTX 3060 or better)
- **Software**:
  - Ubuntu 24.04 LTS (or compatible Linux)
  - Python 3.11+
  - CUDA 12.1+ (for GPU acceleration)
  - Docker (optional, for containerized deployment)

### Detailed Installation

See [INSTALL.md](INSTALL.md) for complete installation instructions including:
- Cloud deployment (Google Cloud, AWS, Azure)
- On-premises school server setup
- Offline deployment configuration
- Docker containerization

## 📖 Usage

### Basic Query Example

```python
from sa_edu_llm import AyaEducator

# Initialize the model
educator = AyaEducator(language="en")

# Ask a curriculum question
response = educator.ask(
    "Explain photosynthesis for Grade 10 Life Sciences",
    grade=10,
    subject="Life Sciences"
)

print(response)
```

### Web Interface

Access the web interface at `http://localhost:8000` after starting the server.

Features:
- Language selection (English, Afrikaans, isiZulu)
- Grade and subject context
- Session history
- Teacher dashboard for monitoring student queries

## 🤝 Contributing

We welcome contributions from developers, educators, linguists, and anyone passionate about education in South Africa!

### How to Contribute

1. **Code Contributions**: See [CONTRIBUTING.md](CONTRIBUTING.md)
2. **Language Datasets**: See [datasets/README.md](datasets/README.md)
3. **Documentation**: Help improve our guides and translations
4. **Testing**: Use the system and report issues
5. **Curriculum Content**: Share CAPS-aligned Q&A examples

### Areas We Need Help

- [ ] isiZulu language fine-tuning data
- [ ] isiXhosa language fine-tuning data
- [ ] Grade 8-12 subject matter experts for content validation
- [ ] UI/UX design for improved student interface
- [ ] Teacher training materials and workshops
- [ ] Documentation translation

See our [Good First Issues](https://github.com/[your-org]/aya-sa-education/labels/good%20first%20issue) for newcomer-friendly tasks.

## 🗺️ Roadmap

### Phase 1: Foundation (Months 1-2) ✅ In Progress
- [x] GitHub repository setup
- [x] Base Aya 23 deployment
- [ ] Basic web interface
- [ ] Initial funding secured

### Phase 2: Language Adaptation (Months 3-4)
- [ ] isiZulu fine-tuning (10,000+ examples)
- [ ] CAPS curriculum embeddings
- [ ] Content safety filters
- [ ] Educator feedback system

### Phase 3: Pilot Deployment (Months 5-6)
- [ ] 2-3 pilot schools in Gauteng
- [ ] Teacher training program
- [ ] Usage analytics dashboard
- [ ] First research paper published

### Phase 4: Scale (Months 7-12)
- [ ] 10-15 schools across 2-3 provinces
- [ ] Afrikaans + isiXhosa support
- [ ] Offline operation capability
- [ ] Community of 20+ contributors

See [ROADMAP.md](ROADMAP.md) for detailed milestones and timelines.

## 💰 Funding

This project is currently seeking funding to support:
- Development team salaries (R300k-400k/year per engineer)
- Hardware for pilot schools (R20k per school)
- Teacher training programs
- Dataset creation and linguistic expertise
- Operational costs (cloud hosting, domain, etc.)

### Funding Partners We're Approaching

- **Shuttleworth Foundation** (open source + social impact)
- **Google.org** (AI for education grants)
- **Local CSI Programs** (Naspers, MTN, Standard Bank)

Interested in funding this work? Contact us at llm-funding@ncpd.org.za

### Budget Transparency

All funding received and expenses incurred are tracked publicly in [BUDGET.md](BUDGET.md).

## 📄 License

This project is licensed under the **Apache License 2.0** - see [LICENSE](LICENSE) for details.

Key points:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ⚠️ Must include license and copyright notice
- ⚠️ Must state significant changes

### Datasets

Individual datasets in `/datasets` may have different licenses (CC-BY-4.0, CC-BY-SA-4.0). See each dataset's README for specific terms.

### Model Weights

Fine-tuned model weights inherit the Apache 2.0 license from Aya 23. Our fine-tuning contributions are also Apache 2.0 licensed.

## 👥 Community

### Get Involved


- **Mailing List**: [Subscribe to updates](https://groups.google.com/g/ncpd-llm)
- **LinkedIn**: [Follow us](https://linkedin.com/company/NCPD-LLM)

### Related Projects

- [Aya Project](https://cohere.com/research/aya) - Original Aya multilingual model

### Governance

This project is governed by a steering committee with representatives from:
- Technical development
- Educational expertise
- Linguistic expertise
- Community representatives
- Funding partners (non-voting)

See [GOVERNANCE.md](GOVERNANCE.md) for our decision-making process.

## 📞 Contact

- **General Inquiries**: info-llm@ncpd.org.za
- **Technical Support**: support-llm@ncpd.org.za
- **Partnership Opportunities**: partnerships-llm@ncpd.org.za
- **Media Inquiries**: media-llm@sncpd.org.za

## 🙏 Acknowledgments

This project builds on the incredible work of:
- **Cohere for AI** for creating and open-sourcing Aya 23
- **Our contributors** who make this possible

Special thanks to educators, students and learners who pilot and provide feedback.

---

**Built with ❤️ for South African education**

*"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela*
