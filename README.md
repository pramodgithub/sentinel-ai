🚨 Sentinel AI — Autonomous Incident Response System

An AI-powered SRE Co-pilot system that detects, diagnoses, plans, executes, and evaluates incident resolution workflows using agentic architecture.

⸻

🔥 Overview

Sentinel AI simulates a real-world production incident response system powered by LLM agents and orchestration.

It mimics how modern SRE teams operate:

Incident → Diagnosis → Planning → Execution → Evaluation → Learning

The system is designed to be:
	•	Autonomous (closed-loop decision making)
	•	Observable (metrics, cost, latency tracked)
	•	Auditable (full reasoning + execution trace)
	•	Extensible (plug into real infra like Kubernetes, AWS)

⸻

🧠 Key Features

🤖 Multi-Agent Architecture
	•	Diagnosis Agent → identifies root cause
	•	Planner Agent → generates execution DAG
	•	Executor Agent → runs tools/actions
	•	Evaluator Agent → scores outcome & decides next step
	•	Memory Agent → retrieves similar past incidents
	•	Risk Agent → enforces guardrails
	•	Learning Agent → improves future decisions

⸻

⚙️ Intelligent Execution Engine
	•	DAG-based execution planning
	•	Parallel diagnostics + sequential remediation
	•	Retry & fallback strategies
	•	Tool abstraction layer (infra-agnostic)

⸻

🧰 Tooling System (Simulated + Extensible)

Supports real-world SRE actions:
	•	check_logs
	•	inspect_metrics
	•	restart_container
	•	monitor_service
	•	check_health_endpoint
	•	scale_service
	•	clear_cache
	•	rollback_deployment
	•	alert_human
	•	close_incident

Each tool produces:
	•	stochastic outputs (realistic noise)
	•	confidence scores
	•	recommended next actions
##Tools screenshot
<p align="center">
  <img src="assets/screenshots/task_results.png" alt="tasks" width="800"/>
  <br/>
  <em>Real-time task execution visualization dashboard</em>
</p>
⸻

🧠 Memory-Augmented Diagnosis
	•	Retrieves similar incidents using vector similarity
	•	Weighs past outcomes and relevance
	•	Improves diagnosis accuracy with experience

⸻

📊 Observability & Metrics

Tracks LLM and system-level metrics:
	•	total tokens used
	•	latency per agent
	•	cost per execution (estimated)
	•	success rate
	•	evaluation score

⸻

🔍 Evaluation Engine (Core Innovation)

Instead of binary success, system evaluates:
	•	issue resolution
	•	system stability
	•	action effectiveness
	•	efficiency
	•	confidence alignment

##Evaluation screenshot
<p align="center">
  <img src="assets/screenshots/evaluation_thinking_panel.png" alt="evaluation_thinking_panel" width="800"/>
  <br/>
  <em>Evaluation & AI Thinking Panel observabilty visualization dashboard</em>
</p>

📜 Full Audit & Traceability

Every execution is logged:
	•	agent decisions
	•	tool outputs
	•	reasoning trace
	•	evaluation outcome

Enables:
	•	replay
	•	debugging
	•	compliance audit

⸻

🖥️ Interactive Dashboard (Streamlit)

Real-time visualization of:
	•	execution DAG
	•	step-by-step agent flow
	•	tool outputs
	•	evaluation panel
	•	LLM usage (tokens, latency, cost)

⸻

🏗️ Architecture

                ┌────────────────────┐
                │   Streamlit UI     │
                └────────┬───────────┘
                         ↓
                ┌────────────────────┐
                │   FastAPI Backend  │
                └────────┬───────────┘
                         ↓
          ┌────────────────────────────────┐
          │      Orchestration Engine      │
          └────────────────────────────────┘
               ↓          ↓         ↓
            Diagnosis   Planner   Executor
               ↓          ↓         ↓
             Memory      DAG     Tool Layer
               ↓                    ↓
          Vector Store        Simulated / Real Infra
               ↓
          Redis State + Streams


🧱 Tech Stack
	•	Backend: FastAPI
	•	Workers: Celery
	•	State & Streaming: Redis (Streams + KV)
	•	LLM Integration: Multi-provider router
	•	UI: Streamlit
	•	Containerization: Docker

⸻

🚀 Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed on your machine
- [Git](https://git-scm.com/) installed

### Setup & Run

1. **Clone the repository**
```bash
   git clone 
   cd 
```

2. **Start the project**
```bash
   docker compose up --build
```

3. **Run in background (optional)**
```bash
   docker compose up --build -d
```

4. **Stop the project**
```bash
   docker compose down
```

### Useful Commands
```bash
# View logs
docker compose logs -f

# View logs for a specific service
docker compose logs -f 

# Restart a specific service
docker compose restart 

# Rebuild a specific service
docker compose up --build 
```



🧪 Demo Scenarios

The system includes prebuilt incident simulations:
	•	High CPU Spike
	•	Service Down
	•	Memory Leak
	•	Error Rate Spike
	•	False Alert
	•	Restart Failure
	•	Performance Drift
	•	Cache Issue
	•	Bad Deployment
	•	High Risk Escalation

Each scenario:
	•	triggers different workflows
	•	tests different tools
	•	generates unique audit logs

⸻

🔐 Safety & Guardrails
	•	RBAC-ready tool execution
	•	human escalation for high-risk actions
	•	audit logging for all decisions
	•	no direct infra execution (agent-based model)

⸻

🧠 Design Principles
	•	Tool Abstraction: decouple decision from execution
	•	Closed Loop: evaluate → retry → adapt
	•	Memory-Driven Intelligence
	•	Explainability First
	•	Production Readiness (simulated)

⸻

🔮 Future Enhancements
	•	Kubernetes / AWS real integration
	•	multi-model comparison (GPT vs open models)
	•	advanced drift detection
	•	policy-based guardrails
	•	cost-aware planning

⸻

🎯 Why This Project Matters

This project demonstrates:
	•	agentic AI system design
	•	real-world SRE automation patterns
	•	LLM evaluation & observability
	•	scalable orchestration architecture

⸻

👨‍💻 Author

Built as part of advanced exploration into:
	•	AI systems design
	•	autonomous workflows
	•	production-grade LLM applications

⸻

⭐ If you find this useful

Give it a star ⭐ — or better, use it as inspiration to build something even more powerful.
:::

⸻