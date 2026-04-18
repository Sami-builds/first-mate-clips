#!/usr/bin/env python3
"""Simple video upload server for First Mate"""

import os
import http.server
import socketserver
from urllib.parse import parse_qs
import json

PORT = int(os.environ.get("PORT", 8080))
UPLOAD_DIR = "uploads"

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == "/upload":
            content_length = int(self.headers['Content-Length'])
            field_data = self.rfile.read(content_length)
            
            # Simple multipart parsing
            content_type = self.headers['content-type']
            boundary = content_type.split('boundary=')[1].encode()
            
            # Extract filename from multipart data
            if b'filename=' in field_data:
                # Write to file
                filename = f"video_{os.time.time()}.mp4"
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                # Find where video data starts (after headers)
                parts = field_data.split(b'\r\n\r\n')
                if len(parts) > 1:
                    video_data = parts[1]
                    # Remove trailing boundary
                    video_data = video_data.rsplit(b'--', 1)[0]
                    
                    with open(filepath, 'wb') as f:
                        f.write(video_data)
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True,
                        "file": filename,
                        "message": "Video uploaded successfully!"
                    }).encode())
                    return
        
        self.send_response(400)
        self.end_headers()

os.makedirs(UPLOAD_DIR, exist_ok=True)

with socketserver.TCPServer(("", PORT), UploadHandler) as httpd:
    print(f"🎬 Video Upload Server running at http://localhost:{PORT}")
    print(f"📁 Uploads saved to: {UPLOAD_DIR}")
    httpd.serve_forever()