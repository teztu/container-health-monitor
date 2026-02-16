# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Video Platform Monitor</h1>
    <p>Status: Running ✅</p>
    <p>Environment: Production</p>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "monitor"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
