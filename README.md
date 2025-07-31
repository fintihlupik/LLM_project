
<img width="1584" height="396" alt="fondo README" src="https://github.com/user-attachments/assets/4cd9f1d1-f715-4452-8103-269f64cf03d8" />

<h1 align="center">LLM project</h1>

<p align="center">
  Financial agent for content generators • Dockerized • FastAPI + Gradio + Chroma DB
</p>

---

## 🧭 Table of Contents

- [📌 Project Overview](#-project-overview)
- [📎 Useful links](#-useful-links)
- [🎯 Target Audience](#-target-audience)
- [⚙️ General Project Overview](#️-general-project-overview)
- [🚀 Future features & Implementations](#-future-features--implementations)
- [🛠️ Tools & Technologies](#-tools--technologies)
- [🧪 Model Architecture](#-model-architecture)
- [📁 Project Structure](#-project-structure)
- [✍ Deployment Instructions](#-deployment-instructions)
- [👩 Contributors](#-contributors)

---

## 📌 Project Overview

<p align="justify">  

**FinancIA** is project is a modular financial AI assistant backend built with FastAPI and Gradio. It leverages a Chroma vector database for efficient semantic search and integrates multiple APIs, including Groq for language modeling and Stability AI for image generation. The system features specialized agents handling stock market data retrieval, academic research via arXiv and PDF processing, and general knowledge queries.

Content generation adapts to multilingual and cultural nuances using libraries like spaCy, KeyBERT, Rake, DeepTranslator, and langdetect. The architecture is designed for extensibility, supporting financial educational content tailored by platform, language, and user demographics. Containerized with Docker, it separates frontend and backend deployments for scalability and maintainability.


## The platform supports:

- ### 📝 Dynamic Content Generation  
  Generate tailored educational content focused on finance for multiple social media platforms such as Instagram, Twitter, and LinkedIn. Content adapts by age group, language, regional dialects, and platform behavior to maximize relevance and engagement.

- ### 💼 Specialized Financial Agent
  An agent with four distinct strategies (Yahoo Finance, standard queries, simple RAG, and combined approach) delivering expert-level financial insights and contextual reasoning.

- ### 📚 Retrieval-Augmented Generation (RAG) with Academic Focus
  Perform deep, context-aware responses by retrieving and indexing economic research papers (PDFs from arXiv) in Chroma. Uses keyword extraction (KeyBERT, Rake, spaCy), translation (DeepTranslator), and LM prompting for rich, grounded answers.

- ### 📈 Real-Time Financial Data Analysis  
  Integrates Yahoo Finance API to extract detailed technical data, company summaries, and links for stocks and indices, enabling timely and accurate financial analysis

- ### 🎨 AI-Powered Image Creation  
  Converts text prompts into photorealistic images using Stability AI, enhancing visual storytelling for financial content.

- ### 🎯 Audience Segmentation  
  Tailor content to specific **demographics** — including **age group**, **language**, and **geographical region** — to maximize **relevance** and **engagement**.


- ### 🌎 Multilingual and Culturally Aware Content Segmentation
Supports dynamic content adaptation for multiple languages and cultural nuances, improving user engagement across demographics.

---
## 📎 Useful links

- WebSite

  
- Documentation
  
  
- Presentation
  
  https://www.canva.com/design/DAGt-gyFBvA/4lWmKpnn3wpufBr-Bo2log/edit?utm_content=DAGt-gyFBvA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
---

## 🎯 Target Audience

- **Content creators**
- **Community manager**
- **Social media manager**

---

## 🔧 General Project Overview

### Features
- FastAPI-based backend with modular structure
- Gradio frontend for demo/testing
- Multi-agent design for finance-related tasks
- ChromaDB for local vector search
- Prompt engineering tailored to platform, age, language, and cultural context
- Fully containerized (backend/frontend split)
- NLP pipeline using KeyBERT, RAKE, spaCy, and langdetect
- Multilingual translation via DeepTranslator (Google)
- Stable Diffusion API integration for realistic image generation


| ✅ Pros                                                             | ❌ Cons                                                                             |
|----------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Modular and clean backend design                                     | No persistent Chroma store (in-memory or local, not shared)                         |
| Covers diverse use cases: stock data, research, content, images      | No UI interactivity beyond Gradio input box                                         |
| Agents are task-specific and clearly isolated                        | No authentication, session tracking, or user history                                |
| Uses lightweight and fast vector store (Chroma)                      | Manual setup for spaCy/NLTK models (not auto-downloaded on build)                   |
| Multilingual and culturally adaptive content generation              | No monitoring, logging, or rate limiting                                            |


---

## 🌐 Routes & Agents

### Features
- `/query`: GROQ LM general-purpose agent
- `/yahoo`: Market data with historical and technical info from Yahoo Finance
- `/agent`: RAG search from Chroma (local knowledge base)
- `/content`: Academic agent using Arxiv and document-based RAG
- `/image`: Realistic image generation via Stability API


| ✅ Pros                                                                    | ❌ Cons                                                            |
|----------------------------------------------------------------------------|---------------------------------------------------------------------|
| Well-separated routes and logic per use case                               | GROQ agent is single-shot, lacks conversation memory                |
| Custom agent strategies: Yahoo, RAG, RAG+Arxiv, GROQ                       | No centralized prompt logging or feedback loop                      |
| Combined keyphrase extraction and translation pipeline for better recall   | Agents are manually selected; not dynamically adaptive              |
| Arxiv-based academic search supports real PDF embedding and indexing)      | Image generation has no style/theme configuration)                  |



---

## 🧠 Architecture & Services

### Features
- `services/`: Core business logic, prompt construction, LM connectors
- `tools/`: Scripts and helpers for PDF fetching, Yahoo parsing, post generation
- `utils/query_depth`: Automatically switches between shallow and deep agents
- `prompts/`: Modular prompt base by platform, age, language, region
- `agents/finance_agent.py`: Unified agent with strategy dispatching

| ✅ Pros                                                       | ❌ Cons                                                                        |
|---------------------------------------------------------------|---------------------------------------------------------------------------------|
| Clear separation between tools, services, and routes          | Prompt design is heuristic; not optimized via real user feedback                |
| Prompt builder is extensible and adaptable                    | No lifecycle management of vector store data (aging, deduplication, tagging)    |
| Query depth analysis introduces contextual strategy control   | Static agent strategy selection; lacks metrics or LLM guidance                  |
| Prompt modularity enables wide reuse across agents            |                                                                                  |



---

## 🚀 Future Features & Implementations

### Planned Improvements
- Add user-facing frontend with search history, filters, and summaries
- Implement agent registry system for pluggable strategy injection
- Add monitoring, logging, and error tracing for observability
- Switch to persistent Chroma (Postgres or S3-backed)
- Integrate memory or context chaining for conversational agents
- Use semantic scoring or retrieval confidence to refine RAG
- Automate download and build of required NLP models (spaCy/NLTK)
- Enable image generation prompts with template presets or styles
- Add multilingual UI for internationalization support
- Create scheduled background tasks (e.g. RSS feeds, economic updates)


---

## 🛠️ Tools & Technologies

### ⚙️ Backend

![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/-Pydantic-3c77ff?logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/-Uvicorn-000000?logo=uvicorn&logoColor=white)
![Starlette](https://img.shields.io/badge/-Starlette-1f61a0?logo=starlette&logoColor=white)

- Python async stack: `aiohttp`, `httpx`, `anyio`, `async-timeout`
- API routing & services: `FastAPI`, `Starlette`, `Uvicorn`
- Data validation & configuration: `pydantic`, `pydantic-settings`, `dataclasses-json`

### 🤖 LLM & NLP Stack

![LangChain](https://img.shields.io/badge/-LangChain-2f2f2f?logo=langchain&logoColor=white)
![SpaCy](https://img.shields.io/badge/-SpaCy-09a3d5?logo=spacy&logoColor=white)
![Transformers](https://img.shields.io/badge/-Transformers-ffcc00?logo=huggingface&logoColor=black)
![HuggingFace](https://img.shields.io/badge/-HuggingFace-D04D20?logo=huggingface&logoColor=white)

- LangChain ecosystem: `langchain`, `langchain-core`, `langchain-community`, `langchain-chroma`, `langchain-text-splitters`, `langchain-ollama`, `langchain-groq`
- Multilingual models: `spaCy`, `en-core-web-sm`, `es-core-news-sm`, `fr-core-news-sm`
- Embedding & tokenization: `transformers`, `tiktoken`, `tokenizers`, `sentence-transformers`, `sentencepiece`
- NLP utilities: `nltk`, `deep-translator`, `langdetect`, `keybert`, `rake-nltk`

### 📦 Vector Database & Data Processing

![ChromaDB](https://img.shields.io/badge/-ChromaDB-ffffff?logo=vector&logoColor=black)
![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white)

- Vector storage: `chromadb`, `pypika`, `peewee`
- Data manipulation: `pandas`, `numpy`, `scikit-learn`, `scipy`
- PDF and document processing: `pypdf`, `rake-nltk`, `pdf_fetcher`

### 🌐 Web UI & Interfaces

![Gradio](https://img.shields.io/badge/-Gradio-3d75c7?logo=gradio&logoColor=white)

- Frontend interface: `gradio`, `gradio-client`
- Async communication: `httpx-sse`, `safehttpx`

### 🐳 DevOps & Utilities

![Docker](https://img.shields.io/badge/-Docker-2496ed?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/-CI/CD-2088FF?logo=githubactions&logoColor=white)
![Dotenv](https://img.shields.io/badge/-dotenv-47736C?logo=python&logoColor=white)

- Containers & orchestration: `docker-compose`, `Dockerfile.backend`, `Dockerfile.frontend`
- Environment management: `.env`, `python-dotenv`
- Logging & monitoring: `loguru`, `coloredlogs`, `opentelemetry-*`, `posthog`

---

## 🧪 Model Architecture



<p align="center">
  <img src="" alt="Diagrama de Arquitectura del Sistema" width="700"/>
</p>

## 📁 Project Structure

```
📦 LLM_PROJECT  
├── 📁 client                  # Gradio frontend interface  
├── 📁 data                  
│   └── 📁 chroma_db          # Vector database storage  
├── 📁 server                 # Backend FastAPI application  
│   ├── 📁 agents             # Agent implementations (e.g., financial)  
│   ├── 📁 database           # DB management scripts and raw data  
│   ├── 📁 prompts            # Prompt templates organized by domain  
│   ├── 📁 routes             # API route definitions  
│   ├── 📁 services           # Core LLM and prompt handling logic  
│   ├── 📁 tools              # PDF/image/Yahoo tools  
│   └── 📁 utils              # Helper utilities   
│   ├── main.py                # Entrypoint to FastAPI app  
│
├── README.md                # Project overview  
├── requirements.txt         # Python dependencies  
├── .env                     # Environment variables (not tracked by Git)  
├── .gitignore               # Git ignore rules  
├── .dockerignore            # Docker ignore rules  
├── docker-compose.yml       # Docker orchestration  
├── Dockerfile.backend       # Docker build config for backend  
├── Dockerfile.frontend      # Docker build config for frontend  

```
---

## ✍ Deployment Instructions

📋 Prerequisites

Before you begin, make sure you have:

    Python 3.10
    Docker Desktop

🧪 1. Clone the repository

    git clone https://github.com/your-username/your-repo.git
    cd your-repo

🔐 2. Configure environment variables

Create a .env file in the project root and add your variables (e.g.):

    # Groq API Key for LLM access
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    
    # Stability AI API Key for image generation
    STABILITY_API_KEY="YOUR_STABILITY_API_KEY"
    
📦 3. Docker

    # Open Desktop Docker
    docker compose build
    docker compose up

    # To check if everything is going well
    Docker ps
    
    # To access to the front and back, you only have to click on the links you will see on the terminal


---
## 👩‍💻 Contributors
We are AI students with a heart and passion for building better solutions for real problems.
Feel free to explore, fork, or connect with us for ideas, feedback, or collaborations.


| Name                  | GitHub                                                                                                                   | LinkedIn                                                                                                                                             |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Yael Parra**        | [![GitHub](https://img.shields.io/badge/GitHub-10b981?logo=github&logoColor=white)](https://github.com/Yael-Parra)       | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yael-parra/)                   |
| **Polina Terekhova Pavlova**    | [![GitHub](https://img.shields.io/badge/GitHub-10b981?logo=github&logoColor=white)](https://github.com/fintihlupik)  | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/polina-terekhova-pavlova/)   |
| **Mariela Adimari**  | [![GitHub](https://img.shields.io/badge/GitHub-10b981?logo=github&logoColor=white)](https://github.com/marie-adi)           | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mariela-adimari/)             |
| **Abigail Masapanta Romero**        | [![GitHub](https://img.shields.io/badge/GitHub-10b981?logo=github&logoColor=white)](https://github.com/abbyenredes)  | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abigail-masapanta-romero/)    |
