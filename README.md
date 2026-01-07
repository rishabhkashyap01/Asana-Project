# Asana RL Environment: High-Fidelity Seed Data Generator

## 📊 Project Overview
This repository contains a production-grade synthetic data engine designed to generate a "Work Graph" for Reinforcement Learning (RL) agents. The generator creates a relational SQLite database that simulates the complexity, hierarchy, and temporal patterns of a modern B2B SaaS organization.

## 🛠 Technical Architecture
The system is built using a modular orchestrator pattern, ensuring scalability and referential integrity across 5,000+ entities.

### Key Components:
- **Orchestrator (`main.py`):** Manages the simulation lifecycle and database initialization.
- **Semantic Engine (`llm_helper.py`):** Interfaces with **Llama-3.1-8b-instant** via Groq to provide context-aware task descriptions.
- **Relational Generators:** Discrete modules for Users, Teams, Projects, and Tasks.
- **Database Helper:** Optimized batch-insertion logic to handle high-volume data writes.



## 🧬 Data Methodology & Realism

### 1. Temporal Heuristics
Unlike simple random dating, this generator applies **Distribution Research** to ensure the environment is training-ready:
- **Due Date Patterns:** Utilizes a **Log-normal distribution** to mimic real-world sprint cycles where the majority of tasks are short-term (3-7 days) with a "long tail" of overdue items.
- **Logical Gating:** Enforces strict causality (e.g., $Created\_At < Completed\_At < Current\_Time$).

### 2. Semantic Consistency (LLM-Hybrid)
To satisfy the requirement for high-fidelity text, we utilize a hybrid approach:
- **Heuristic Seeds:** Core task names are derived from common patterns in professional issue trackers (Engineering vs. Marketing jargon).
- **LLM Enrichment:** The generator uses a "Top-k" strategy where the primary tasks of each project are enriched with Markdown-formatted descriptions via Llama 3.1, providing complex instructions for AI agents to parse.

### 3. Organizational Logic
- **Departmental Mapping:** Users are assigned to functional teams (Engineering, Sales, etc.), and projects are generated based on those departmental templates to ensure the "Work Graph" is semantically valid.



## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/) (Free Tier)

### Installation
1. Clone the repository and navigate to the directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

### Setup API key:
1. Copy .env.example to a new file named .env.
2. Open .env and paste your Groq API key.
3. The script will automatically load this via python-dotenv.