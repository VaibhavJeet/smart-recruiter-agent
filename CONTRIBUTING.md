# Contributing to Smart Recruiter Agent

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart-recruiter-agent.git
   cd smart-recruiter-agent
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/VaibhavJeet/smart-recruiter-agent.git
   ```

## Development Setup

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Frontend (Next.js)

```bash
cd frontend
npm install
```

### Environment Configuration

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

## Making Changes

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Adding New Features

### Adding a New LangChain Agent

1. Create agent in `backend/app/agents/`:
   ```python
   from langchain.agents import AgentExecutor
   from app.core.llm import get_llm

   class NewAgent:
       def __init__(self):
           self.llm = get_llm()

       async def run(self, input_data):
           pass
   ```

2. Register in `backend/app/agents/__init__.py`
3. Add tests in `backend/tests/agents/`

### Adding a New MCP Integration

1. Create integration in `backend/app/mcp/`:
   ```python
   from app.mcp.base import BaseMCPIntegration

   class NewIntegration(BaseMCPIntegration):
       name = "new_integration"

       async def connect(self):
           pass

       async def execute(self, action, params):
           pass
   ```

2. Add configuration in `config/mcp.yaml`
3. Document usage in README

## Testing

### Backend
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

### Linting
```bash
# Backend
cd backend
ruff check .
ruff format .
mypy app

# Frontend
cd frontend
npm run lint
```

## Pull Request Process

1. Update your fork with upstream changes
2. Create a feature branch
3. Make changes and commit
4. Push to your fork
5. Create a Pull Request

### PR Requirements

- [ ] Tests pass
- [ ] Linting passes
- [ ] Documentation updated
- [ ] PR description explains changes

## Questions?

Open a [GitHub Issue](https://github.com/VaibhavJeet/smart-recruiter-agent/issues)