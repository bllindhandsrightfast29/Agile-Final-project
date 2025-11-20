"""
Attack Narrator - AI-powered storytelling for attacks

Uses Claude API (if available) to generate Khan Academy-style
explanations of what's happening during attacks.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not available. Using fallback narration.")


class AttackNarrator:
    """Generates educational narration for attack techniques"""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None

        if ANTHROPIC_AVAILABLE and self.api_key:
            try:
                self.client = Anthropic(api_key=self.api_key)
                logger.info("✅ Claude API initialized for enhanced narration")
            except Exception as e:
                logger.warning(f"Could not initialize Claude API: {e}")

    async def narrate_technique(self, technique) -> dict:
        """Generate narration for a technique"""

        if self.client:
            return await self._narrate_with_claude(technique)
        else:
            return self._narrate_fallback(technique)

    async def _narrate_with_claude(self, technique) -> dict:
        """Use Claude to generate educational narration"""
        try:
            prompt = f"""You are an educational cybersecurity instructor like Sal Khan from Khan Academy.
Explain the following MITRE ATT&CK technique in a clear, engaging way that a beginner can understand.

Technique: {technique.name} ({technique.id})
Description: {technique.description}

Provide:
1. A simple explanation (2-3 sentences) of what this attack does
2. A real-world analogy to help understand it
3. Why an attacker would use this technique
4. How defenders can detect or prevent it

Keep it conversational and educational, like you're drawing it out on a whiteboard."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            narration_text = message.content[0].text

            return {
                "type": "ai_generated",
                "technique_id": technique.id,
                "technique_name": technique.name,
                "narration": narration_text,
                "voice": "claude"
            }

        except Exception as e:
            logger.error(f"Failed to generate Claude narration: {e}")
            return self._narrate_fallback(technique)

    def _narrate_fallback(self, technique) -> dict:
        """Fallback narration using templates"""

        # Template-based narration
        narration = self._generate_template_narration(technique)

        return {
            "type": "template",
            "technique_id": technique.id,
            "technique_name": technique.name,
            "narration": narration,
            "voice": "template"
        }

    def _generate_template_narration(self, technique) -> str:
        """Generate template-based narration"""

        tactic = technique.tactics[0] if technique.tactics else "unknown"

        # Build narration based on tactic
        narration_parts = []

        # Introduction
        narration_parts.append(f"This is {technique.name}, a {tactic} technique.")

        # Description (simplified)
        description = technique.description[:200]
        if len(technique.description) > 200:
            description += "..."
        narration_parts.append(description)

        # What's happening
        if tactic == "initial-access":
            narration_parts.append(
                "The attacker is trying to get their first foothold into your network. "
                "Think of it like someone trying to unlock your front door."
            )
        elif tactic == "execution":
            narration_parts.append(
                "The attacker is now running malicious code on the system. "
                "Like someone who got into your house and is now rummaging through your stuff."
            )
        elif tactic == "privilege-escalation":
            narration_parts.append(
                "The attacker is trying to gain higher privileges, like going from a regular user to an administrator. "
                "Think of it like a guest trying to get the master key to your building."
            )
        elif tactic == "credential-access":
            narration_parts.append(
                "The attacker is stealing passwords and credentials. "
                "Like a thief copying all the keys from your key rack."
            )
        elif tactic == "lateral-movement":
            narration_parts.append(
                "The attacker is moving from one system to another within your network. "
                "Like a burglar moving from room to room in your house."
            )
        elif tactic == "exfiltration":
            narration_parts.append(
                "The attacker is stealing your data and sending it outside the network. "
                "Like someone loading your valuables into a truck."
            )

        # Detection tip
        if technique.detection:
            detection_tip = technique.detection[:150]
            if len(technique.detection) > 150:
                detection_tip += "..."
            narration_parts.append(f"\n\nDetection tip: {detection_tip}")

        return " ".join(narration_parts)

    def narrate_step(self, step_description: str, context: dict = None) -> str:
        """Generate narration for a specific attack step"""
        if context is None:
            context = {}

        # Simple step-by-step narration
        return f"Now happening: {step_description}"

    def generate_scenario_intro(self, scenario_name: str, description: str) -> str:
        """Generate introduction for an attack scenario"""
        return f"""
Welcome to the '{scenario_name}' scenario!

{description}

Watch as we visualize each step of this attack chain.
Pay attention to how attackers move through different stages,
and think about where defenders could detect and stop them.

Let's begin!
        """.strip()

    def generate_scenario_conclusion(self, scenario_name: str, techniques_used: int) -> str:
        """Generate conclusion for an attack scenario"""
        return f"""
Scenario '{scenario_name}' complete!

We just visualized {techniques_used} different attack techniques.

Key takeaways:
- Attackers use multiple techniques in combination
- Each step provides opportunities for detection
- Defense is about breaking the attack chain at any point

Great job learning about these cybersecurity concepts!
        """.strip()
