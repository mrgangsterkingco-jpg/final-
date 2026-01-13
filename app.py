from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

# 🔥 শক্তিশালী সার্ভার লিস্ট (Backup System)
# একটি কাজ না করলে অটোমেটিক অন্যটি কাজ করবে
COBALT_INSTANCES = [
    "https://cobalt.pub",           # Server 1 (Best)
    "https://api.succoon.net",      # Server 2 (Backup)
    "https://api.cobalt.tools"      # Server 3 (Official)
]

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "system": "Yousave Core v10",
        "message": "Engine is running with Multi-Server support."
    })

@app.route('/api/engine', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        
        url = data.get('url')
        quality = data.get('quality', 'max')
        format_type = data.get('format', 'video')

        if not url:
            return jsonify({"status": "error", "text": "No URL provided"}), 400

        # নতুন v10 কনফিগারেশন
        payload = {
            "url": url,
            "videoQuality": quality,     # v7 এর vQuality এখন videoQuality হতে পারে
            "audioFormat": "mp3",
            "downloadMode": "audio" if format_type == 'audio' else "auto",
            "youtubeVideoCodec": "h264",
            "tiktokFullAudio": True,
            "alwaysProxy": False
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # লুপ চালিয়ে সব সার্ভার চেক করা হবে
        last_error = None
        
        for base_url in COBALT_INSTANCES:
            try:
                # সার্ভার URL ঠিক করা (Slash handling)
                api_url = f"{base_url.rstrip('/')}"
                
                print(f"Trying server: {api_url}") # Logs for debugging
                
                response = requests.post(
                    api_url, 
                    json=payload, 
                    headers=headers, 
                    timeout=15 # ১৫ সেকেন্ড টাইমআউট
                )
                
                # যদি রেসপন্স সফল হয়
                if response.status_code == 200:
                    result = response.json()
                    
                    # Cobalt v10 response structure check
                    if result.get('status') in ['stream', 'redirect', 'picker', 'tunnel']:
                         return jsonify(result)
                    
                    if result.get('url'): # সরাসরি URL পেলে
                        return jsonify({"status": "stream", "url": result.get('url')})
                        
            except Exception as e:
                print(f"Server {base_url} failed: {str(e)}")
                last_error = str(e)
                continue # পরের সার্ভারে যাও

        # সব সার্ভার ফেইল করলে
        return jsonify({
            "status": "error", 
            "text": "All servers are busy. Please try again in 1 minute."
        }), 500

    except Exception as e:
        return jsonify({"status": "error", "text": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
