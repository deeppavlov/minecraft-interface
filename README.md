# Mint-connector

### Launch instructions (agent=telegram)

Step 1: Fill in the TG_TOKEN environment variable by executing `export TG_TOKEN=...` in your shell;
Step 2: Make sure that the proxy addresses are correct if you want to use proxy: `assistant_dists/dream_mint/proxy.yml`;
Step 3: Launch the mint distribution of dream `assistant_dists/dream_mint` using the following command (warning! all running docker containers are going to be killed when you stop dream or `Ctrl+C`): `docker-compose -f docker-compose.yml -f assistant_dists/dream_mint/docker-compose.override.yml -f assistant_dists/dream_mint/dev.yml -f assistant_dists/dream_mint/proxy.yml up --build --force-recreate; docker stop $(docker ps -aq)`. This command launches the mint distribution of dream using proxy for all containers that are specified in `assistant_dists/dream_mint/proxy.yml`;
Step 4: (Preferably on a separate machine) clone this repository, choose the connector you wish to use. Launch the corresponding game/program/project, execute the following command from inside your local clone of this repo: `python server.py --ip 0.0.0.0 --server_ip CONN_IP --server_port CONN_PORT --port LOCAL_PORT --conn CONNECTOR`, where `CONN_PORT` is a public port from the machine that hosts dream. You may have to tikner a bit with this port, as it is used to make the ROS-Flask container accessible from anywhere in the world. Ask your network administrator to map the port 5000 on the machine hosting dream to any public available port (for example: 10000). You don't have to change anything in dream, but you would have to use your own `CONN_IP` and `CONN_PORT` (again, ask your network admin). `LOCAL_PORT` — doesn't really matter, but it has historically been set to 8339. `CONNECTOR` is the name of the python module with implementations of commands. `--conn game_minecraft` for example.
Step 5: Use your telegram bot to communicate with the game/program/project you chose earlier. For example: if you chose minecraft connector, enter a world, and message your bot "move forward" from your smartphone or any other device. Your character should move forward and the bot should reply whether it is executing the command or if something went wrong.

P.S. There are many things that can go wrong when trying to use the instructions above, because dream is constantly evolving. So in future these instructions may universally work or they may have a few missing steps. But usually it all boils down to looking and poking around in the distribution config files (look closely at the command in step 3, almost all most important config files are specified there).

### An important note

If you're using minecraft, you should turn off autopause on unfocus using the following combination: *F3 + P*.