"""
Attack Visualizer - Maps MITRE techniques to visual representations

This is where the magic happens! Each attack type gets a unique
retro 2D visualization (Pacman, Snake, NES-style).
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VisualElement:
    """A visual element in the scene"""
    type: str  # sprite, path, effect, text
    asset: str  # which sprite/asset to use
    position: Dict[str, float]  # x, y coordinates
    animation: str  # animation to play
    duration: float  # how long this element appears
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class VisualScene:
    """A complete visual scene for an attack"""
    scene_type: str  # network, system, process, data
    background: str  # background asset
    elements: List[VisualElement]
    narration_points: List[Dict[str, Any]]  # where to show narration
    duration: float  # total scene duration


class AttackVisualizer:
    """Maps MITRE ATT&CK techniques to visual representations"""

    def __init__(self, mitre_loader):
        self.mitre_loader = mitre_loader
        self.visual_mappings = self._initialize_mappings()

    def _initialize_mappings(self) -> Dict[str, callable]:
        """Initialize technique-to-visual mappings"""
        return {
            # Initial Access
            "initial-access": self._visualize_initial_access,
            "phishing": self._visualize_phishing,

            # Execution
            "execution": self._visualize_execution,
            "command-and-scripting": self._visualize_command_execution,

            # Persistence
            "persistence": self._visualize_persistence,

            # Privilege Escalation
            "privilege-escalation": self._visualize_privilege_escalation,

            # Defense Evasion
            "defense-evasion": self._visualize_defense_evasion,

            # Credential Access
            "credential-access": self._visualize_credential_access,

            # Discovery
            "discovery": self._visualize_discovery,

            # Lateral Movement
            "lateral-movement": self._visualize_lateral_movement,

            # Collection
            "collection": self._visualize_collection,

            # Command and Control
            "command-and-control": self._visualize_c2,

            # Exfiltration
            "exfiltration": self._visualize_exfiltration,

            # Impact
            "impact": self._visualize_impact,
        }

    def get_visual_for_technique(self, technique) -> Dict[str, Any]:
        """Get visual representation for a technique"""
        # Determine which visualization to use based on tactics
        primary_tactic = technique.tactics[0] if technique.tactics else "execution"

        # Get the appropriate visualizer function
        visualizer_func = self.visual_mappings.get(
            primary_tactic,
            self._visualize_generic
        )

        scene = visualizer_func(technique)

        return {
            "technique_id": technique.id,
            "technique_name": technique.name,
            "scene": {
                "type": scene.scene_type,
                "background": scene.background,
                "duration": scene.duration,
                "elements": [
                    {
                        "type": elem.type,
                        "asset": elem.asset,
                        "position": elem.position,
                        "animation": elem.animation,
                        "duration": elem.duration,
                        "metadata": elem.metadata
                    }
                    for elem in scene.elements
                ],
                "narration_points": scene.narration_points
            }
        }

    def _visualize_initial_access(self, technique) -> VisualScene:
        """Visualize initial access techniques"""
        return VisualScene(
            scene_type="network",
            background="network_diagram",
            duration=8.0,
            elements=[
                VisualElement(
                    type="sprite",
                    asset="attacker_pacman",
                    position={"x": 50, "y": 300},
                    animation="move_right",
                    duration=3.0,
                    metadata={"color": "red", "size": 32}
                ),
                VisualElement(
                    type="sprite",
                    asset="firewall",
                    position={"x": 400, "y": 300},
                    animation="idle",
                    duration=8.0,
                    metadata={"color": "blue"}
                ),
                VisualElement(
                    type="effect",
                    asset="breach_effect",
                    position={"x": 400, "y": 300},
                    animation="explode",
                    duration=1.0,
                    metadata={"delay": 3.0}
                ),
                VisualElement(
                    type="sprite",
                    asset="attacker_pacman",
                    position={"x": 600, "y": 300},
                    animation="celebrate",
                    duration=2.0,
                    metadata={"delay": 4.0}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Attacker approaches the network perimeter..."},
                {"time": 3, "text": "Breach detected! Firewall bypassed!"},
                {"time": 5, "text": "Initial access established."}
            ]
        )

    def _visualize_phishing(self, technique) -> VisualScene:
        """Visualize phishing attacks"""
        return VisualScene(
            scene_type="network",
            background="email_interface",
            duration=10.0,
            elements=[
                VisualElement(
                    type="sprite",
                    asset="email_icon",
                    position={"x": 100, "y": 200},
                    animation="bounce",
                    duration=2.0,
                    metadata={"suspicious": True}
                ),
                VisualElement(
                    type="sprite",
                    asset="user_icon",
                    position={"x": 500, "y": 200},
                    animation="idle",
                    duration=10.0
                ),
                VisualElement(
                    type="path",
                    asset="dotted_line",
                    position={"x": 100, "y": 200},
                    animation="draw_to_target",
                    duration=2.0,
                    metadata={"target": {"x": 500, "y": 200}, "delay": 2.0}
                ),
                VisualElement(
                    type="sprite",
                    asset="user_icon",
                    position={"x": 500, "y": 200},
                    animation="click",
                    duration=1.0,
                    metadata={"delay": 4.0}
                ),
                VisualElement(
                    type="effect",
                    asset="malware_download",
                    position={"x": 500, "y": 200},
                    animation="download",
                    duration=2.0,
                    metadata={"delay": 5.0}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Malicious email sent to target..."},
                {"time": 2, "text": "Email arrives in user's inbox"},
                {"time": 4, "text": "User clicks malicious link!"},
                {"time": 6, "text": "Malware downloading..."}
            ]
        )

    def _visualize_privilege_escalation(self, technique) -> VisualScene:
        """Visualize privilege escalation - like climbing a ladder!"""
        return VisualScene(
            scene_type="system",
            background="permission_hierarchy",
            duration=8.0,
            elements=[
                # User starts at bottom
                VisualElement(
                    type="sprite",
                    asset="user_low_privilege",
                    position={"x": 300, "y": 450},
                    animation="idle",
                    duration=2.0,
                    metadata={"privilege": "user", "color": "green"}
                ),
                # Ladder appears
                VisualElement(
                    type="sprite",
                    asset="ladder",
                    position={"x": 300, "y": 300},
                    animation="appear",
                    duration=6.0,
                    metadata={"delay": 1.0}
                ),
                # User climbs
                VisualElement(
                    type="sprite",
                    asset="user_climbing",
                    position={"x": 300, "y": 300},
                    animation="climb",
                    duration=3.0,
                    metadata={"delay": 2.0}
                ),
                # Crown appears (root/admin)
                VisualElement(
                    type="sprite",
                    asset="crown",
                    position={"x": 300, "y": 150},
                    animation="shine",
                    duration=2.0,
                    metadata={"delay": 5.0}
                ),
                # User becomes admin
                VisualElement(
                    type="sprite",
                    asset="user_admin",
                    position={"x": 300, "y": 150},
                    animation="celebrate",
                    duration=3.0,
                    metadata={"delay": 5.0, "color": "gold"}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Attacker has low-privilege access..."},
                {"time": 2, "text": "Exploit found! Escalating privileges..."},
                {"time": 5, "text": "Root access obtained!"}
            ]
        )

    def _visualize_command_execution(self, technique) -> VisualScene:
        """Visualize command execution - terminal with commands typing"""
        return VisualScene(
            scene_type="process",
            background="terminal_screen",
            duration=7.0,
            elements=[
                VisualElement(
                    type="text",
                    asset="command_prompt",
                    position={"x": 50, "y": 100},
                    animation="type",
                    duration=2.0,
                    metadata={"text": "$ whoami", "speed": "fast"}
                ),
                VisualElement(
                    type="text",
                    asset="command_output",
                    position={"x": 50, "y": 130},
                    animation="appear",
                    duration=1.0,
                    metadata={"text": "attacker", "delay": 2.0}
                ),
                VisualElement(
                    type="text",
                    asset="command_prompt",
                    position={"x": 50, "y": 160},
                    animation="type",
                    duration=2.0,
                    metadata={"text": "$ cat /etc/passwd", "delay": 3.0}
                ),
                VisualElement(
                    type="sprite",
                    asset="data_stream",
                    position={"x": 50, "y": 190},
                    animation="scroll",
                    duration=2.0,
                    metadata={"delay": 5.0, "color": "green"}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Attacker executes reconnaissance commands"},
                {"time": 3, "text": "Reading sensitive system files..."},
                {"time": 5, "text": "Data exfiltration in progress"}
            ]
        )

    def _visualize_lateral_movement(self, technique) -> VisualScene:
        """Visualize lateral movement - Pacman style moving between systems"""
        return VisualScene(
            scene_type="network",
            background="network_grid",
            duration=12.0,
            elements=[
                # Multiple systems
                VisualElement(
                    type="sprite",
                    asset="server",
                    position={"x": 200, "y": 300},
                    animation="idle",
                    duration=12.0,
                    metadata={"label": "Server 1", "compromised": True}
                ),
                VisualElement(
                    type="sprite",
                    asset="server",
                    position={"x": 400, "y": 300},
                    animation="idle",
                    duration=12.0,
                    metadata={"label": "Server 2"}
                ),
                VisualElement(
                    type="sprite",
                    asset="server",
                    position={"x": 600, "y": 300},
                    animation="idle",
                    duration=12.0,
                    metadata={"label": "Server 3"}
                ),
                # Attacker moves between systems
                VisualElement(
                    type="sprite",
                    asset="attacker_snake",
                    position={"x": 200, "y": 300},
                    animation="move_path",
                    duration=10.0,
                    metadata={
                        "path": [
                            {"x": 200, "y": 300},
                            {"x": 400, "y": 300},
                            {"x": 600, "y": 300}
                        ],
                        "style": "snake"
                    }
                ),
                # Compromise effects
                VisualElement(
                    type="effect",
                    asset="compromise",
                    position={"x": 400, "y": 300},
                    animation="pulse",
                    duration=1.0,
                    metadata={"delay": 4.0, "color": "red"}
                ),
                VisualElement(
                    type="effect",
                    asset="compromise",
                    position={"x": 600, "y": 300},
                    animation="pulse",
                    duration=1.0,
                    metadata={"delay": 8.0, "color": "red"}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Attacker moves from compromised system..."},
                {"time": 4, "text": "Second system compromised!"},
                {"time": 8, "text": "Third system breached! Network owned."}
            ]
        )

    def _visualize_credential_access(self, technique) -> VisualScene:
        """Visualize credential theft - collecting coins/keys"""
        return VisualScene(
            scene_type="system",
            background="memory_space",
            duration=8.0,
            elements=[
                # Keys/credentials scattered
                VisualElement(
                    type="sprite",
                    asset="key",
                    position={"x": 150, "y": 200},
                    animation="float",
                    duration=8.0,
                    metadata={"type": "password"}
                ),
                VisualElement(
                    type="sprite",
                    asset="key",
                    position={"x": 300, "y": 250},
                    animation="float",
                    duration=8.0,
                    metadata={"type": "hash"}
                ),
                VisualElement(
                    type="sprite",
                    asset="key",
                    position={"x": 450, "y": 200},
                    animation="float",
                    duration=8.0,
                    metadata={"type": "token"}
                ),
                # Attacker collects them Pacman-style
                VisualElement(
                    type="sprite",
                    asset="attacker_pacman",
                    position={"x": 50, "y": 200},
                    animation="collect_path",
                    duration=7.0,
                    metadata={
                        "path": [
                            {"x": 150, "y": 200},
                            {"x": 300, "y": 250},
                            {"x": 450, "y": 200}
                        ]
                    }
                ),
                # Collection effects
                VisualElement(
                    type="effect",
                    asset="collect_sparkle",
                    position={"x": 150, "y": 200},
                    animation="collect",
                    duration=0.5,
                    metadata={"delay": 2.0}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Dumping credentials from memory..."},
                {"time": 3, "text": "Password hashes collected"},
                {"time": 6, "text": "Access tokens acquired"}
            ]
        )

    def _visualize_exfiltration(self, technique) -> VisualScene:
        """Visualize data exfiltration - data flowing out"""
        return VisualScene(
            scene_type="network",
            background="data_center",
            duration=10.0,
            elements=[
                VisualElement(
                    type="sprite",
                    asset="database",
                    position={"x": 150, "y": 300},
                    animation="idle",
                    duration=10.0,
                    metadata={"label": "Internal Database"}
                ),
                VisualElement(
                    type="sprite",
                    asset="attacker_server",
                    position={"x": 650, "y": 300},
                    animation="idle",
                    duration=10.0,
                    metadata={"label": "C2 Server", "color": "red"}
                ),
                # Data packets flowing
                VisualElement(
                    type="sprite",
                    asset="data_packet",
                    position={"x": 150, "y": 300},
                    animation="move_to",
                    duration=8.0,
                    metadata={
                        "target": {"x": 650, "y": 300},
                        "repeat": True,
                        "delay_between": 1.0
                    }
                ),
                # Alert icon
                VisualElement(
                    type="sprite",
                    asset="alert_icon",
                    position={"x": 400, "y": 100},
                    animation="pulse",
                    duration=10.0,
                    metadata={"delay": 2.0, "color": "yellow"}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Sensitive data identified..."},
                {"time": 2, "text": "Exfiltration in progress!"},
                {"time": 5, "text": "Data streaming to attacker server"}
            ]
        )

    def _visualize_defense_evasion(self, technique) -> VisualScene:
        """Visualize defense evasion - stealth mechanics"""
        return VisualScene(
            scene_type="system",
            background="security_monitoring",
            duration=9.0,
            elements=[
                VisualElement(
                    type="sprite",
                    asset="security_camera",
                    position={"x": 400, "y": 100},
                    animation="scan",
                    duration=9.0
                ),
                VisualElement(
                    type="sprite",
                    asset="attacker_ghost",
                    position={"x": 100, "y": 300},
                    animation="sneak",
                    duration=8.0,
                    metadata={"invisible": True, "opacity": 0.3}
                ),
                VisualElement(
                    type="effect",
                    asset="obfuscation",
                    position={"x": 300, "y": 300},
                    animation="cloak",
                    duration=9.0,
                    metadata={"style": "shimmer"}
                )
            ],
            narration_points=[
                {"time": 0, "text": "Security monitoring active..."},
                {"time": 3, "text": "Attacker using evasion techniques"},
                {"time": 6, "text": "Bypassing detection systems"}
            ]
        )

    def _visualize_generic(self, technique) -> VisualScene:
        """Generic visualization for unmapped techniques"""
        return VisualScene(
            scene_type="abstract",
            background="cyber_grid",
            duration=6.0,
            elements=[
                VisualElement(
                    type="text",
                    asset="title",
                    position={"x": 300, "y": 200},
                    animation="fade_in",
                    duration=2.0,
                    metadata={"text": technique.name, "size": 24}
                ),
                VisualElement(
                    type="sprite",
                    asset="cyber_effect",
                    position={"x": 400, "y": 300},
                    animation="pulse",
                    duration=6.0
                )
            ],
            narration_points=[
                {"time": 0, "text": f"Executing: {technique.name}"}
            ]
        )

    # Additional visualizers for other tactics...
    def _visualize_execution(self, technique):
        return self._visualize_command_execution(technique)

    def _visualize_persistence(self, technique):
        return self._visualize_generic(technique)

    def _visualize_discovery(self, technique):
        return self._visualize_generic(technique)

    def _visualize_collection(self, technique):
        return self._visualize_credential_access(technique)

    def _visualize_c2(self, technique):
        return self._visualize_generic(technique)

    def _visualize_impact(self, technique):
        return self._visualize_generic(technique)
