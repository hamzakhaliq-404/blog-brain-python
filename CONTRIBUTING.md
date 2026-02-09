# Contributing to Blog Brain

Thank you for your interest in contributing to Blog Brain! This document provides guidelines for development and contributions.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Pull Request Process](#pull-request-process)
6. [Agent Development](#agent-development)

---

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Google Gemini API key
- Serper.dev API key

### Initial Setup

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/blog-brain-python
cd blog-brain-python

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run tests
pytest tests/ -v
```

---

## Project Structure

```
blog-brain-python/
├── agents/           # AI agent definitions
├── tasks/            # Task specifications
├── tools/            # Custom CrewAI tools
├── schemas/          # Pydantic models
├── utils/            # Helper functions
├── tests/            # Test suite
├── main.py           # FastAPI entry point
├── crew.py           # Orchestration logic
└── config.py         # Configuration
```

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

```python
# 1. Imports: Group in this order
import os  # Standard library
from typing import Dict  # Standard library types

from fastapi import FastAPI  # Third-party
from pydantic import BaseModel  # Third-party

from config import settings  # Local imports
from utils.logger import setup_logger  # Local imports

# 2. Type Hints: Always use
def process_content(topic: str, tone: str = "professional") -> Dict[str, any]:
    """Process content with type hints."""
    pass

# 3. Docstrings: Google style
def create_agent(name: str, role: str) -> Agent:
    """
    Create a CrewAI agent.

Args:
        name: Agent's name
        role: Agent's role description

    Returns:
        Configured CrewAI Agent instance
    """
    pass

# 4. Error Handling: Be explicit
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### Code Organization

1. **Functions**: Keep under 50 lines
2. **Classes**: Single responsibility principle
3. **Files**: One main class or related functions per file
4. **Constants**: UPPER_CASE at the module level

### Naming Conventions

```python
# Variables and functions: snake_case
user_input = "test"
def process_data(): pass

# Classes: PascalCase
class ContentGenerator: pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_TIMEOUT = 30

# Private: Leading underscore
def _internal_helper(): pass
```

---

## Testing

### Writing Tests

Use **pytest** with fixtures:

```python
# tests/test_example.py
import pytest
from your_module import your_function

@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"topic": "Test Topic", "tone": "professional"}

def test_your_function(sample_data):
    """Test with descriptive name."""
    result = your_function(**sample_data)
    assert result is not None
    assert result["status"] == "success"
```

### Test Coverage

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test agent/task interactions
- **API Tests**: Test endpoints with TestClient

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_tools.py -v

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_api.py::TestAPIEndpoints::test_health_check -v
```

### Test Checklist

Before submitting PR:
- [ ] All tests pass
- [ ] New features have tests
- [ ] Coverage maintained or improved
- [ ] No broken imports

---

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions

### 2. Make Changes

- Follow coding standards
- Write/update tests
- Update documentation
- Add docstrings

### 3. Test Locally

```bash
# Run tests
pytest tests/ -v

# Check code style (optional)
flake8 .

# Type checking (optional)
mypy .
```

### 4. Commit

```bash
git add .
git commit -m "feat: Add new feature description"
```

Commit message format:
```
<type>: <subject>

<body (optional)>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Formatting

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub with:
- Clear title and description
- Link to related issues
- Screenshots (if UI changes)
- Test results

### 6. Code Review

- Respond to feedback promptly
- Make requested changes
- Keep PR focused and small

---

## Agent Development

### Creating a New Agent

```python
# agents/your_agent.py
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from tools.your_tools import your_tool
import os

def create_your_agent() -> Agent:
    """
    Create Your Agent with specific role.
    
    Returns:
        Configured CrewAI Agent
    """
    # Set API key
    os.environ['GOOGLE_API_KEY'] = settings.gemini_api_key
    
    # Create LLM
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=0.5  # Adjust as needed
    )
    
    # Create agent
    agent = Agent(
        role="Your Agent Role",
        goal="What this agent aims to achieve",
        backstory="""
        Detailed background and personality.
        What makes this agent unique.
        """,
        tools=[your_tool],  # Optional
        llm=llm,
        verbose=True,
        allow_delegation=False  # Or True if needed
    )
    
    return agent
```

### Creating a New Task

```python
# tasks/your_task.py
from crewai import Task
from agents.your_agent import create_your_agent

def create_your_task(topic: str) -> Task:
    """
    Create task for your agent.
    
    Args:
        topic: The content topic
        
    Returns:
        Configured CrewAI Task
    """
    agent = create_your_agent()
    
    task = Task(
        description=f"""
        Clear instruction for the agent.
        Context: {topic}
        
        Requirements:
        1. First requirement
        2. Second requirement
        """,
        expected_output="""
        Exact format expected.
        Be very specific.
        """,
        agent=agent
    )
    
    return task
```

### Creating a New Tool

```python
# tools/your_tool.py
from crewai.tools import tool
import requests

@tool
def your_tool(query: str) -> dict:
    """
    Brief description of what the tool does.
    
    Args:
        query: Description of the input
        
    Returns:
        Dictionary with results
    """
    try:
        # Tool implementation
        result = perform_action(query)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## Documentation

### Docstring Format

Use Google style:

```python
def complex_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    One-line summary.
    
    Longer description if needed.
    Can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 10
        
    Returns:
        Dictionary containing:
            - key1 (str): Description
            - key2 (int): Description
            
    Raises:
        ValueError: When param1 is empty
        APIError: When API call fails
        
    Example:
        >>> result = complex_function("test", 20)
        >>> print(result["key1"])
        'test_processed'
    """
    pass
```

### Documentation Updates

When adding features:
1. Update `README.md` if user-facing
2. Update `API_GUIDE.md` for new endpoints
3. Update `DEPLOYMENT.md` for config changes
4. Add inline comments for complex logic

---

## Common Tasks

### Adding a New Endpoint

1. Define schema in `schemas/`
2. Add endpoint in `main.py`
3. Add tests in `tests/test_api.py`
4. Document in `API_GUIDE.md`

### Modifying Agent Behavior

1. Edit agent in `agents/`
2. Update task if needed in `tasks/`
3. Add tests
4. Update docstrings

### Adding Dependencies

1. Add to `requirements.txt`
2. Pin version: `package==1.2.3`
3. Document why added (comment or PR description)

---

## Questions?

- **Bug Reports**: Open GitHub issue with reproduction steps
- **Feature Requests**: Open GitHub issue with use case
- **Questions**: Check existing issues or start discussion

---

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn

---

**Thank you for contributing!** 🎉
