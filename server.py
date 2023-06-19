import argparse
import threading
import requests
import time

from flask import Flask

#TODO: import modules based on cli args
from game_minecraft import execute, COMMANDS, prepare_game, interception_data


REQUEST_WAIT_TIME = 3
EXECUTING = None


app = Flask(__name__)
idata = None


@app.route("/is_command_performed", methods=["POST"])
def is_command_performed():
    return {"result": True if EXECUTING.is_alive() else False}


def recieve_commands(server, port):
    global EXECUTING
    while True:
        print("recieving commands from dream...")
        headers = {'Accept': 'application/json'}
        r = requests.post(url=f"http://{server}:{port}/recieve_command", headers=headers)
        print(f"request status: {r.status_code}")
        recv_cmd = r.json()['command'] if 200 <= r.status_code <= 299 else ""
        print(f"recieved: {recv_cmd}")
        for command in COMMANDS:
            if recv_cmd and command in recv_cmd:
                EXECUTING = execute(idata, command)
                break
        time.sleep(REQUEST_WAIT_TIME)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--server_ip')
    parser.add_argument('--server_port')
    args = parser.parse_args()
    idata = interception_data(*prepare_game())
    print(f"sending commands list to ros-server: {COMMANDS}")
    r = requests.request("POST", f"http://{args.server_ip}:{args.server_port}/set_commands", json={'commands': COMMANDS})
    print(f"commands sent, status = {r.status_code}")
    threading.Thread(recieve_commands(args.server_ip, args.server_port))
    app.run(host=args.ip, port=int(args.port), debug=True, use_reloader=False) # debug mode wants to run flask in main thread
