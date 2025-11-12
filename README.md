# 🧠 RAGKit API

> A lightweight API wrapper around the [`ragkit-flow`](https://test.pypi.org/project/ragkit-flow/) framework — exposing composable, inspectable RAG pipelines as simple HTTP endpoints.

---

## 🚀 Overview

**RAGKit API** provides a minimal web layer for running and comparing prebuilt RAG pipelines built with [`ragkit-flow`](https://test.pypi.org/project/ragkit-flow/).

It’s designed for demonstrations, prototyping, and interactive exploration of retrieval-augmented generation (RAG) systems before deploying to scalable infrastructure (e.g. AWS EC2 / ECS).

This API currently focuses on a few core example pipelines, with support for:

- 🔍 **Multiple vector databases** (e.g. D&D, Business, Research)
- ⚙️ **Custom routing and augmentation blocks**
- 🧱 **Composable pipelines** using the same underlying RAGKit framework
- 🧩 **Simple RESTful endpoints** for easy web integration

---

## 🧪 Architecture

```
Next.js frontend  →  FastAPI / RAGKit API  →  RAGKit Pipelines  →  VectorDBs (Chroma)
```

Each RAG pipeline is defined internally and can be called via HTTP routes like:

| Endpoint               | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `POST /query/dnd`      | Query the Dungeons & Dragons knowledge base       |
| `POST /query/business` | Query the business intelligence dataset           |
| `POST /query/custom`   | Query a custom or experimental collection         |
| `GET /pipelines`       | List available pipelines and their configurations |

---

## ⚙️ Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourname/ragkit-api.git
cd ragkit-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Install the core RAGKit library

```bash
pip install -i https://test.pypi.org/simple/ ragkit-flow==0.1.0a7
```

### 3. Start the server

```bash
uvicorn main:app --reload
```

---

## 📡 Example Usage

### Query the D&D pipeline

```bash
curl -X POST http://127.0.0.1:8000/query/dnd \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the rules for fireball in 5e?"}'
```

**Response**

```json
{
  "query": "What are the rules for fireball in 5e?",
  "retrieved_docs": 3,
  "answer": "Fireball is a 3rd-level evocation spell..."
}
```

---

## 🧩 Example Pipeline Definition

Each route uses a preconfigured `RAGPipeline` from `ragkit-flow`:

```python
from ragkit import RAGPipeline, RetrieverBlock, GeneratorBlock, AugmentationBlock, HyDE
from openai import OpenAI

llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_dnd_pipeline():
    rag = RAGPipeline(
        name="dnd",
        llm_client=llm_client,
        client_model="gpt-4o-mini",
        collection_name="dnd",
        persist_directory="./chroma_db/dnd"
    )

    return (
        rag.add(AugmentationBlock, augmentations=[HyDE(llm_client=llm_client)])
           .add(RetrieverBlock, top_k=3)
           .add(GeneratorBlock)
    )
```

---

## 🗂️ Planned Pipelines

| Name       | VectorDB       | Description                                             |
| ---------- | -------------- | ------------------------------------------------------- |
| `dnd`      | Local Chroma   | Dungeons & Dragons knowledge base (fantasy + mechanics) |
| `business` | Local Chroma   | Microsoft Open Business Dataset (real-world data)       |
| `custom`   | Local / Remote | User-provided documents for flexible demos              |

---

## 🧠 Future Roadmap

| Milestone                          | Description                                       |
| ---------------------------------- | ------------------------------------------------- |
| ☁️ **Deployable Mode**             | Host RAGKit API and vector DBs on AWS EC2         |
| 📊 **Playground Dashboard**        | Frontend for visualizing pipeline steps and logs  |
| 🧩 **Dynamic Routing API**         | Allow runtime creation and selection of pipelines |
| 🧱 **Persistent Index Management** | Upload and index new documents through API        |

---

## 🤖 Development Notes

- Each pipeline is defined in `/pipelines/` and imported in `main.py`.
- VectorDBs (Chroma collections) are stored under `/data/chroma_db/`.
- This repo is focused on _read-only inference and retrieval demos_ — not live indexing.
- All heavy lifting (augmentation, retrieval, generation) is handled by `ragkit-flow`.

---

## 📜 License

MIT © 2025 [Your Name]

---

## ❤️ Acknowledgements

Built on top of [RAGKit Flow](https://test.pypi.org/project/ragkit-flow/) — a composable and inspectable framework for retrieval-augmented generation pipelines.

---
