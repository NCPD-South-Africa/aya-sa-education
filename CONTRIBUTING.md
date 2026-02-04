# Contributing to SA Edu LLM

Thank you for your interest in contributing! This document provides guidelines for contributors.

## 🤝 How to Contribute

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly  
5. Submit a pull request

## 📝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on what's best for students
- Give constructive feedback

## 🔧 Development Setup

```bash
git clone https://github.com/YOUR-USERNAME/aya-sa-education.git
cd aya-sa-education
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

## 💻 Coding Standards

- Follow PEP 8 (Python style guide)
- Use type hints
- Write docstrings for functions
- Keep functions under 50 lines
- Write tests for new features

## 📦 Areas We Need Help

### High Priority
- [ ] isiZulu language datasets
- [ ] isiXhosa language datasets
- [ ] CAPS curriculum Q&A pairs
- [ ] Web interface improvements
- [ ] Documentation translation

### Medium Priority
- [ ] API enhancements
- [ ] Performance optimization
- [ ] Teacher training materials

## ✅ Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

## 🐛 Reporting Bugs

Use GitHub Issues with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## 💡 Suggesting Features

Open an issue with:
- Feature description
- Use case / benefit
- Implementation ideas (optional)

## 📚 More Information

- [Dataset Guidelines](datasets/README.md)
- [Architecture Docs](docs/architecture.md)
- [Installation Guide](INSTALL.md)

Thank you for contributing to South African education! 🇿🇦
