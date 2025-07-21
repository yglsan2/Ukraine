#!/usr/bin/env python3
"""
Test simple de l'API RagTime optimisée
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json
import numpy as np
from datetime import datetime

# NumpyEncoder simplifié
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

app = Flask(__name__)
CORS(app)
app.json_encoder = NumpyEncoder

@app.route('/api/health', methods=['GET'])
def health_check():
    """Test de santé simple"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'RagTime API Test',
        'numpy_test': np.float32(3.14)  # Test du NumpyEncoder
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test avec des types numpy"""
    test_data = {
        'float32': np.float32(3.14),
        'int64': np.int64(42),
        'array': np.array([1, 2, 3]),
        'bool': np.bool_(True)
    }
    return jsonify(test_data)

if __name__ == '__main__':
    print("🚀 Démarrage API de test...")
    print("📊 NumpyEncoder activé")
    print("🌐 CORS activé")
    app.run(host='0.0.0.0', port=5000, debug=False) 