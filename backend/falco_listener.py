"""
Falco Event Listener - Watches Docker runtime events

Integrates with Falco to detect real security events in Docker containers
and visualize them in real-time.
"""

import asyncio
import json
import logging
from typing import Optional, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class FalcoListener:
    """Listens to Falco events and triggers visualizations"""

    def __init__(self, socket_path: str = "/var/run/falco.sock"):
        self.socket_path = socket_path
        self.running = False
        self.event_callback: Optional[Callable] = None
        self.event_mapping = self._initialize_event_mappings()

    def _initialize_event_mappings(self) -> dict:
        """Map Falco rules to MITRE techniques"""
        return {
            # Container events
            "Terminal shell in container": "T1059",  # Command execution
            "Write below rpm database": "T1543.002",  # Persistence
            "DB program spawned process": "T1059.004",  # Unix shell
            "Modify binary dirs": "T1222",  # File permissions modification
            "Contact K8S API Server": "T1552",  # Discovery

            # Network events
            "Outbound Connection to C2 Servers": "T1071",  # Application Layer Protocol
            "Contact cloud metadata service": "T1552.005",  # Cloud Instance Metadata API

            # Credential access
            "Read sensitive file untrusted": "T1552.001",  # Credentials in files
            "Read SSH keys": "T1552.004",  # SSH keys

            # Privilege escalation
            "Privileged container started": "T1611",  # Escape to Host
            "Set Setuid or Setgid bit": "T1548.001",  # Setuid and Setgid

            # Persistence
            "Schedule Cron Jobs": "T1053.003",  # Cron
            "Create files below dev": "T1036",  # Masquerading

            # Defense evasion
            "Delete or rename shell history": "T1070.003",  # Clear command history
            "Clear Log Activities": "T1070",  # Indicator removal

            # Add more mappings as needed...
        }

    async def initialize(self):
        """Initialize Falco listener"""
        # Check if Falco socket exists
        if not Path(self.socket_path).exists():
            logger.warning(f"Falco socket not found at {self.socket_path}")
            logger.info("Running without Falco integration. Use simulate mode for demo.")
            return

        logger.info(f"Falco socket found: {self.socket_path}")
        # In production, we would connect to the socket here

    def set_event_callback(self, callback: Callable):
        """Set callback function for when events are detected"""
        self.event_callback = callback

    async def start_listening(self):
        """Start listening for Falco events"""
        self.running = True
        logger.info("📡 Falco listener started")

        # In a real implementation, we would:
        # 1. Connect to Falco socket/API
        # 2. Parse events
        # 3. Map to MITRE techniques
        # 4. Call event_callback

        # For now, this is a placeholder
        while self.running:
            await asyncio.sleep(1.0)

    async def stop_listening(self):
        """Stop listening for events"""
        self.running = False
        logger.info("Falco listener stopped")

    def map_falco_to_mitre(self, falco_rule: str) -> Optional[str]:
        """Map a Falco rule to a MITRE technique"""
        return self.event_mapping.get(falco_rule)

    async def parse_falco_event(self, event_data: dict) -> dict:
        """Parse a Falco event and prepare for visualization"""
        rule = event_data.get("rule", "")
        output = event_data.get("output", "")
        priority = event_data.get("priority", "")

        # Map to MITRE technique
        technique_id = self.map_falco_to_mitre(rule)

        return {
            "source": "falco",
            "rule": rule,
            "output": output,
            "priority": priority,
            "technique_id": technique_id,
            "timestamp": event_data.get("time"),
            "container": event_data.get("output_fields", {}).get("container.id"),
        }

    async def simulate_event(self, rule_name: str) -> dict:
        """Simulate a Falco event for testing"""
        if rule_name not in self.event_mapping:
            logger.warning(f"Unknown Falco rule: {rule_name}")
            return {}

        technique_id = self.event_mapping[rule_name]

        event = {
            "rule": rule_name,
            "output": f"Simulated: {rule_name}",
            "priority": "Warning",
            "time": "2024-01-01T00:00:00.000000000Z",
            "output_fields": {
                "container.id": "simulated-container",
                "proc.name": "bash"
            }
        }

        parsed = await self.parse_falco_event(event)

        if self.event_callback:
            await self.event_callback(parsed)

        return parsed


# Simulated Falco events for testing
EXAMPLE_SCENARIOS = [
    {
        "name": "Container Escape Attack",
        "description": "Attacker attempts to escape from container to host",
        "events": [
            "Privileged container started",
            "Terminal shell in container",
            "Modify binary dirs",
            "Read sensitive file untrusted"
        ]
    },
    {
        "name": "Credential Theft",
        "description": "Attacker steals SSH keys and credentials",
        "events": [
            "Terminal shell in container",
            "Read SSH keys",
            "Read sensitive file untrusted",
            "Outbound Connection to C2 Servers"
        ]
    },
    {
        "name": "Persistence Establishment",
        "description": "Attacker sets up persistent access",
        "events": [
            "Terminal shell in container",
            "Schedule Cron Jobs",
            "Create files below dev",
            "Set Setuid or Setgid bit"
        ]
    }
]
