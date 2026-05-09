# Neurosymbolic Engine 🧠🧩

A high-performance **Neurosymbolic AI Pipeline Engine** designed to combine the intuitive, generative power of LLMs (Right Brain) with the logical, factual rigor of Knowledge Graphs (Left Brain).

## 🚀 The Hardware Metaphor Architecture
This engine is built on the philosophy of aligning AI cognitive components with modern computer hardware architecture:

- **GPU (Right Brain / LLM):** Uses Google Gemini (or any LLM) to process massive amounts of unstructured data in parallel, recognizing patterns and parsing natural language into structured JSON entities and relationships.
- **CPU (Left Brain / Neo4j Ontology):** Uses Neo4j as the strict logic processor and Single Source of Truth. It verifies the GPU's parsed logic against existing facts and permanently stores them without hallucination.
- **HBM (Working Memory / Port 5050):** A shared high-bandwidth memory layer that acts as a real-time bridge. It caches massive context and feeds it instantly into the GPU's context window, eliminating reasoning bottlenecks.

## ✨ Key Features
- **Zero Hallucination Fact-Checking:** Generative outputs are cross-referenced with Neo4j before being accepted.
- **Dynamic Entity Parsing:** Automatically extracts `Nodes` and `Edges` from raw text/PDFs.
- **Explainable AI (XAI):** Every decision or extracted fact is traceable via the Neo4j Graph View or Obsidian Knowledge Vault.

## 📦 Requirements
- Python 3.10+
- Neo4j Database (Local or AuraDB)
- Google Gemini API Key
- A Local Shared Memory Server (e.g., Port 5050 API)

## 💻 Usage

```python
from neurosymbolic_engine import NeurosymbolicEngine

engine = NeurosymbolicEngine()
text = "The 2026 hospital management strategy aims to maximize DSS accuracy to the level of human neural networks."

# Executes the full HBM -> GPU -> CPU -> HBM pipeline
engine.run_pipeline(text)
```

## 📜 License
MIT License
