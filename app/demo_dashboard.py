"""
Sentinel AI — Terminal Dashboard
Run with: streamlit run sentinel_dashboard.py
"""

import streamlit as st
import requests
import time
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SENTINEL//AI",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "http://fastapi:8000"

# ─── Terminal CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Share+Tech+Mono&display=swap');

  html, body, [class*="css"] {
    background-color: #080c10 !important;
    color: #f2f5f7 !important;
    font-family: 'JetBrains Mono', monospace !important;
  }
  .stApp { background-color: #080c10 !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1rem 1.4rem !important; max-width: 100% !important; }

  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: #0d1117; }
  ::-webkit-scrollbar-thumb { background: #22c55e55; border-radius: 2px; }

  /* ── Panels ── */
  .panel-blue {
    border: 1px solid #3b82f6;
    border-radius: 4px;
    background: #080c10;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 14px #3b82f622, inset 0 0 30px #3b82f606;
  }
  .panel-green {
    border: 1px solid #22c55e;
    border-radius: 4px;
    background: #080c10;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 14px #22c55e22, inset 0 0 30px #22c55e06;
  }
  .panel-amber {
    border: 1px solid #f59e0b;
    border-radius: 4px;
    background: #080c10;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 12px #f59e0b18;
  }
  .panel-red {
    border: 1px solid #ef4444;
    border-radius: 4px;
    background: #080c10;
    padding: 14px 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 12px #ef444422;
  }

  /* ── Panel Titles ── */
  .pt-blue  { font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:12px; padding-bottom:7px; color:#3b82f6; border-bottom:1px solid #3b82f630; }
  .pt-green { font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:12px; padding-bottom:7px; color:#22c55e; border-bottom:1px solid #22c55e30; }
  .pt-amber { font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:12px; padding-bottom:7px; color:#f59e0b; border-bottom:1px solid #f59e0b30; }
  .pt-red   { font-size:10px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:12px; padding-bottom:7px; color:#ef4444; border-bottom:1px solid #ef444430; }

  /* ── Status Bar ── */
  .status-bar {
    border: 1px solid #22c55e;
    border-radius: 4px;
    background: #080c10;
    padding: 9px 18px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 0 18px #22c55e28;
    font-size: 11px;
    color: #4ade80;
  }
  .sdot { display:inline-block; width:7px; height:7px; border-radius:50%; background:#22c55e; box-shadow:0 0 6px #22c55e; margin-right:5px; animation:pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }

  /* ── Severity Badge ── */
  .badge { display:inline-block; font-size:9px; font-weight:700; padding:2px 8px; border-radius:2px; letter-spacing:1.5px; }
  .bc { background:#450a0a; color:#f87171; border:1px solid #7f1d1d; }
  .bh { background:#431407; color:#fb923c; border:1px solid #7c2d12; }
  .bm { background:#422006; color:#fbbf24; border:1px solid #78350f; }
  .bl { background:#14532d; color:#4ade80; border:1px solid #166534; }

  /* ── Step Result Rows ── */
  .step-row { display:flex; align-items:center; padding:6px 0; border-bottom:1px solid #0f1923; font-size:11px; gap:10px; }
  .step-row:last-child { border-bottom:none; }
  .step-name { color:#f2f5f7; flex:1; }

  /* ── Progress Bar ── */
  .pb-wrap { margin-bottom:6px; }
  .pb-label { display:flex; justify-content:space-between; font-size:10px; color:#f2f5f7; margin-bottom:3px; }
  .pb-track { height:3px; background:#1f2937; border-radius:2px; overflow:hidden; }
  .pb-g { height:100%; background:#22c55e; border-radius:2px; }
  .pb-b { height:100%; background:#3b82f6; border-radius:2px; }
  .pb-a { height:100%; background:#f59e0b; border-radius:2px; }
  .pb-r { height:100%; background:#ef4444; border-radius:2px; }

  /* ── KV Rows ── */
  .kv { display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #0f1923; font-size:11px; }
  .kv:last-child { border-bottom:none; }
  .kk { color:#f2f5f7; letter-spacing:.5px; }
  .kv-g { color:#4ade80; font-size:15px; !important;}
  .kv-a { color:#fbbf24; font-size:15px; !important; }
  .kv-r { color:#f87171; font-size:15px; !important; }
  .kv-b { color:#60a5fa; font-size:15px; !important;}
  .kv-n { color:#f2f5f7; font-size:15px; !important;}

  /* ── Thinking ── */
  
        /* Hide the broken Material Icon text */
        [data-testid="stIconMaterial"] {
            display: none !important;
        }

        /* Add a CSS-based arrow to expander header instead */
        .st-emotion-cache-1c9yjad,
        details > summary::before {
            content: "▶" !important;
            font-family: inherit !important;
            margin-right: 8px;
        }

        /* Rotate arrow when expander is open */
        details[open] > summary::before {
            content: "▼" !important;
        }
           
  .think-dec { font-size:11px; color:#f2f5f7; line-height:1.6; border-left:2px solid #3b82f640; padding-left:10px; margin:6px 0; }

  /* ── DAG Level Pills ── */
  .lvl-pill { background:#0d1117; border:1px solid #3b82f640; border-radius:3px; padding:4px 8px; font-size:10px; color:#60a5fa; margin:3px 0; display:block; }
  .lvl-hdr  { font-size:9px; letter-spacing:2px; color:#3b82f6; margin-bottom:6px; text-transform:uppercase; }

  /* ── Streamlit widget overrides ── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div > div {
    background-color: #0d1117 !important;
    border: 1px solid #3b82f660 !important;
    border-radius: 4px !important;
    color:#f2f5f7; !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 8px #3b82f630 !important;
  }
  label, .stSelectbox label, .stTextInput label, .stTextArea label {
    color: #4b5563 !important;
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
  }
  .stFormSubmitButton > button, .stButton > button {
    background: #0a1a0d !important;
    border: 1px solid #22c55e !important;
    color: #4ade80 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    border-radius: 2px !important;
    padding: 7px 24px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
  }
  .stFormSubmitButton > button:hover, .stButton > button:hover {
    background: #22c55e22 !important;
    box-shadow: 0 0 12px #22c55e60 !important;
  }
  .stMetric { background: transparent !important; }
  .stMetric label { color:#4b5563 !important; font-size:9px !important; letter-spacing:1.5px !important; }
  .stMetric [data-testid="stMetricValue"] { color:#9ca3af !important; font-size:16px !important; font-family:'JetBrains Mono',monospace !important; }
  .stExpander { border:1px solid #1f2937 !important; border-radius:4px !important; background:#0a0f14 !important; }
  .stExpander summary { color:#f2f5f7 !important; font-size:11px !important; font-family:'JetBrains Mono',monospace !important; }
  .stAlert { background:#0a0f14 !important; border-radius:4px !important; font-family:'JetBrains Mono',monospace !important; font-size:11px !important; }
  .stSpinner > div { border-top-color:#22c55e !important; }
  p, div, span, li { font-family:'JetBrains Mono',monospace !important; font-size: 10px !important; }
  .stGraphViz svg { background:#080c10 !important; border-radius:4px; border:1px solid #1f2937; }
            
  [data-testid="stForm"], [data-testid="thinking_expanders"],[data-testid="task_expanders"] {
    background: transparent !important; border: 1px solid #3b82f6 !important; border-radius: 8px !important; padding: 0 !important; width: 98%; align-self: flex-end;    padding: 10px 16px !important;
    }  
 div[data-testid="stExpander"] details {
    background-color: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
}

/* the header row itself */
div[data-testid="stExpander"] details summary {
    background-color: transparent !important;
    color: var(--text-color) !important;
}

/* when open — summary gets a white bg by default */
div[data-testid="stExpander"] details[open] summary {
    background-color: rgba(255,255,255,0.05) !important;
    color: var(--text-color) !important;
}

/* the label text inside the header */
div[data-testid="stExpander"] details summary p,
div[data-testid="stExpander"] details summary span {
    color: #f2f5f7 !important;
    font-family: monospace !important;
    font-size: 11px !important;
}

/* expander body */
div[data-testid="stExpander"] details div[data-testid="stExpanderDetails"] {
    background-color: transparent !important;
}       
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────────
def severity_badge(s):
    cls = {"CRITICAL":"bc","HIGH":"bh","MEDIUM":"bm","LOW":"bl"}.get(s,"bl")
    return f'<span class="badge {cls}">{s}</span>'

def prog(label, pct, color="g"):
    c_txt = {"g":"#4ade80","b":"#60a5fa","a":"#fbbf24","r":"#f87171"}.get(color,"#4ade80")
    return f"""<div class="pb-wrap">
      <div class="pb-label"><span>{label}</span><span style="color:{c_txt}">{pct}%</span></div>
      <div class="pb-track"><div class="pb-{color}" style="width:{pct}%"></div></div>
    </div>"""

def quote_block(text, color="#22c55e"):
    return f'<div style="margin-top:10px;font-size:11px;color:#f2f5f7;line-height:1.6;border-left:2px solid {color}40;padding-left:10px">{text}</div>'


# ─── Status Bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-bar">
  <span><span class="sdot"></span> SENTINEL//AI ONLINE</span>
  <span style="color:#1f2937">│</span>
  <span>AI SRE Co-Pilot</span>
  <span style="color:#1f2937">│</span>
  <span style="color:#cad3e0">v1.1.0  ·  env: Development</span>
</div>
""", unsafe_allow_html=True)


# ─── Submit Incident ────────────────────────────────────────────────────────────
st.markdown('<div class="panel-blue"><div class="pt-blue">◈ SUBMIT INCIDENT</div>', unsafe_allow_html=True)

INCIDENT_SCENARIOS = {
    "High CPU Spike": {
        "service": "orders-service",
        "severity": "CRITICAL",
        "description": "Orders API latency above 6 seconds, CPU at 95%, error rate 15%, logs showing timeout errors."
    },
    "Service Down": {
        "service": "payment-service",
        "severity": "CRITICAL",
        "description": "Payment service is not responding, health endpoint failing, customers unable to complete transactions."
    },
    "Memory Leak Detected": {
        "service": "inventory-service",
        "severity": "HIGH",
        "description": "Memory usage steadily increasing to 90%, logs indicate possible memory leak, occasional restarts observed."
    },
    "Error Rate Spike": {
        "service": "checkout-service",
        "severity": "HIGH",
        "description": "Error rate increased to 20%, logs showing repeated null pointer exceptions."
    },
    "False Alert / No Issue": {
        "service": "catalog-service",
        "severity": "LOW",
        "description": "Temporary spike in logs but system metrics and health checks are normal."
    },
    "Restart Failure Scenario": {
        "service": "auth-service",
        "severity": "CRITICAL",
        "description": "Service crashed, restart attempts failing, logs show dependency issues."
    },
    "Gradual Performance Drift": {
        "service": "search-service",
        "severity": "MEDIUM",
        "description": "Latency gradually increasing over time, CPU and memory slightly elevated, no clear errors."
    },
    "Cache Issue": {
        "service": "recommendation-service",
        "severity": "MEDIUM",
        "description": "Users seeing stale data, cache not updating, response time inconsistent."
    },
    "Bad Deployment": {
        "service": "user-service",
        "severity": "HIGH",
        "description": "Recent deployment causing failures, logs show new version errors, rollback may be required."
    },
    "High Risk / Escalation Needed": {
        "service": "billing-service",
        "severity": "CRITICAL",
        "description": "Critical billing failures detected, inconsistent transaction records, requires human intervention."
    }
}
scenario = st.selectbox("Select Incident Scenario", list(INCIDENT_SCENARIOS.keys()))

selected = INCIDENT_SCENARIOS[scenario]
with st.form("incident_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        service = st.text_input("Service Name", value=selected["service"])

    with col2:
        severity = st.selectbox(
            "Severity",
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            index=["CRITICAL", "HIGH", "MEDIUM", "LOW"].index(selected["severity"])
        )

    description = st.text_area(
        "Incident Description",
        value=selected["description"],
        height=90,
    )
    submitted = st.form_submit_button("⟳  SUBMIT INCIDENT")

st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    if not service or not description:
        st.error("Service name and description are required.")
    else:
        try:
            response = requests.post(
                f"{API_BASE}/incident",
                json={"service": service, "severity": severity, "description": description}
            )
            if response.status_code == 200:
                incident_id = response.json().get("incident_id")
                st.session_state["incident_id"] = incident_id
                st.session_state.pop("execution_id", None)
                st.markdown(f"""
                <div class="panel-green">
                  <span style="color:#22c55e;font-size:11px">✓ INCIDENT QUEUED</span>
                  &nbsp;&nbsp;
                  <span style="color:#f2f5f7;font-size:10px">ID: {incident_id}</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.error(f"API error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")


# ─── Resolve execution_id ────────────────────────────────────────────────────────
if "incident_id" in st.session_state and "execution_id" not in st.session_state:
    incident_id = st.session_state["incident_id"]
    with st.spinner("Waiting for worker to pick up incident..."):
        for _ in range(20):
            try:
                res = requests.get(f"{API_BASE}/incident/{incident_id}/execution", timeout=5)
                if res.status_code == 200:
                    execution_id = res.json().get("execution_id")
                    if execution_id:
                        st.session_state["execution_id"] = execution_id
                        break
            except Exception:
                pass
            time.sleep(2)
        else:
            st.error("Timed out waiting for worker to pick up the incident.")
            st.stop()


# ─── Live Execution Tracking ─────────────────────────────────────────────────────
if "execution_id" in st.session_state:
    execution_id = st.session_state["execution_id"]

    st.markdown(f"""
    <div class="panel-green">
      <div class="pt-green">◈ LIVE EXECUTION</div>
      <div class="kv"><span class="kk">EXECUTION ID</span><span class="kv-b">{execution_id}</span></div>
    </div>""", unsafe_allow_html=True)

    status_ph    = st.empty()
    incident_ph  = st.empty()
    diag_ph      = st.empty()
    plan_ph      = st.empty()
    results_ph   = st.empty()
    col_eval, col_think = st.columns([2, 3])   # 40% / 60%
    with col_eval:
        eval_ph = st.empty()
    with col_think:
        thinking_ph = st.empty()

    live_state = {}

    for poll in range(60):
        # ── Fetch main state ─────────────────────────────────────
        try:
            res   = requests.get(f"{API_BASE}/execution/{execution_id}", timeout=5)
            state = res.json()
           # st.write(f"[debug] state: {state}")  # debug
        except Exception as e:
            status_ph.warning(f"Waiting for execution... ({e})")
            time.sleep(3)
            continue

        if state.get("status") == "pending":
            status_ph.info("Execution queued — waiting for worker...")
            time.sleep(3)
            continue
        
        
        # ── Status progress bar ──────────────────────────────────
        poll_pct = int((poll / 60) * 100)
        status_ph.markdown(
            f'<div class="panel-amber"><div class="pt-amber">◈ STATUS</div>'
            f'{prog("POLL PROGRESS", poll_pct, "a")}'
            f'<div style="font-size:10px;color:#4b5563;margin-top:4px">poll {poll+1}/60 · 3s interval</div></div>',
            unsafe_allow_html=True
        )

        # ── Incident details ─────────────────────────────────────
        incident    = state.get("incident", {})
        inc_service  = incident.get("service",     service)
        inc_severity = incident.get("severity",    severity)
        inc_desc     = incident.get("description", "")
        
        incident_ph.markdown(f"""
        <div class="panel-blue">
          <div class="pt-blue">◈ INCIDENT DETAILS</div>
          <div class="kv"><span class="kk">SCENARIO</span><span class="kv-b">{scenario}</span></div>
          <div class="kv"><span class="kk">SERVICE</span><span class="kv-b">{inc_service}</span></div>
          <div class="kv"><span class="kk">SEVERITY</span><span>{severity_badge(inc_severity)}</span></div>
          {quote_block(inc_desc, "#3b82f6")}
        </div>""", unsafe_allow_html=True)

        # ── Diagnosis ────────────────────────────────────────────
        diagnosis = state.get("diagnosis")
        if diagnosis:
            confidence = diagnosis.get("confidence", "—")
            cause      = diagnosis.get("probable_cause", "—")
            reasoning  = diagnosis.get("reasoning", "")
            try:
                conf_num   = float(str(confidence).replace("%",""))
                conf_cls   = "kv-g" if conf_num >= 70 else "kv-a"
            except Exception:
                conf_cls = "kv-n"
            diag_ph.markdown(f"""
            <div class="panel-green">
              <div class="pt-green">◈ DIAGNOSIS</div>
              <div class="kv"><span class="kk">CONFIDENCE</span><span class="{conf_cls}">{confidence}</span></div>
              <div class="kv"><span class="kk">PROBABLE CAUSE</span><span class="kv-n">{cause}</span></div>
              {quote_block(reasoning, "#22c55e")}
            </div>""", unsafe_allow_html=True)

        # ── DAG + Levels ─────────────────────────────────────────
        plan = state.get("plan")
        if plan:
            edges = plan.get("edges", [])
            with plan_ph.container():
                col_dag, col_lvl = st.columns([3, 2])
                with col_dag:
                    st.markdown('<div class="panel-blue"><div class="pt-blue">◈ EXECUTION DAG</div>', unsafe_allow_html=True)
                    if edges:
                        g = 'digraph {\n  bgcolor="#080c10"\n  node [style=filled fillcolor="#0d1117" color="#3b82f6" fontcolor="#9ca3af" fontname="monospace" fontsize=10]\n  edge [color="#3b82f660"]\n'
                        for edge in edges:
                            g += f'  "{edge[0]}" -> "{edge[1]}";\n'
                        g += "}"
                        st.graphviz_chart(g)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_lvl:
                    st.markdown('<div class="panel-blue"><div class="pt-blue">◈ EXECUTION LEVELS</div>', unsafe_allow_html=True)
                    try:
                        lvl_res = requests.get(f"{API_BASE}/execution/{execution_id}/levels", timeout=5)
                        if lvl_res.status_code == 200:
                            levels = lvl_res.json().get("levels", [])
                            for i, level in enumerate(levels):
                                st.markdown(f'<div class="lvl-hdr">LEVEL {i+1}</div>', unsafe_allow_html=True)
                                for step in level:
                                    st.markdown(f'<span class="lvl-pill">▸ {step}</span>', unsafe_allow_html=True)
                    except Exception:
                        pass
                    st.markdown('</div>', unsafe_allow_html=True)

        # ── Live Step Results ─────────────────────────────────────
        try:
            lr       = requests.get(f"{API_BASE}/execution/{execution_id}/live_results", timeout=5)
            live_state = lr.json()
            live_results = live_state.get("live_results", [])
        except Exception:
            live_results = []

        if live_results:
            total    = len(live_results)
            done_c   = sum(1 for r in live_results if r.get("status") == "completed")
            run_c    = sum(1 for r in live_results if r.get("status") == "running")
            fail_c   = sum(1 for r in live_results if r.get("status") == "failed")
            done_pct = int(done_c / total * 100) if total else 0

            rows_html = ""
            for item in live_results:
                s     = item.get("status", "")
                icons = {"completed":"✓","running":"◈","failed":"✗"}
                cols  = {"completed":"#4ade80","running":"#60a5fa","failed":"#f87171"}
                ic    = icons.get(s,"○")
                cc    = cols.get(s,"#6b7280")
                rows_html += (
                    f'<div class="step-row">'
                    f'<span style="color:{cc};font-size:13px">{ic}</span>'
                    f'<span class="step-name">{item.get("step","")}</span>'
                    f'<span style="color:{cc};font-size:9px;letter-spacing:1px">{s.upper()}</span>'
                    f'</div>'
                )

            with results_ph.container():
                st.markdown(f"""
                <div class="panel-green">
                  <div class="pt-green">◈ TASK RESULTS — {total} TASKS</div>
                  {prog("COMPLETION", done_pct, "g")}
                  <div style="display:flex;gap:16px;font-size:10px;margin-bottom:10px">
                    <span style="color:#4ade80">✓ {done_c} done</span>
                    <span style="color:#60a5fa">◈ {run_c} running</span>
                    <span style="color:#f87171">✗ {fail_c} failed</span>
                  </div>
                  {rows_html}
                </div>""", unsafe_allow_html=True)

                for item in live_results:
                    s  = item.get("status","")
                    ic = {
                            "completed": "✅",
                            "running":   "🔄",
                            "failed":    "❌"
                        }.get(s, "⭕")
                    with st.expander(f"{ic}  {item.get('step','')}  [{s.upper()}]", expanded=False):
                        if item.get("result"):
                            st.json(item["result"])

        # ── Evaluation ───────────────────────────────────────────
        evaluation = state.get("evaluation") or live_state.get("evaluation")

        if evaluation:
            execution_id = state.get("execution_id") or live_state.get("execution_id")

            # --- Evaluation fields ---
            resolved   = evaluation.get("resolved", "—")
            confidence = evaluation.get("confidence", "—")
            rec        = evaluation.get("recommendation", "")
            obsrvn     = evaluation.get("observations", "")
            status     = evaluation.get("status", "unknown")
            llm_usage = evaluation.get("llm_metrics", {})


            is_ok   = status == "resolved"
            is_warn = status == "partial"

            panel_cls = "panel-green" if is_ok else "panel-yellow" if is_warn else "panel-red"
            pt_cls    = "pt-green" if is_ok else "pt-yellow" if is_warn else "pt-red"
            border_c  = "#22c55e" if is_ok else "#eab308" if is_warn else "#ef4444"

            res_txt = "✓ RESOLVED" if is_ok else "⚠ PARTIAL" if is_warn else "✗ FAILED"
            res_cls = "kv-g" if is_ok else "kv-y" if is_warn else "kv-r"

           
            eval_ph.markdown(f"""
            <div class="{panel_cls}">
            <div class="{pt_cls}">◈ EVALUATION</div>

            <div class="kv">
                <span class="kk">STATUS</span>
                <span class="{res_cls}">{res_txt}</span>
            </div>

            <div class="kv">
                <span class="kk">CONFIDENCE</span>
                <span class="kv-n">{confidence}</span>
            </div>

            <div class="kv">
                <span class="kk">LLM CALLS</span>
                <span class="kv-n">{llm_usage.get("calls", 0)}</span>
            </div>

            <div class="kv">
                <span class="kk">INPUT TOKENS</span>
                <span class="kv-n">{llm_usage.get("input_tokens", 0)} | ${llm_usage.get("cost_input_tokens", 0):.6f}</span>
            </div>

            <div class="kv">
                <span class="kk">OUTPUT TOKENS</span>
                <span class="kv-n">{llm_usage.get("output_tokens", 0)} | ${llm_usage.get("cost_output_tokens", 0):.6f}</span>
            </div>

            <div class="kv">
                <span class="kk">AVG LATENCY</span>
                <span class="kv-n">{llm_usage.get("avg_latency", 0)} ms</span>
            </div>

            <div class="kv">
                <span class="kk">EST COST</span>
                <span class="kv-n">${llm_usage.get("cost", 0):.6f}</span>
            </div>

            {quote_block(obsrvn, border_c)}
            <div class="kv">
                <span class="kk">Recommendation</span>
                <span class="kv-n">{rec}</span>
            </div>
            </div>
            """, unsafe_allow_html=True)

            

        # ── AI Thinking Panel ─────────────────────────────────────
        try:
            tk_res  = requests.get(f"{API_BASE}/execution/{execution_id}/thinking", timeout=5)
            thinking = tk_res.json().get("thinking", [])
        except Exception:
            thinking = []

        if thinking:
            with thinking_ph.container():
                st.markdown('<div class="panel-blue"><div class="pt-blue">◈ AI THINKING PANEL</div>', unsafe_allow_html=True)
                for t in thinking:
                    agent    = t.get("agent", "unknown").upper()
                    step     = t.get("step", "")
                    decision = t.get("decision", "")
                    observations = t.get("observations", "")
                    llm_metrics = t.get("llm_metrics", {})
                    token_label = (
                                        f"[{agent}] → {step}  |  "
                                        f"PROVIDER {llm_metrics.get('provider','-')} - {llm_metrics.get('model','-')} | "
                                        f"IN {llm_metrics.get('input_tokens', 0)}  "
                                        f"OUT {llm_metrics.get('output_tokens', 0)}  "
                                        f"TOT {llm_metrics.get('total_tokens', 0)}  "
                                        f"⏱ {llm_metrics.get('latency_ms', 0)}ms  "
                                        f"CTX {llm_metrics.get('context_window_pct', 0):.1f}%"
                                   ) if llm_metrics else f"[{agent}]  →  {step}"

                    with st.expander(token_label, expanded=False):
                        if "input" in t:
                            st.markdown('<span style="font-size:9px;letter-spacing:2px;color:#4b5563">INPUT</span>', unsafe_allow_html=True)
                            st.json(t["input"])
                        if observations:
                            st.markdown('<span style="font-size:9px;letter-spacing:2px;color:#4b5563">OBSERVATIONS</span>', unsafe_allow_html=True)
                            st.json(observations)    
                        if decision:
                            st.markdown(f'<div class="think-dec"><b>DECISION</b><br>{decision}</div>', unsafe_allow_html=True)
                        if "confidence" in t:
                            st.markdown(f'<div class="kv"><span class="kk">CONFIDENCE</span><span class="kv-g">{t["confidence"]}</span></div>', unsafe_allow_html=True)    
                        if "retrieved_context" in t:
                            st.markdown('<span style="font-size:9px;letter-spacing:2px;color:#4b5563">RETRIEVED CONTEXT</span>', unsafe_allow_html=True)
                            st.json(t["retrieved_context"])
                        if "output" in t:
                            st.markdown('<span style="font-size:9px;letter-spacing:2px;color:#4b5563">OUTPUT</span>', unsafe_allow_html=True)
                            st.json(t["output"])
                        
                st.markdown('</div>', unsafe_allow_html=True)
                

                 # ── Stop condition: runbook_generation seen in thinking ─
                runbook_done = any(
                    t.get("agent", "").upper() == "RUNBOOKAGENT" and t.get("step") == "runbook_generation"
                    for t in thinking
                )
                if runbook_done:
                    status_ph.markdown(
                        '<div class="panel-green"><span class="sdot"></span>'
                        '<span style="color:#4ade80;font-size:11px;letter-spacing:1px"> EXECUTION COMPLETE</span></div>',
                        unsafe_allow_html=True
                    )
                    break

        time.sleep(3)