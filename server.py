import argparse
import threading
import requests
import time

from flask import Flask

from game import execute, COMMANDS#, prepare_game, interception_data


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
        r = requests.request("POST", f"https://{server}/recieve_commands")
        print(f"request status: {r.status_code}")
        cmd = r.json() if 200 <= r.status_code <= 299 else None
        if cmd.replace("_", " ") in COMMANDS:
            EXECUTING = execute(idata, cmd)
        time.sleep(REQUEST_WAIT_TIME)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--server_ip')
    parser.add_argument('--server_port')
    args = parser.parse_args()
    #idata = interception_data(*prepare_game())
    print("sending commands list to ros-server")
    r = requests.request("POST", f"https://{args.server_ip}/set_commands", json={'commands': COMMANDS})
    print(f"commands sent, status = {r.status_code}")
    threading.Thread(recieve_commands(args.server_ip, args.server_port))
    app.run(host=args.ip, port=int(args.port), debug=True, use_reloader=False) # debug mode wants to run flask in main thread
