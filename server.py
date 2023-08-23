import argparse
import threading
import requests
import time
import importlib

from flask import Flask


COMMANDS: list = []
execute: callable = lambda: True


REQUEST_WAIT_TIME = 3
EXECUTING = None


app = Flask(__name__)
idata = None


@app.route("/is_command_performed", methods=["POST"])
def is_command_performed():
    return {"result": True if EXECUTING.is_alive() else False}


def receive_commands(server, port):
    global EXECUTING
    while True:
        print("receiving commands from dream...")
        headers = {'Accept': 'application/json'}
        r = requests.post(url=f"http://{server}:{port}/receive_command", headers=headers)
        print(f"request status: {r.status_code}")
        recv_cmd = r.json()['command'] if 200 <= r.status_code <= 299 else ""
        print(f"received: {recv_cmd}")
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
    parser.add_argument('--conn')
    args = parser.parse_args()
    if args.conn == "game_minecraft":
        interception_data: callable = importlib.import_module(args.conn).interception_data
        prepare_game: callable = importlib.import_module(args.conn).prepare_game
        idata = interception_data(*prepare_game())

    COMMANDS = importlib.import_module(args.conn).COMMANDS
    execute = importlib.import_module(args.conn).execute

    print(f"sending commands list to ros-server: {list(COMMANDS.keys())}")
    r = requests.request("POST", f"http://{args.server_ip}:{args.server_port}/set_commands", json={'commands': list(COMMANDS.keys())})
    print(f"commands sent, status = {r.status_code}")
    threading.Thread(receive_commands(args.server_ip, args.server_port))
    app.run(host=args.ip, port=int(args.port), debug=True, use_reloader=False) # debug mode wants to run flask in main thread
