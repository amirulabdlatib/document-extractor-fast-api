# Document Extractor FastAPI

A **100% RAG Privacy First (Retrieval-Augmented Generation) document extraction system** powered by **Ollama** for complete privacy-first document processing. This proof-of-concept architecture ensures **zero data exposure to third parties** by running entirely on your local infrastructure.

## 🔒 Privacy-First Architecture

**Complete Data Sovereignty:**
- ✅ DeepSeek LLM running locally via Ollama
- ✅ No external API calls for LLM inference
- ✅ Local vector database (Weaviate)
- ✅ Local observability (Langfuse)
- ✅ Zero data leakage to third parties
- ✅ Offline-capable operation

Perfect for enterprises, regulated industries, and sensitive document processing where data privacy is paramount.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Documents     │───▶│   ETL Pipeline   │───▶│   Weaviate DB   │
│   (pdf)       │    │   (Extract/      │    │   (Local)       │
└─────────────────┘    │   Transform/     │    └─────────────────┘
                       │   Load)          │              │
┌─────────────────┐    └──────────────────┘              │
│   FastAPI       │                                      │
│   Server        │◀─────────────────────────────────────┘
│   (Local)       │           RAG Pipeline
└─────────────────┘    ┌──────────────────┐
         │              │   Ollama +       │
         │              │   DeepSeek       │
         └─────────────▶│   (Local LLM)    │
                        └──────────────────┘
                        ┌──────────────────┐
                        │   Langfuse       │
                        │   Observability  │
                        │   (Local)        │
                        └──────────────────┘
