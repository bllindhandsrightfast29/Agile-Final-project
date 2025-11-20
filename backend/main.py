"""
Cyber Defense Visualization System - Main Backend Server

This is the core FastAPI server that:
1. Serves the frontend visualization
2. Provides WebSocket for real-time attack streaming
3. Integrates with Falco for live event monitoring
4. Loads MITRE ATT&CK data for attack mapping
"""

import asyncio
import json
import logging
from typing import Set
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from mitre_loader import MITRELoader
from visualizer import AttackVisualizer
from narrator import AttackNarrator
from falco_listener import FalcoListener

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cyber Defense Visualization System",
    description="Real-time attack visualization and narration system",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
mitre_loader = MITRELoader()
visualizer = AttackVisualizer(mitre_loader)
narrator = AttackNarrator()
falco_listener = FalcoListener()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return

        message_json = json.dumps(message)
        disconnected = set()

        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("🚀 Starting Cyber Defense Visualization System...")

    # Load MITRE ATT&CK data
    logger.info("📚 Loading MITRE ATT&CK framework...")
    try:
        await mitre_loader.load_data()
        technique_count = len(mitre_loader.get_all_techniques())
        logger.info(f"✅ Loaded {technique_count} MITRE ATT&CK techniques")
    except Exception as e:
        logger.error(f"❌ Failed to load MITRE data: {e}")

    # Initialize Falco listener (if available)
    logger.info("🐳 Initializing Falco listener...")
    try:
        await falco_listener.initialize()
        logger.info("✅ Falco listener initialized")
    except Exception as e:
        logger.warning(f"⚠️  Falco not available (optional): {e}")

    logger.info("🎮 System ready! Open browser to start visualizations")


@app.get("/")
async def read_root():
    """Serve the main visualization page"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Defense Visualization</title>
    </head>
    <body>
        <h1>🎮 Cyber Defense Visualization System</h1>
        <p>Frontend will be served here. Navigate to <code>/viewer</code> for the visualization.</p>
        <a href="/viewer">Launch Visualization</a>
    </body>
    </html>
    """)


@app.get("/api/techniques")
async def get_techniques():
    """Get all MITRE ATT&CK techniques"""
    techniques = mitre_loader.get_all_techniques()
    return {
        "count": len(techniques),
        "techniques": [
            {
                "id": tech.id,
                "name": tech.name,
                "description": tech.description[:200] + "..." if len(tech.description) > 200 else tech.description,
                "tactics": tech.tactics
            }
            for tech in techniques[:50]  # Limit to first 50 for performance
        ]
    }


@app.get("/api/techniques/{technique_id}")
async def get_technique(technique_id: str):
    """Get specific technique details"""
    technique = mitre_loader.get_technique(technique_id)
    if not technique:
        return {"error": "Technique not found"}

    # Get visual representation
    visual = visualizer.get_visual_for_technique(technique)

    # Get narration
    narration = await narrator.narrate_technique(technique)

    return {
        "technique": {
            "id": technique.id,
            "name": technique.name,
            "description": technique.description,
            "tactics": technique.tactics
        },
        "visual": visual,
        "narration": narration
    }


@app.post("/api/simulate/{technique_id}")
async def simulate_attack(technique_id: str):
    """Simulate an attack and broadcast visualization"""
    technique = mitre_loader.get_technique(technique_id)
    if not technique:
        return {"error": "Technique not found"}

    # Generate visualization data
    visual = visualizer.get_visual_for_technique(technique)
    narration = await narrator.narrate_technique(technique)

    # Broadcast to all connected clients
    await manager.broadcast({
        "type": "attack_simulation",
        "technique_id": technique_id,
        "technique_name": technique.name,
        "visual": visual,
        "narration": narration,
        "timestamp": asyncio.get_event_loop().time()
    })

    return {
        "status": "simulated",
        "technique": technique.name,
        "broadcast_to": len(manager.active_connections)
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time attack visualization"""
    await manager.connect(websocket)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connection_established",
            "message": "Connected to Cyber Defense Visualization System",
            "available_techniques": len(mitre_loader.get_all_techniques())
        })

        # Listen for messages from client
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "request_attack":
                technique_id = message.get("technique_id")
                if technique_id:
                    await simulate_attack(technique_id)

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/api/scenarios")
async def get_scenarios():
    """Get available attack scenarios"""
    scenarios_dir = Path("data/attack_scenarios")
    scenarios = []

    if scenarios_dir.exists():
        for scenario_file in scenarios_dir.glob("*.json"):
            with open(scenario_file) as f:
                scenario = json.load(f)
                scenarios.append(scenario)

    return {"scenarios": scenarios}


@app.post("/api/scenarios/{scenario_id}/play")
async def play_scenario(scenario_id: str):
    """Play an attack scenario (sequence of techniques)"""
    scenario_file = Path(f"data/attack_scenarios/{scenario_id}.json")

    if not scenario_file.exists():
        return {"error": "Scenario not found"}

    with open(scenario_file) as f:
        scenario = json.load(f)

    # Start background task to play scenario
    asyncio.create_task(play_scenario_background(scenario))

    return {
        "status": "playing",
        "scenario": scenario.get("name"),
        "steps": len(scenario.get("steps", []))
    }


async def play_scenario_background(scenario: dict):
    """Play a scenario in the background"""
    steps = scenario.get("steps", [])

    for step in steps:
        technique_id = step.get("technique_id")
        delay = step.get("delay", 2.0)

        # Simulate the attack
        await simulate_attack(technique_id)

        # Wait before next step
        await asyncio.sleep(delay)

    # Send completion message
    await manager.broadcast({
        "type": "scenario_complete",
        "scenario": scenario.get("name")
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
