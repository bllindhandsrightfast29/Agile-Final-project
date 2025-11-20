#!/usr/bin/env python3
"""
Simple HTTP server for testing on mobile devices
Serves the frontend and proxies API requests to backend
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse
from http.server import SimpleHTTPRequestHandler

PORT = 3000

class MobileTestServer(SimpleHTTPRequestHandler):
    """HTTP server that serves frontend files"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="frontend", **kwargs)

    def end_headers(self):
        # Add CORS headers for mobile testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        # Cache control for development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"📱 {self.address_string()} - {format % args}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 60)
    print("🎮 Cyber Defense Visualization - Mobile Test Server")
    print("=" * 60)
    print()

    # Get local IP for mobile access
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"📍 Access on your Android device:")
        print(f"   http://{local_ip}:{PORT}")
        print()
        print(f"💻 Access on this computer:")
        print(f"   http://localhost:{PORT}")
        print()
    except:
        print(f"💻 Access at: http://localhost:{PORT}")
        print()

    print("📝 Note: Make sure your Android device is on the same WiFi network!")
    print()
    print("⚠️  Backend API at http://localhost:8000 must be running separately")
    print("   Start it with: cd backend && python main.py")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    with socketserver.TCPServer(("0.0.0.0", PORT), MobileTestServer) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped")
            sys.exit(0)


if __name__ == "__main__":
    main()
