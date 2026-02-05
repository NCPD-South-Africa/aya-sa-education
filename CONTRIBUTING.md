# Contributing to SA Edu LLM

Thank you for your interest in contributing to the South African Educational LLM project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. We are committed to providing a welcoming and inclusive experience for everyone.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, education, socio-economic status
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behaviors include:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community and students
- Showing empathy towards other community members

**Unacceptable behaviors include:**
- Harassment, trolling, or derogatory comments
- Publishing others' private information without permission
- Any conduct which could reasonably be considered inappropriate in a professional setting

## How Can I Contribute?

### 1. Code Contributions

We welcome code contributions in these areas:
- Model fine-tuning scripts and improvements
- Web interface enhancements
- API development
- Performance optimizations
- Bug fixes
- Test coverage improvements

### 2. Language & Dataset Contributions

**High Priority:**
- isiZulu instruction-response pairs
- isiXhosa instruction-response pairs
- CAPS curriculum question-answer pairs (all subjects, Grades 8-12)
- Translation of existing English datasets

**See [datasets/README.md](datasets/README.md) for dataset contribution guidelines.**

### 3. Documentation

Help us improve:
- User guides and tutorials
- API documentation
- Translation of docs into South African languages
- Video tutorials for teachers

### 4. Testing & Quality Assurance

- Test the system in real classroom environments
- Report bugs and usability issues
- Suggest feature improvements
- Validate model responses for accuracy and appropriateness

### 5. Community Building

- Answer questions in GitHub Issues and Discord
- Write blog posts or create content about the project
- Present at conferences or meetups
- Help onboard new contributors

## Getting Started

### Prerequisites

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/sa-edu-llm.git
   cd sa-edu-llm
   ```

3. **Set up your development environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/[org-name]/sa-edu-llm.git
   ```

### Development Setup

Run tests to ensure everything is working:
```bash
pytest tests/
```

Start the development server:
```bash
python scripts/run_server.py --dev
```

## Development Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following our coding standards (see below)

3. **Test your changes**:
   ```bash
   # Run all tests
   pytest tests/
   
   # Run specific test file
   pytest tests/test_model.py
   
   # Run with coverage
   pytest --cov=sa_edu_llm tests/
   ```

4. **Commit your changes** (see commit guidelines below)

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:
- Line length: 100 characters (not 79)
- Use double quotes for strings (unless single quotes avoid escaping)
- Use type hints for function signatures

**Code formatting tools (automatically run by pre-commit):**
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting
- `mypy` for type checking

### Code Organization

```
sa_edu_llm/
├── models/          # Model loading, inference, fine-tuning
├── api/             # FastAPI application and routes
├── training/        # Training scripts and utilities
├── data/            # Data processing and loading
├── safety/          # Content filtering and moderation
├── evaluation/      # Model evaluation and benchmarking
└── utils/           # Shared utilities
```

### Writing Good Code

**DO:**
- Write clear, self-documenting code
- Add docstrings to all functions and classes
- Include type hints
- Write unit tests for new functionality
- Keep functions small and focused (< 50 lines ideal)
- Use meaningful variable names

**DON'T:**
- Commit commented-out code
- Leave TODO comments without creating an issue
- Mix unrelated changes in a single commit
- Skip writing tests for new features

### Example Function

```python
from typing import List, Optional

def generate_response(
    query: str,
    language: str = "en",
    grade: Optional[int] = None,
    subject: Optional[str] = None,
) -> str:
    """
    Generate an educational response to a student query.
    
    Args:
        query: The student's question or prompt
        language: ISO 639-1 language code (en, zu, xh, af)
        grade: Student's grade level (8-12)
        subject: Subject area (e.g., "Mathematics", "Life Sciences")
    
    Returns:
        Generated response text in the requested language
    
    Raises:
        ValueError: If language is not supported
        
    Example:
        >>> response = generate_response(
        ...     "What is photosynthesis?",
        ...     language="en",
        ...     grade=10,
        ...     subject="Life Sciences"
        ... )
    """
    # Implementation here
    pass
```

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates

### Examples

```
feat(model): add isiZulu language support

Implement fine-tuning pipeline for isiZulu dataset.
Includes 10,000 instruction-response pairs from CAPS curriculum.

Closes #42
```

```
fix(api): correct authentication token validation

Token expiry was not being checked correctly, allowing
expired tokens to pass validation.

Fixes #123
```

```
docs(readme): update installation instructions

Add Docker installation option and troubleshooting section.
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines and passes linting
- [ ] All tests pass (`pytest tests/`)
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] Commit messages follow guidelines

### PR Description Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass

## Related Issues
Closes #(issue number)
```

### Review Process

1. At least one maintainer must approve the PR
2. All CI checks must pass
3. Conversations must be resolved
4. Branch must be up-to-date with main

### After Approval

Your PR will be merged by a maintainer. The branch will be automatically deleted after merge.

## Dataset Contributions

See [datasets/README.md](datasets/README.md) for detailed guidelines on:
- Data format requirements
- Licensing requirements
- Quality standards
- Submission process

### Quick Dataset Contribution Guide

1. Ensure your data is properly licensed (CC-BY-SA-4.0 preferred)
2. Format as JSONL with required fields
3. Include metadata (language, grade level, subject)
4. Submit via PR to `datasets/raw/`
5. Maintainers will review and process

## Questions?

- **GitHub Issues**: For bugs and feature requests
- **Discord**: For general questions and discussion
- **Email**: dev@sa-edu-llm.org for private inquiries

## Recognition

Contributors are recognized in:
- README.md Contributors section
- CONTRIBUTORS.md (all contributors listed)
- Release notes (for significant contributions)

Thank you for contributing to education in South Africa! 🇿🇦
