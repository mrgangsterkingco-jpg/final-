from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# সব ডোমেইন থেকে এক্সেস দেওয়ার জন্য CORS অন করা হলো
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "system": "Yousave Core API",
        "message": "Engine is running smoothly."
    })

@app.route('/api/engine', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        
        # ইনপুট ডাটা নেওয়া
        url = data.get('url')
        quality = data.get('quality', 'max') # ডিফল্ট Max (4K/8K)
        format_type = data.get('format', 'video')

        if not url:
            return jsonify({"status": "error", "text": "No URL provided"}), 400

        # Cobalt API কনফিগারেশন (Ultimate Settings)
        payload = {
            "url": url,
            "vCodec": "h264",
            "vQuality": quality,
            "aFormat": "mp3",
            "isAudioOnly": (format_type == 'audio'),
            "isTTFullAudio": True,
            "dubLang": False,
            "disableMetadata": True
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # রিকোয়েস্ট পাঠানো (Server-less Process)
        response = requests.post('https://api.cobalt.tools/api/json', json=payload, headers=headers)
        result = response.json()

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "text": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
