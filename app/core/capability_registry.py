class CapabilityRegistry:

    def __init__(self):

        self.capabilities = {
            "check_logs": "Inspect application logs",
            "inspect_metrics": "Check CPU, memory, system metrics",
            "restart_container": "Restart failing container",
            "monitor_service": "Observe service health after remediation",
            "close_incident": "Mark incident resolved",
            "check_health_endpoint": "Check service health endpoint",
            "scale_service": "Scale service replicas",
            "clear_cache": "Clear application cache",
            "rollback_deployment": "Rollback to previous stable version",
            "alert_human": "Notify human operator for intervention"
        }

    def is_valid(self, action: str):
        return action in self.capabilities

    def list_actions(self):
        return list(self.capabilities.keys())