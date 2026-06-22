# VULNERABILITY: Demonstrating insecure usage of vulnerable library versions

import yaml       # PyYAML 5.1 - CVE-2020-14343
import requests   # requests 2.6.0 - CVE-2015-2296
from flask import Flask, request, jsonify

app = Flask(__name__)   # Flask 0.12.2 - CVE-2018-1000656

# VULNERABILITY: yaml.load() without Loader allows RCE
# Attack: !!python/object/apply:os.system ['id']
@app.route('/api/import_config', methods=['POST'])
def import_config():
    config_data = request.data.decode()
    config = yaml.load(config_data)   # CVE-2020-14343 - use yaml.safe_load() instead
    return jsonify({'imported': True, 'keys': list(config.keys()) if config else []})

# VULNERABILITY: Pillow processing untrusted images with heap overflow CVE
@app.route('/api/resize_image', methods=['POST'])
def resize_image():
    from PIL import Image   # Pillow 8.1.0 - CVE-2021-25287
    import io
    uploaded = request.files.get('image')
    img = Image.open(io.BytesIO(uploaded.read()))   # Crafted TIFF triggers heap overflow
    img = img.resize((100, 100))
    return jsonify({'width': img.size[0], 'height': img.size[1]})

# VULNERABILITY: Requests with SSL verification disabled + vulnerable version
@app.route('/api/fetch_external', methods=['POST'])
def fetch_external():
    data = request.get_json()
    url = data.get('url')
    resp = requests.get(url, verify=False)   # urllib3 CVE-2019-11324
    return jsonify({'status': resp.status_code, 'content': resp.text[:500]})

# VULNERABILITY: SQLAlchemy raw query (CVE via 1.3.0 known issues)
@app.route('/api/query', methods=['GET'])
def raw_query():
    from sqlalchemy import create_engine, text
    engine = create_engine('sqlite:///app.db')
    user_input = request.args.get('filter', '')
    # Raw query construction with vulnerable SQLAlchemy version
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM users WHERE name = '{user_input}'"))
        return jsonify([dict(row) for row in result])

if __name__ == '__main__':
    app.run(debug=True, port=5006)
