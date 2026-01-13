from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

# 🔥 নতুন এবং শক্তিশালী সার্ভার লিস্ট (Backup System)
# wuk.sh এবং cobalt.pub এখন সবচেয়ে ভালো কাজ করছে
INSTANCES = [
    "https://co.wuk.sh",            # Server 1 (Super Stable)
    "https://cobalt.pub",           # Server 2
    "https://api.cobalt.tools",     # Server 3 (Official)
    "https://api.wuk.sh"            # Server 4
]

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "system": "Yousave Core v11",
        "message": "Engine is running with High-Stability Servers."
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

        # হেডারস (Browser-like headers to avoid blocking)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Origin": "https://co.wuk.sh",
            "Referer": "https://co.wuk.sh/"
        }

        # v10 API Payload structure
        payload = {
            "url": url,
            "videoQuality": quality,
            "audioFormat": "mp3",
            "downloadMode": "audio" if format_type == 'audio' else "auto",
            "youtubeVideoCodec": "h264",
            "alwaysProxy": False,
            "disableMetadata": True
        }

        # লুপ চালিয়ে সব সার্ভার চেক করা হবে
        last_error = None
        
        for base_url in INSTANCES:
            try:
                # ক্লিন URL তৈরি করা
                clean_base = base_url.rstrip('/')
                api_url = f"{clean_base}/api/json"
                
                print(f"Trying server: {api_url}") # Logs for debugging
                
                response = requests.post(
                    api_url, 
                    json=payload, 
                    headers=headers, 
                    timeout=15 # ১৫ সেকেন্ড টাইমআউট
                )
                
                # যদি রেসপন্স সফল হয় (200 OK)
                if response.status_code == 200:
                    result = response.json()
                    
                    # Cobalt response check
                    if result.get('status') in ['stream', 'redirect', 'picker', 'tunnel']:
                         return jsonify(result)
                    
                    if result.get('url'): # সরাসরি URL পেলে
                        return jsonify({"status": "stream", "url": result.get('url')})
                else:
                    print(f"Server {clean_base} error: {response.status_code}")
                        
            except Exception as e:
                print(f"Server {base_url} failed: {str(e)}")
                last_error = str(e)
                continue # পরের সার্ভারে যাও

        # সব সার্ভার ফেইল করলে এই মেসেজ দেখাবে
        return jsonify({
            "status": "error", 
            "text": "All servers are currently busy. Please try again in a few seconds."
        }), 500

    except Exception as e:
        return jsonify({"status": "error", "text": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
