import json
from flask import Flask, request
from flask import jsonify

import game

app = Flask(__name__)

@app.route('/move', methods = ['POST'])
def move():
    data = json.loads(request.get_data())
    
    if 'dir' in data.keys:
        game.execute(data['dir'])
    if 'cam' in data.keys:
        game.execute(data['cam'])
        
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)