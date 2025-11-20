# Extending the Visualization System

This guide shows you how to customize and extend the Cyber Defense Visualization System.

## Adding Custom Attack Visualizations

### 1. Create a New Visual Scene

Edit `backend/visualizer.py` and add a new visualization method:

```python
def _visualize_my_custom_attack(self, technique) -> VisualScene:
    """Visualize my custom attack"""
    return VisualScene(
        scene_type="network",
        background="cyber_grid",
        duration=10.0,
        elements=[
            VisualElement(
                type="sprite",
                asset="attacker_pacman",
                position={"x": 100, "y": 300},
                animation="move_right",
                duration=5.0
            ),
            # Add more elements...
        ],
        narration_points=[
            {"time": 0, "text": "Custom attack starting..."},
            {"time": 5, "text": "Attack completed!"}
        ]
    )
```

### 2. Map Technique to Visualization

Update the `_initialize_mappings()` method:

```python
def _initialize_mappings(self):
    return {
        # Existing mappings...
        "my-custom-tactic": self._visualize_my_custom_attack,
    }
```

## Creating Custom Sprites

### 1. Add Sprite Factory Method

Edit `frontend/game/sprites.js`:

```javascript
createMyCustomSprite(x, y) {
    const graphics = this.scene.add.graphics();

    // Draw your sprite
    graphics.fillStyle(COLORS.primary, 1);
    graphics.fillCircle(16, 16, 16);

    graphics.generateTexture('my_custom_sprite', 32, 32);
    graphics.destroy();

    return this.scene.add.sprite(x, y, 'my_custom_sprite');
}
```

### 2. Use in Scene Renderer

Update `frontend/game/scenes.js` to handle your new sprite:

```javascript
case 'my_custom_sprite':
    sprite = this.spriteFactory.createMyCustomSprite(
        element.position.x,
        element.position.y
    );
    break;
```

## Adding Custom Animations

In `frontend/game/scenes.js`, add new animation types:

```javascript
case 'my_animation':
    this.scene.tweens.add({
        targets: sprite,
        // Your animation properties
        x: sprite.x + 200,
        y: sprite.y - 100,
        rotation: Math.PI * 2,
        duration: element.duration * 1000,
        ease: 'Bounce.easeOut'
    });
    break;
```

## Creating Attack Scenarios

### 1. Create Scenario JSON

Create a new file in `data/attack_scenarios/my_scenario.json`:

```json
{
  "id": "my_scenario",
  "name": "My Custom Attack Scenario",
  "description": "Description of what this scenario demonstrates",
  "difficulty": "intermediate",
  "duration_minutes": 3,
  "steps": [
    {
      "technique_id": "T1566.001",
      "name": "Phishing",
      "delay": 0,
      "description": "Initial access"
    },
    {
      "technique_id": "T1059",
      "name": "Command Execution",
      "delay": 2.0,
      "description": "Execute payload"
    }
  ],
  "learning_objectives": [
    "Understanding attack chains",
    "Detection opportunities"
  ]
}
```

### 2. Load in Backend

The backend automatically loads all JSON files from `data/attack_scenarios/`.

## Integrating with Your Cypher Defender

### Option 1: Feed Real Events to Visualizer

```python
# In your cypher defender code
import requests

def visualize_detected_attack(technique_id):
    response = requests.post(
        'http://localhost:8000/api/simulate/{technique_id}'
    )
    # This broadcasts to all connected viewers
```

### Option 2: WebSocket Integration

```python
import asyncio
import websockets
import json

async def send_attack_event():
    async with websockets.connect('ws://localhost:8000/ws') as ws:
        await ws.send(json.dumps({
            "type": "request_attack",
            "technique_id": "T1059"
        }))
```

### Option 3: Falco Integration

1. **Configure Falco Output** - Point Falco to send events to your visualizer:

```yaml
# falco.yaml
json_output: true
json_include_output_property: true

# Send to your backend
http_output:
  enabled: true
  url: "http://localhost:8000/api/falco_event"
```

2. **Add Endpoint in Backend** - Create handler in `backend/main.py`:

```python
@app.post("/api/falco_event")
async def receive_falco_event(event: dict):
    # Parse Falco event
    parsed = await falco_listener.parse_falco_event(event)

    # Map to MITRE technique
    technique_id = parsed.get("technique_id")

    if technique_id:
        # Trigger visualization
        await simulate_attack(technique_id)

    return {"status": "processed"}
```

## Customizing Narration

### Use Custom Templates

Edit `backend/narrator.py`:

```python
def _generate_template_narration(self, technique) -> str:
    # Add your own narration logic
    custom_intro = f"🎯 Alert! {technique.name} detected!"

    # Add context specific to your environment
    if technique.id == "T1059":
        return f"{custom_intro}\n\nThis is a command execution attack commonly seen in your environment..."

    return custom_intro
```

### Integrate Your Own LLM

```python
class AttackNarrator:
    def __init__(self):
        # Use your preferred LLM
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def _narrate_with_llm(self, technique):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[...]
        )
        return response.choices[0].message.content
```

## Multi-Code Parallel Execution

You mentioned wanting to try parallel code execution. Here's how:

### Backend Parallel Processing

```python
import asyncio

async def process_multiple_attacks(technique_ids: List[str]):
    """Process multiple attacks in parallel"""
    tasks = [
        simulate_attack(tid) for tid in technique_ids
    ]

    results = await asyncio.gather(*tasks)
    return results
```

### Frontend Parallel Visualization

```javascript
async function playMultipleScenes(scenes) {
    // Play multiple attack visualizations simultaneously
    const promises = scenes.map(scene =>
        window.gameEngine.playVisualization(scene)
    );

    await Promise.all(promises);
}
```

## Performance Optimization

### Caching MITRE Data

The system already caches MITRE ATT&CK data in `data/mitre_cache/`. To force refresh:

```bash
rm -rf data/mitre_cache/*
# Restart backend - it will re-download
```

### Sprite Pooling

For better performance with many sprites:

```javascript
class SpriteFactory {
    constructor(scene) {
        this.scene = scene;
        this.pools = {}; // Sprite pools
    }

    getFromPool(type) {
        if (!this.pools[type]) {
            this.pools[type] = [];
        }

        let sprite = this.pools[type].pop();
        if (!sprite) {
            sprite = this.createSprite(type);
        }

        return sprite;
    }
}
```

## Testing Your Extensions

### Backend Tests

```python
# test_visualizer.py
import pytest
from visualizer import AttackVisualizer

def test_custom_visualization():
    viz = AttackVisualizer(mitre_loader)
    scene = viz._visualize_my_custom_attack(technique)

    assert scene.duration > 0
    assert len(scene.elements) > 0
```

### Frontend Tests

```javascript
// Test in browser console
const testScene = {
    scene: {
        type: "network",
        background: "cyber_grid",
        duration: 5.0,
        elements: [...]
    }
};

await window.gameEngine.playVisualization(testScene);
```

## Deployment

### Production Docker Setup

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build: .
    restart: always
    environment:
      - WORKERS=4
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Scaling with Load Balancer

```yaml
services:
  backend:
    scale: 3  # Run 3 backend instances

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

## Contributing Back

Found a cool visualization? Share it!

1. Create a new branch
2. Add your visualization
3. Test thoroughly
4. Submit a pull request

## Resources

- [MITRE ATT&CK](https://attack.mitre.org)
- [Phaser.js Docs](https://photonstorm.github.io/phaser3-docs/)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Falco Rules](https://falco.org/docs/rules/)

Happy hacking! 🎮🛡️
