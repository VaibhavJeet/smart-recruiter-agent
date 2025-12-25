# Smart Recruiter Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)](https://langchain.com/)

An AI-powered recruitment agent that automates candidate screening, resume parsing, interview scheduling, and intelligent job-candidate matching. Built with LangChain, MCP (Model Context Protocol) integrations, and Next.js 15.

## Problem Statement

Modern recruitment teams face significant challenges:

- **Volume Overload**: Hundreds of applications per position make manual screening impractical
- **Inconsistent Evaluation**: Human bias and fatigue lead to inconsistent candidate assessment
- **Slow Response Times**: Delayed feedback frustrates candidates and loses top talent
- **Coordination Complexity**: Scheduling interviews across multiple stakeholders is time-consuming

## Solution

Smart Recruiter Agent provides an end-to-end AI-powered recruitment workflow:

1. **Resume Parsing & Analysis**: Extracts structured data from resumes (PDF, DOCX, TXT)
2. **Intelligent Screening**: Matches candidates against job requirements using semantic understanding
3. **Automated Outreach**: Generates personalized communication for candidates
4. **Interview Scheduling**: Coordinates availability and schedules interviews automatically
5. **Candidate Ranking**: Provides ranked shortlists with detailed match explanations

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Next.js 15 Frontend                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Dashboard │  │ Job Mgmt │  │Candidates│  │ Interview Queue  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │ REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                     FastAPI Backend                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   LangChain Agent Core                       ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  ││
│  │  │Resume Parser│  │Job Matcher  │  │Scheduler Agent      │  ││
│  │  │   Agent     │  │   Agent     │  │                     │  ││
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    MCP Integrations                          ││
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────────────────┐ ││
│  │  │Database│  │Calendar│  │  Slack │  │Email (SMTP/Gmail)  │ ││
│  │  │  MCP   │  │  MCP   │  │   MCP  │  │        MCP         │ ││
│  │  └────────┘  └────────┘  └────────┘  └────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Remote LLM │    │  Local LLM   │    │   Vector DB  │
│ (OpenAI/etc) │    │   (Ollama)   │    │  (ChromaDB)  │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Tech Stack

### Backend
- **Python 3.11+** - Modern Python with type hints
- **FastAPI** - High-performance async API framework
- **LangChain 0.3+** - Agent orchestration, chains, tools, memory
- **LangGraph** - Multi-agent workflow orchestration
- **ChromaDB** - Vector storage for semantic search
- **Pydantic** - Data validation and settings management

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first styling
- **Shadcn/UI** - Accessible component library
- **React Query** - Server state management

### MCP Integrations
- **Database MCP** - PostgreSQL/SQLite candidate storage
- **Calendar MCP** - Google Calendar/Outlook scheduling
- **Slack MCP** - Team notifications
- **Email MCP** - Candidate communication

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker (optional, for local services)

### 1. Clone the repository
```bash
git clone https://github.com/VaibhavJeet/smart-recruiter-agent.git
cd smart-recruiter-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Configuration

### LLM Configuration

The agent supports multiple LLM providers. Configure via environment variables:

#### OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

#### Anthropic Claude
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

#### Local LLM (Ollama)
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### MCP Integrations

Configure integrations in `config/mcp.yaml`:

```yaml
integrations:
  database:
    enabled: true
    provider: sqlite
    connection_string: ${DATABASE_URL}

  calendar:
    enabled: false
    provider: google
    credentials_path: ./credentials/google.json

  slack:
    enabled: false
    bot_token: ${SLACK_BOT_TOKEN}

  email:
    enabled: false
    provider: smtp
    host: ${SMTP_HOST}
```

## Project Structure

```
smart-recruiter-agent/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangChain agents
│   │   ├── chains/           # LangChain chains
│   │   ├── tools/            # Custom LangChain tools
│   │   ├── mcp/              # MCP integration handlers
│   │   ├── models/           # Pydantic models
│   │   ├── api/              # FastAPI routes
│   │   └── core/             # Configuration, LLM setup
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities
│   └── package.json
├── config/
│   └── mcp.yaml
├── docker-compose.yml
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## API Reference

### Candidates
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/candidates` | Upload and parse resume |
| GET | `/api/candidates` | List all candidates |
| GET | `/api/candidates/{id}` | Get candidate details |
| POST | `/api/candidates/{id}/match` | Match against job |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/jobs` | Create job posting |
| GET | `/api/jobs` | List all jobs |
| GET | `/api/jobs/{id}/candidates` | Get matched candidates |

### Interviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/interviews/schedule` | Schedule interview |
| GET | `/api/interviews` | List interviews |
| PATCH | `/api/interviews/{id}` | Update interview |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [LangChain](https://langchain.com) for the agent framework
- [Model Context Protocol](https://modelcontextprotocol.io) for integration standards
- [Anthropic](https://anthropic.com) for Claude and MCP specification
