from mcp.server.fastmcp import FastMCP
from random import choice, randint

mcp = FastMCP("Sentinel MCP Server",
                host="0.0.0.0",
                port=8001,
                log_level="INFO"
            )

@mcp.tool()
def check_logs(step: str, service: str):
    """Check logs for errors and issues"""
    scenarios = [
        {"error": "timeout error", "confidence": 0.90},
        {"error": "memory leak detected", "confidence": 0.85},
        {"error": "disk I/O spike", "confidence": 0.75},
        {"error": "no issue", "confidence": 0.60},
    ]
    return {
        "step": step,
        "result": choice(scenarios)
    }

@mcp.tool()
def alert_human(step: str, severity: str):
    """Alert a human with incident details"""
    scenarios = [
        {"alert_sent": True, "acknowledged": True, "confidence": 0.95},
        {"alert_sent": True, "acknowledged": False, "confidence": 0.95},
        {"alert_sent": True, "acknowledged": True, "confidence": 0.85},
    ]
    return {
        "step": step,
        "result": choice(scenarios)
    }

@mcp.tool()
def check_health_endpoint(step: str, service_url: str):
    """Check health endpoint status"""
    scenarios = [
        {"health": "ok", "response_time_ms": randint(100, 300), "confidence": 0.9},
        {"health": "degraded", "response_time_ms": randint(400, 800), "confidence": 0.7},
        {"health": "error", "response_time_ms": randint(900, 1200), "confidence": 0.4},
        {"health": "timeout", "response_time_ms": randint(1300, 1500), "confidence": 0.3},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def clear_cache(step: str, cache_type: str):
    """Clear cache to improve performance"""
    scenarios = [
        {"cache_cleared": True, "latency_improvement": randint(10, 40), "confidence": 0.9},
        {"cache_cleared": True, "latency_improvement": randint(15, 35), "confidence": 0.88},
        {"cache_cleared": False, "latency_improvement": 0, "confidence": 0.6},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def close_incident(step: str, incident_id: str):
    """Close an active incident"""
    scenarios = [
        {"closed": True, "confidence": 0.95},
        {"closed": True, "confidence": 0.92},
        {"closed": False, "reason": "unresolved_signals", "confidence": 0.4},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def inspect_metrics(step: str, service: str):
    """Inspect system metrics (CPU, memory, etc)"""
    scenarios = [
        {"cpu": randint(40, 60), "memory": randint(30, 50), "confidence": 0.8},
        {"cpu": randint(70, 95), "memory": randint(70, 90), "confidence": 0.8},
        {"cpu": randint(10, 40), "memory": randint(10, 30), "confidence": 0.8},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def monitor_service(step: str, service: str):
    """Monitor service for stability"""
    scenarios = [
        {"service_status": "healthy", "latency_ms": randint(50, 150), "confidence": 0.9},
        {"service_status": "recovering", "latency_ms": randint(200, 350), "confidence": 0.75},
        {"service_status": "still_unstable", "latency_ms": randint(400, 500), "confidence": 0.5},
        {"service_status": "down", "latency_ms": 0, "confidence": 0.3},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def restart_container(step: str, container_id: str):
    """Restart a container"""
    scenarios = [
        {"action": "restart_attempted", "success": True, "confidence": 0.9},
        {"action": "restart_attempted", "success": True, "confidence": 0.85},
        {"action": "restart_attempted", "success": False, "confidence": 0.4},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def rollback_deployment(step: str, deployment_id: str):
    """Rollback deployment to previous stable version"""
    scenarios = [
        {"version": "previous_stable", "rollback": True, "confidence": 0.88},
        {"version": "previous_stable", "rollback": True, "confidence": 0.85},
        {"version": "previous_stable", "rollback": False, "reason": "rollback_failed", "confidence": 0.45},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

@mcp.tool()
def scale_service(step: str, service: str, direction: str = "up"):
    """Scale service up or down"""
    scenarios = [
        {"replicas": randint(3, 6), "scaling": direction, "success": True, "confidence": 0.85},
        {"replicas": randint(3, 6), "scaling": direction, "success": True, "confidence": 0.82},
        {"replicas": randint(2, 4), "scaling": direction, "success": False, "reason": "limit_reached", "confidence": 0.5},
    ]
    result = choice(scenarios)
    return {
        "step": step,
        "result": result
    }

if __name__ == "__main__":
    mcp.run(transport="sse")