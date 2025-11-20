"""
MITRE ATT&CK Framework Data Loader

Loads and parses MITRE ATT&CK techniques for visualization.
Caches data locally for offline use.
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
import aiohttp

logger = logging.getLogger(__name__)

@dataclass
class MITRETechnique:
    """Represents a MITRE ATT&CK technique"""
    id: str
    name: str
    description: str
    tactics: List[str]
    platforms: List[str]
    detection: str = ""
    mitigation: str = ""
    examples: List[str] = None

    def __post_init__(self):
        if self.examples is None:
            self.examples = []


class MITRELoader:
    """Loads and manages MITRE ATT&CK data"""

    MITRE_ENTERPRISE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    CACHE_DIR = Path("data/mitre_cache")

    def __init__(self):
        self.techniques: Dict[str, MITRETechnique] = {}
        self.tactics: Dict[str, List[str]] = {}
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    async def load_data(self):
        """Load MITRE ATT&CK data from cache or download"""
        cache_file = self.CACHE_DIR / "enterprise-attack.json"

        # Try to load from cache first
        if cache_file.exists():
            logger.info("Loading MITRE data from cache...")
            with open(cache_file, 'r') as f:
                data = json.load(f)
        else:
            logger.info("Downloading MITRE ATT&CK data...")
            data = await self._download_data()
            # Save to cache
            with open(cache_file, 'w') as f:
                json.dump(data, f)

        self._parse_data(data)

    async def _download_data(self) -> dict:
        """Download MITRE ATT&CK data"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.MITRE_ENTERPRISE_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to download MITRE data: {response.status}")

    def _parse_data(self, data: dict):
        """Parse MITRE ATT&CK STIX data"""
        objects = data.get("objects", [])

        # First pass: collect tactics
        for obj in objects:
            if obj.get("type") == "x-mitre-tactic":
                tactic_name = obj.get("x_mitre_shortname", "")
                if tactic_name:
                    self.tactics[tactic_name] = []

        # Second pass: parse techniques
        for obj in objects:
            if obj.get("type") == "attack-pattern":
                technique = self._parse_technique(obj)
                if technique:
                    self.techniques[technique.id] = technique

                    # Add to tactic lists
                    for tactic in technique.tactics:
                        if tactic in self.tactics:
                            self.tactics[tactic].append(technique.id)

        logger.info(f"Parsed {len(self.techniques)} techniques across {len(self.tactics)} tactics")

    def _parse_technique(self, obj: dict) -> Optional[MITRETechnique]:
        """Parse a single technique from STIX object"""
        try:
            # Get technique ID (e.g., T1059.001)
            external_refs = obj.get("external_references", [])
            technique_id = None
            for ref in external_refs:
                if ref.get("source_name") == "mitre-attack":
                    technique_id = ref.get("external_id")
                    break

            if not technique_id:
                return None

            # Get kill chain phases (tactics)
            kill_chain_phases = obj.get("kill_chain_phases", [])
            tactics = [phase.get("phase_name") for phase in kill_chain_phases]

            # Get platforms
            platforms = obj.get("x_mitre_platforms", [])

            # Get detection info
            detection = obj.get("x_mitre_detection", "")

            return MITRETechnique(
                id=technique_id,
                name=obj.get("name", ""),
                description=obj.get("description", ""),
                tactics=tactics,
                platforms=platforms,
                detection=detection
            )
        except Exception as e:
            logger.warning(f"Failed to parse technique: {e}")
            return None

    def get_technique(self, technique_id: str) -> Optional[MITRETechnique]:
        """Get a specific technique by ID"""
        return self.techniques.get(technique_id)

    def get_all_techniques(self) -> List[MITRETechnique]:
        """Get all techniques"""
        return list(self.techniques.values())

    def get_techniques_by_tactic(self, tactic: str) -> List[MITRETechnique]:
        """Get all techniques for a specific tactic"""
        technique_ids = self.tactics.get(tactic, [])
        return [self.techniques[tid] for tid in technique_ids if tid in self.techniques]

    def search_techniques(self, query: str) -> List[MITRETechnique]:
        """Search techniques by name or description"""
        query = query.lower()
        results = []

        for technique in self.techniques.values():
            if query in technique.name.lower() or query in technique.description.lower():
                results.append(technique)

        return results
