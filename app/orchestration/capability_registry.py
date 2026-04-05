"""Registry for managing available agent capabilities."""

from typing import Dict, Callable, Any


class CapabilityRegistry:
    """Registry for agent capabilities and tools."""

    def __init__(self):
        """Initialize the capability registry."""
        self.capabilities: Dict[str, Callable] = {}

    def register(self, name: str, capability: Callable) -> None:
        """Register a new capability.
        
        Args:
            name: Name of the capability
            capability: Callable implementing the capability
        """
        self.capabilities[name] = capability

    def get(self, name: str) -> Callable:
        """Get a registered capability.
        
        Args:
            name: Name of the capability
            
        Returns:
            The callable capability
        """
        return self.capabilities.get(name)

    def list(self) -> list:
        """List all registered capabilities.
        
        Returns:
            List of capability names
        """
        return list(self.capabilities.keys())
