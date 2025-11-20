# 📱 Mobile Viewing Guide

How to view the Cyber Defense Visualization System on your Android phone!

## Quick Demo (No Backend Required!)

The easiest way to view on mobile:

### Option 1: Standalone Mobile Demo

1. **Open on your Android phone:**
   - Navigate to: `frontend/mobile-demo.html` directly in your browser
   - Or use the mobile test server (instructions below)

2. **Works completely offline!**
   - No backend needed
   - 4 pre-built demo scenarios
   - Full touch controls

### Option 2: Mobile Test Server

If you have Python on your computer:

```bash
# On your computer (same WiFi as your phone)
python mobile-server.py
```

This will show you an IP address like:
```
📍 Access on your Android device:
   http://192.168.1.XXX:3000/mobile-demo.html
```

Open that URL on your Android phone!

## Full System with Backend

To use all 400+ MITRE techniques:

### Step 1: Start Backend on Computer

```bash
# Terminal 1
cd backend
python main.py
```

### Step 2: Start Frontend Server

```bash
# Terminal 2
python mobile-server.py
```

### Step 3: Get Your Computer's IP

On your computer:
- **Windows**: `ipconfig` (look for IPv4 Address)
- **Mac/Linux**: `ifconfig` or `hostname -I`

Example: `192.168.1.100`

### Step 4: Open on Android

On your phone's browser:
```
http://YOUR_IP:3000
```

Example: `http://192.168.1.100:3000`

**Important:** Your phone must be on the same WiFi network!

## Hosting in the Cloud (Access from Anywhere!)

Since you're using Claude Code on the web, you can also:

### Option A: Use Cloud Service

Deploy to services that give you a public URL:

1. **Replit** (easiest):
   ```bash
   git clone <your-repo>
   # Replit will auto-detect and run
   ```

2. **Railway**:
   ```bash
   railway up
   ```

3. **Render** (free tier):
   - Connect your GitHub repo
   - Auto-deploys on push

### Option B: Share Local Network

Use tools like:
- **ngrok**: `ngrok http 3000`
- **localtunnel**: `lt --port 3000`

This gives you a public URL you can access from anywhere!

## Mobile Features

✅ **Responsive Design**
- Automatically scales to your screen size
- Touch-friendly buttons (48px minimum)
- Optimized font sizes

✅ **Touch Controls**
- Tap to select scenarios
- Smooth scrolling
- No hover effects (touch-optimized)

✅ **Performance**
- Phaser.js auto-scales game canvas
- Works on older Android devices
- Minimal data usage

## Troubleshooting

### Can't connect to backend

**Solution 1:** Use the mobile demo (no backend needed!)
```
Open: frontend/mobile-demo.html
```

**Solution 2:** Check firewall
```bash
# Allow port 8000 and 3000
# Windows: Windows Defender Firewall
# Mac: System Preferences > Security > Firewall
```

### Game canvas too small

The game auto-scales, but if it's too small:
- Rotate to landscape mode
- Zoom out in browser
- Try full-screen mode

### Connection refused

Make sure:
1. Phone is on same WiFi as computer
2. Computer firewall allows connections
3. Using correct IP address (not 127.0.0.1)

### Slow performance

- Close other apps on phone
- Use mobile-demo.html (lighter version)
- Clear browser cache

## Best Viewing Experience

**Recommended:**
- Screen size: 5"+ (works on smaller too)
- Orientation: Portrait for controls, Landscape for game
- Browser: Chrome or Firefox
- Connection: WiFi (not required for demo)

**Tips:**
- Add to home screen for app-like experience
- Use landscape mode for better game view
- Enable "Request desktop site" if issues occur

## Offline Mode

The mobile demo works completely offline:

1. **One-time setup:**
   ```bash
   # Save the frontend folder to your phone
   # Or host it and cache it
   ```

2. **Open anytime:**
   - No internet needed
   - All demos work
   - Perfect for demos/presentations

## Testing Without Phone

Use browser dev tools:

1. Open browser (Chrome/Firefox)
2. Press F12
3. Click "Toggle Device Toolbar"
4. Select "Galaxy S20" or similar
5. Refresh page

## URLs Quick Reference

**Mobile Demo (Offline):**
```
file:///path/to/frontend/mobile-demo.html
```

**Local Network:**
```
http://YOUR_IP:3000/mobile-demo.html
http://YOUR_IP:3000/index.html (full version)
```

**Backend API:**
```
http://YOUR_IP:8000
```

## Questions?

- **No backend available?** → Use mobile-demo.html
- **Can't get IP?** → Use cloud hosting (Replit, Railway)
- **Phone not on WiFi?** → Use mobile hotspot or cloud hosting
- **Need to demo offline?** → Save mobile-demo.html to phone

Happy mobile hacking! 📱🎮🛡️
