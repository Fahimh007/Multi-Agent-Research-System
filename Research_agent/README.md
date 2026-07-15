# 🦙 DeepSearch AI: Multi-Agent Research Assistant

> **DeepSearch AI** is a cutting-edge web research assistant built with Django, LangGraph, LangChain, and OpenAI's GPT-4o-mini. It features a **collaborative multi-agent system** that automates the entire research workflow: from smart web searching and content extraction to structured report writing and critical evaluation.

## 🌟 Key Features

### 🔹 Multi-Agent Architecture
- **Search Agent**: Uses **Tavily** for intelligent web searches and source discovery
- **Reader Agent**: Extracts comprehensive content from URLs using **Scrapegraph-python**
- **Writer Agent**: Generates professional, well-structured research reports
- **Critic Agent**: Evaluates reports for accuracy, depth, clarity, and structure

### 🔹 Powered by Next-Gen AI
- **Language Model**: 🚀 **OpenAI GPT-4o-mini** (fast, accurate, and cost-effective)
- **Web Search**: 🔍 **Tavily AI** for semantic search with real-time web results
- **Web Scraping**: 🕸️ **Scrapegraph-python** for intelligent HTML parsing
- **Orchestration**: 🧩 **LangGraph** for seamless multi-agent workflows
- **Framework**: 🏗️ **Django 5.x** for robust web application development

### 🔹 Intelligent Research Workflow
1. **Search**: Find relevant sources using AI-powered keyword expansion
2. **Read**: Extract full content from multiple web pages
3. **Synthesize**: Automatically generate comprehensive reports
4. **Evaluate**: Get AI-powered feedback and quality scoring
5. **Iterate**: Refine and improve with agent collaboration

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)
- OpenAI API key
- Tavily API key

### Installation

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install django langchain langchain-openrouter langchain-community tavily-python langchain-openai langgraph scrapegraph-python python-dotenv

# 3. Configure environment variables
cp .env.example .env
```

Edit the `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run Development Server

```bash
# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Access the application at: ➡️ **http://localhost:8000**

## 🛠️ Development

### Folder Structure

```
Research_agent/
├── myapp/                        # Django application
│   ├── agents/                   # Multi-agent system
│   │   ├── agents.py             # Agent definitions (Search, Reader, Writer, Critic)
│   │   └── __init__.py
│   ├── templates/                # Django templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── result.html
│   ├── tools/                    # LangChain tools
│   │   ├── tools.py              # Web search and scraping tools
│   │   └── __init__.py
│   └── views.py                  # Django views handling agent execution
├── Research_agent/               # Project settings
├── manage.py                     # Django management script
├── .env                          # Environment variables (not in git)
└── .env.example                  # Example environment file
```

### Agent Breakdown

#### Search Agent (`myapp/agents/agents.py`)
- Uses **Tavily** to find relevant web sources based on query
- AI-powered keyword expansion for better search results
- Returns list of relevant URLs

#### Reader Agent (`myapp/agents/agents.py`)
- Takes URLs from search agent
- Uses **Scrapegraph-python** to extract full content
- Handles multiple pages and combines results

#### Writer Chain (`myapp/agents/agents.py`)
- GPT-4o-mini based prompt engineering
- Structured output format with: Introduction, Findings, Conclusion, Sources
- Professional tone and clear organization

#### Critic Chain (`myapp/agents/agents.py`)
- Evaluates report quality based on:
  - Accuracy
  - Depth
  - Clarity
  - Structure
  - Source citation
- Provides overall score and constructive feedback

## 💻 Technology Stack

| Category | Technology | Description |
|----------|------------|-------------|
| **Web Framework** | Django 5.x | Production-ready web application |
| **Agent Orchestration** | LangGraph | Visual, stateful multi-agent workflows |
| **LLM Integration** | LangChain Core | Agent builders and tool integration |
| **Language Model** | OpenAI GPT-4o-mini | Advanced AI reasoning and generation |
| **Web Search** | Tavily AI | Semantic web search engine |
| **Web Scraping** | Scrapegraph-python | Intelligent HTML content extraction |
| **Environment** | Python 3.13 | Modern Python features |
| **Utilities** | dotenv | Environment variable management |

## 📝 Usage

1. Go to **http://localhost:8000**
2. Enter your research query (e.g., "What is artificial intelligence?")
3. Click **"Run DeepSearch"**
4. Watch the agents collaborate in real-time
5. View the generated report and evaluation

## 🧪 Testing

```bash
# Run Django tests
python manage.py test
```

## 📦 Deployment

For production deployment:

```bash
# Collect static files
python manage.py collectstatic

# Run production server (e.g., using Gunicorn)
gunicorn Research_agent.wsgi:application --bind [IP_ADDRESS]:8000
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect API terms of service.

---

**Made with ❤️ using Django, LangGraph, and OpenAI**