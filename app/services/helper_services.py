from app.core.shared_store import get_thinking_trace


MODEL_PRICING = {
    "qwen3-coder:480b-cloud": {
        "input_per_1m": 0.22,
        "output_per_1m": 1.00,
    },
    "ollama-local": {
        "input_per_1m": 0.0,
        "output_per_1m": 0.0,
    }
}

def calculate_cost(total_input: int, total_output: int, model: str) -> dict:
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["ollama-local"])

    input_cost  = round((total_input  / 1_000_000) * pricing["input_per_1m"],  6)
    output_cost = round((total_output / 1_000_000) * pricing["output_per_1m"], 6)

    return {
    
        "input_cost_usd": input_cost,
        "output_cost_usd": output_cost,
        "total_cost_usd": round(input_cost + output_cost, 6),
    }
def compute_llm_metrics(execution_id, model_name):
    traces = get_thinking_trace(execution_id) or []

    total_input = 0
    total_output = 0
    total_latency = 0
    calls = 0

    for t in traces:
        metrics = t.get("llm_metrics")
        if not metrics:
            continue

        total_input += metrics.get("input_tokens", 0)
        total_output += metrics.get("output_tokens", 0)
        total_latency += metrics.get("latency_ms", 0)
        calls += 1

    avg_latency = round(total_latency / calls, 2) if calls else 0


    cost = calculate_cost(
                total_input=total_input,
                total_output=total_output,
                model=model_name
            )
    estimated_output_cost = cost.get("output_cost_usd", 0.0)
    estimated_input_cost = cost.get("input_cost_usd", 0.0)
    estimated_cost = cost.get("total_cost_usd", 0.0)

    return {
        "calls": calls,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "cost_input_tokens": estimated_input_cost,
        "cost_output_tokens": estimated_output_cost,
        "avg_latency": avg_latency,
        "cost": estimated_cost
    }