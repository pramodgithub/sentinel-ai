from app.tools.log_tool import LogTool
from app.tools.metrics_tool import MetricsTool
from app.tools.restart_tool import RestartTool
from app.tools.monitor_tool import MonitorTool
from app.tools.close_incident import closeIncident
from app.tools.check_health_endpoint import checkHealthEndpoint
from app.tools.scale_service import scaleService
from app.tools.clear_cache import clearCache
from app.tools.rollback_deployment import rollbackDeployment
from app.tools.alert_human import alertHuman


class ToolRegistry:

    def __init__(self):

        self.tools = {
            "check_logs": LogTool(),
            "inspect_metrics": MetricsTool(),
            "restart_container": RestartTool(),
            "monitor_service": MonitorTool(),
            "close_incident": closeIncident(),
            "check_health_endpoint": checkHealthEndpoint(),
            "scale_service": scaleService(),
            "clear_cache": clearCache(),
            "rollback_deployment": rollbackDeployment(),
            "alert_human": alertHuman(),
        }

    def get_tool(self, name):

        return self.tools.get(name)