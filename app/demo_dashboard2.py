import streamlit as st
import requests
import time
import json

def status_icon(status):
    return {
        "running": "🟡",
        "completed": "🟢",
        "failed": "🔴"
    }.get(status, "⚪")

API_BASE = "http://fastapi:8000"

st.set_page_config(page_title="Sentinel AI Demo", layout="wide")
st.title("Sentinel AI — Incident Self Healing Demo")

# ── Submit Incident ────────────────────────────────────────────────
st.header("Submit Incident")

with st.form("incident_form"):
    service = st.text_input("Service Name", value="orders-service")
    severity = st.selectbox("Severity", ["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    description = st.text_area(
        "Incident Description",
        value="Orders API latency above 6 seconds, CPU at 95%, error rate 15%, logs showing database timeouts.",
        height=120
    )
    submitted = st.form_submit_button("Submit Incident")

if submitted:
    if not service or not description:
        st.error("Service name and description are required.")
    else:
        response = requests.post(
            f"{API_BASE}/incident",
            json={"service": service, "severity": severity, "description": description}
        )
        if response.status_code == 200:
            data = response.json()
            incident_id = data.get("incident_id")
            st.session_state["incident_id"] = incident_id
            st.success(f"Incident submitted — Incident ID: {incident_id}")
        else:
            st.error(f"API error {response.status_code}: {response.text}")

# ── Resolve execution_id from incident_id ─────────────────────────
if "incident_id" in st.session_state and "execution_id" not in st.session_state:
    incident_id = st.session_state["incident_id"]
    with st.spinner("Waiting for worker to start execution..."):
        for _ in range(20):  # wait up to 20 * 2s = 40 seconds
            res = requests.get(f"{API_BASE}/incident/{incident_id}/execution", timeout=5)
            if res.status_code == 200:
                data = res.json()
                execution_id = data.get("execution_id")
                if execution_id:
                    st.session_state["execution_id"] = execution_id
                    break
            time.sleep(2)
        else:
            st.error("Timed out waiting for worker to pick up the incident.")
            st.stop()

# ── Live Execution Tracking ────────────────────────────────────────
if "execution_id" in st.session_state:
    execution_id = st.session_state["execution_id"]
    st.header(f"Live Execution — `{execution_id}`")

    status_placeholder    = st.empty()
    incident_placeholder  = st.empty()
    diagnosis_placeholder = st.empty()
    plan_placeholder      = st.empty()
    results_placeholder   = st.empty()
    evaluation_placeholder= st.empty()
    thinking_placeholder  = st.empty()

    for poll in range(60):  # poll up to 60 times, 3s apart = 3 min max

        try:
            res = requests.get(f"{API_BASE}/execution/{execution_id}", timeout=5)
            state = res.json()
        except Exception as e:
            status_placeholder.warning(f"Waiting for execution to start... ({e})")
            time.sleep(3)
            continue

        if state.get("status") == "pending":
            status_placeholder.info("Execution queued — waiting for worker to pick up...")
            time.sleep(3)
            continue

        # ── Incident ──────────────────────────────────────────────
        with incident_placeholder.container():
            st.subheader("Incident")
            incident = state.get("incident", {})
            col1, col2 = st.columns(2)
            col1.metric("Service",  service)
            col2.metric("Severity", severity)
            st.write(incident.get("description", ""))

        # ── Diagnosis ─────────────────────────────────────────────
        diagnosis = state.get("diagnosis")
        if diagnosis:
            with diagnosis_placeholder.container():
                st.subheader("Diagnosis")
                col1, col2 = st.columns(2)
                col1.metric("Confidence",     diagnosis.get("confidence", "—"))
                col2.write(f"**Cause:** {diagnosis.get('probable_cause', '—')}")
                st.write(diagnosis.get("reasoning", ""))

        # ── Plan ──────────────────────────────────────────────────
        plan = state.get("plan")
        # Remove this line entirely
        # from app.core.dag import compute_levels

        # Replace the levels block in the plan section with:
        if plan:
            with plan_placeholder.container():
                st.subheader("🧭 Execution DAG")

                plan = state.get("plan", {})
                edges = plan.get("edges", [])

                if edges:
                    graph = "digraph {\n"
                    for edge in edges:
                        graph += f'"{edge[0]}" -> "{edge[1]}";\n'
                    graph += "}"

                    st.graphviz_chart(graph)

                # fetch levels from API
                lvl_res = requests.get(f"{API_BASE}/execution/{execution_id}/levels", timeout=5)
                if lvl_res.status_code == 200:
                    levels = lvl_res.json().get("levels", [])
                    st.subheader("📊 Execution Flow (Levels)")
                    if levels:
                        cols = st.columns(len(levels))

                        for i, level in enumerate(levels):
                            with cols[i]:
                                st.markdown(f"**Level {i+1}**")
                                for step in level:
                                    st.write(f"🔹 {step}")

        # ── Live Step Results ─────────────────────────────────────
        response = requests.get(f"{API_BASE}/execution/{execution_id}/live_results", timeout=5)
        state = response.json()
        
        live_results = state.get("live_results", [])
        
        if live_results:
            with results_placeholder.container():
                st.subheader(f"Task Results — {len(live_results)} completed")
                for item in live_results:
                    
                    step = item.get("step")
                    status = item.get("status")
                    result = item.get("result")

                    icon = status_icon(status)

                    with st.expander(f"{icon} {step} ", expanded=False):
                        st.write(f"Status: {status}")
                        st.json(result)

        # ── Evaluation ────────────────────────────────────────────
        evaluation = state.get("evaluation")
        if evaluation:
            with evaluation_placeholder.container():
                st.subheader("Evaluation")
                col1, col2 = st.columns(2)
                col1.metric("Resolved",   str(evaluation.get("resolved",   "—")))
                col2.metric("Confidence", str(evaluation.get("confidence", "—")))
                st.write(evaluation.get("recommendation", ""))

            status_placeholder.success("Execution Complete")
            break

        # ── AI Thinking Panel ────────────────────────────────────────────


        response = requests.get(f"{API_BASE}/execution/{execution_id}/thinking")
        data = response.json()

        thinking = data.get("thinking", [])
        if thinking:
            with thinking_placeholder.container():
                st.subheader("🧠 AI Thinking Panel")

                for t in thinking:

                    agent = t.get("agent", "unknown")
                    step = t.get("step", "")
                    decision = t.get("decision", "")

                    with st.expander(f"🤖 {agent.upper()} → {step}"):

                        if "input" in t:
                            st.markdown("**Input:**")
                            st.json(t["input"])

                        if "retrieved_context" in t:
                            st.markdown("**Retrieved Context:**")
                            st.json(t["retrieved_context"])

                        if decision:
                            st.markdown("**Decision:**")
                            st.write(decision)

                        if "output" in t:
                            st.markdown("**Output:**")
                            st.json(t["output"])

                        if "confidence" in t:
                            st.metric("Confidence", t["confidence"])

        status_placeholder.info(f"Running... poll {poll + 1}/60")
        time.sleep(3)