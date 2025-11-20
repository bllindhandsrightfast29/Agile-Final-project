# Cyber Defense Visualization System 🎮🛡️

> **"Khan Academy meets Cybersecurity"** - Visual storytelling for 400+ MITRE ATT&CK techniques

## What is This?

An educational cybersecurity visualization tool that creates **real-time animated "movies"** of cyber attacks and defenses. Think retro 2D games (Pacman, Snake, NES-style) but for learning how attacks work.

## Features

- 🎬 **Real-time Attack Visualization**: Watch attacks happen as 2D animations
- 📚 **400+ MITRE ATT&CK Techniques**: Visual explanations for every technique
- 🎮 **Retro Game Style**: Low-level 2D animation (NES, Pacman, Frogger aesthetic)
- 🎤 **AI Narration**: Storyteller that explains what's happening
- 🐳 **Falco Integration**: Watches Docker container events in real-time
- 🔴 **Red Team Scenarios**: Visualize atomic red team attacks

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Falco Docker   │─────▶│  Python Backend  │─────▶│  2D Game Engine │
│  (Events)       │      │  (FastAPI)       │      │  (Phaser.js)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │                           │
                                │                           │
                         ┌──────▼──────┐           ┌────────▼────────┐
                         │  MITRE      │           │  Visual         │
                         │  ATT&CK DB  │           │  Storytelling   │
                         └─────────────┘           └─────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Run the System

```bash
# Terminal 1: Start backend
python backend/main.py

# Terminal 2: Start frontend dev server
cd frontend
npm run dev
```

### 3. Open Browser

Navigate to `http://localhost:3000` and watch the cybersecurity movie!

## Example Visualizations

### Parameter Exploitation
```
[User Input] ──▶ [Web Server] ──▶ [💉 Malicious Payload]
                     │
                     ▼
              [🔓 System Access]
```

### Privilege Escalation
```
[👤 Low Privilege User]
         │
         ▼
    [🪜 Exploit]
         │
         ▼
[👑 Root Access]
```

## Configuration

Create `.env` file:

```env
# API Keys (optional for enhanced narration)
ANTHROPIC_API_KEY=your_key_here

# Falco Configuration
FALCO_SOCKET_PATH=/var/run/falco.sock

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server
│   ├── mitre_loader.py      # MITRE ATT&CK data loader
│   ├── visualizer.py        # Attack-to-visual mapper
│   ├── falco_listener.py    # Falco event listener
│   └── narrator.py          # AI storytelling engine
├── frontend/
│   ├── index.html           # Main visualization page
│   ├── game/
│   │   ├── engine.js        # Phaser.js game engine
│   │   ├── sprites.js       # Attack sprites/animations
│   │   └── scenes.js        # Battle scenes
│   └── style.css            # Retro styling
├── data/
│   └── attack_scenarios/    # Pre-built attack scenarios
└── docker-compose.yml       # Full stack deployment
```

## Technologies

- **Backend**: Python, FastAPI, WebSockets
- **Frontend**: HTML5 Canvas, Phaser.js (2D game engine)
- **Data**: MITRE ATT&CK Framework
- **Security**: Falco Docker runtime security
- **AI**: Anthropic Claude (narration)

## Development

This is an educational tool for learning cybersecurity concepts through visual storytelling. Perfect for:
- Security training
- Red team/blue team exercises
- CTF explanations
- Security awareness education

## License

MIT License - Educational use encouraged!
