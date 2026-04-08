# 🚀 Customer Support RL Agent (OpenEnv Hackathon)

## 🧠 Overview

This project implements a reinforcement learning-based customer support agent using the OpenEnv framework. The system simulates real-world customer support scenarios and trains an intelligent agent to classify queries, assign priorities, and generate helpful responses.

The agent combines:

* Rule-based reasoning
* GRPO-style candidate evaluation
* LLM-based response generation (OpenAI API)
* Smart fallback system for reliability

---

## 🎯 Problem Addressed

Customer support systems must:

* Understand user intent
* Assign urgency (priority)
* Provide accurate and helpful responses

This project builds a realistic environment to train and evaluate such an agent.

---

## ⚙️ Environment Design

### Observation Space

```json
{
  "customer_query": "string"
}
```

### Action Space

```json
{
  "category": "billing | technical | general",
  "priority": "low | medium | high",
  "response": "string"
}
```

### Reward Function

* ✅ Correct classification → +0.4
* ✅ Correct priority → +0.3
* ✅ Helpful response → +0.3
* ❌ Irrelevant response → penalty

---

## 🧪 Tasks

### 1️⃣ Easy

Simple queries (e.g., password reset)

### 2️⃣ Medium

Multi-intent queries (e.g., billing + issue)

### 3️⃣ Hard

Ambiguous or emotional queries (e.g., complaints)

---

## 🤖 Agent Architecture

```text
Query → Classification → LLM / Fallback → Action → Reward
```

### Components:

* Rule Engine → category + priority
* OpenAI LLM → response generation
* Fallback System → ensures robustness
* RL Loop → improves behavior

---

## 🔥 Key Features

* ✅ GRPO-style candidate selection
* ✅ Dataset generation pipeline
* ✅ Fine-tuning support (TinyLlama)
* ✅ OpenAI API integration (required)
* ✅ Deterministic fallback system
* ✅ Clean logging format (OpenEnv compliant)

---

## 📊 Baseline Performance

| Metric       | Score     |
| ------------ | --------- |
| Avg Reward   | 0.6 – 0.7 |
| Success Rate | High      |
| Stability    | High      |

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python inference.py
```

---

## 🔑 Environment Variables

```bash
HF_TOKEN=your_api_key
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
```

---

## 🧠 Design Choices

* Hybrid system ensures performance even without API access
* Rule-based classification improves reward stability
* LLM improves natural language quality
* Fallback ensures reliability under failures

---

## 🏁 Conclusion

This project demonstrates a scalable approach to building intelligent agents for real-world customer support using reinforcement learning and LLMs.

---
