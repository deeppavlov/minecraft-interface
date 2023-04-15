import json
import argparse
from flask import Flask, request
from flask import jsonify

from game import execute, prepare_game, interception_data

app = Flask(__name__)
idata = None

@app.route('/move', methods = ['POST'])
def move():
    data = request.get_data().decode('utf-8')
    
    # if 'dir' in data.keys:
    #     game.execute(data['dir'])
    # if 'cam' in data.keys:
    #     game.execute(data['cam'])
        
    execute(idata, data)

    return jsonify({"status": f"recieved {data}"})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--port')
    args = parser.parse_args()
    idata = interception_data(*prepare_game())
    app.run(host=args.ip, port=int(args.port), debug=True, use_reloader=False)