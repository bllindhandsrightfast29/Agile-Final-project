# Quick Start Guide

Get the Cyber Defense Visualization System running in 5 minutes!

## Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ (for local development)

## Option 1: Docker (Recommended)

### 1. Start the system

```bash
chmod +x start.sh
./start.sh docker
```

### 2. Open your browser

Navigate to: **http://localhost:3000**

### 3. Start visualizing!

- Select a technique from the dropdown
- Click "Simulate Attack"
- Watch the retro 2D visualization!

That's it! 🎮

## Option 2: Local Development

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start backend

```bash
cd backend
python main.py
```

### 3. Start frontend (new terminal)

```bash
cd frontend
python -m http.server 3000
```

### 4. Open browser

Navigate to: **http://localhost:3000**

## First Steps

### Try These Demo Scenarios:

1. **Privilege Escalation** - Watch a user climb to root!
2. **Lateral Movement** - See attackers move between systems
3. **Credential Theft** - Pacman-style credential collection
4. **Data Exfiltration** - Watch data flow to attacker servers

### Select Individual Techniques:

1. Click the "Select a technique..." dropdown
2. Choose from 400+ MITRE ATT&CK techniques
3. Click "Simulate Attack"
4. Read the narration to understand what's happening

## Enhanced Features (Optional)

### Add AI Narration

1. Get an Anthropic API key from https://console.anthropic.com
2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
3. Add your key:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```
4. Restart the system

Now you'll get Khan Academy-style explanations!

### Enable Falco Integration

For real-time Docker security monitoring:

1. Install Falco: https://falco.org/docs/install/
2. Uncomment Falco service in `docker-compose.yml`
3. Restart: `docker-compose up -d`

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Or use a different port
PORT=8080 python backend/main.py
```

### Frontend shows "disconnected"
- Make sure backend is running on port 8000
- Check browser console for errors
- Verify WebSocket connection

### Docker issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f backend
```

## What's Next?

- Explore the codebase to understand attack visualization
- Add your own custom attack scenarios in `data/attack_scenarios/`
- Customize sprite visualizations in `frontend/game/sprites.js`
- Integrate with your own security tools
- Use for security training and education!

## Need Help?

- Check README.md for full documentation
- Review code comments for implementation details
- Open an issue if you find bugs

Happy visualizing! 🎮🛡️
