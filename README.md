# Project 3, Checkpoint 1: Adaptive Bitrate Proxy

## Introduction
The `docker_setup` directory contains the files to build a Docker image for this project. You will use port mapping to watch video using your web browser outside of the container. It is recommended to read the [Docker documentation](https://docs.docker.com/) to have a basic understanding of what is Docker doing and how to use it. 


## Installation
1. Install Docker.
2. Navigate inside the `docker_setup` directory.
3. Run `docker build -t 15441-project3:latest -f ./DockerFile .`. It may takes a few mintues to build the image. You can use `docker images` to check images you have already built.
4. Now that you have the image, you can run 
`docker run -it -p 7778:7778 -p 7779:7779 15441-project3:latest /bin/bash` to launch a container inside your machines with port mapping configured for ports 7778 and 7779. With port mapping, you can access ports 7778 and 7779 of your container from your machine's web browser. These port numers are just an example. You may need to map other ports instead. You can find more info in the [Docker networking documentation](https://docs.docker.com/config/containers/container-networking/).


## Docker Usage
* You can use the command `docker ps` to check all the running containers (ID and status).
* You can use Ctrl-D to exit a container. Note that exiting a container will stop it but **not** remove it. You can still find it using the command `docker ps -a`. If you want to enter that container again, use the commands `docker start <CONTAINER_ID>` and `docker attach <CONTAINER_ID>`.
* The files inside a container will be preserved if you exit the container. ***Warning: If you remove your container with `docker rm <CONTAINER_ID>`, then all of your files will be deleted.***
* You can find more info about Docker [here](https://docs.docker.com/get-started/) and [here](https://docs.docker.com/engine/reference/commandline/container/).


## Netsim
* Netsim is the tool we use to provide a simulated network environment inside the container. The environment contains Apache servers with video content and the bandwidth-limited link in front of the servers.
* We provide three topologies: **onelink**, **twolink** and **sharelink**.
* You can start, stop, or restart the network using the terminal:
```
./netsim.py {onelink,twolink,sharelink} {start,stop,restart}
```
For example, `./netsim.py sharelink start` would start a new sharelink topology inside the container.
* You can use the `run` command in netsim to change the bandwidth of links according to an event file:
```
./netsim.py {onelink,twolink,sharelink} {run} -e EVENTS_FILE
```
We provide two sample event files, but feel free to create your own event files to test your implementation.


## Multiple terminals
* Sometimes you may need to run multiple command terminals inside a container. You can use the following command to do that:
```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```
* For example, `docker exec -it a12a00861c4a /bin/bash` would open a new terminal for container whose ID is `a12a00861c4a`. You can find more info [here](https://docs.docker.com/engine/reference/commandline/exec/).


## Use browser outside of your container
* You can use your own browser in your machine to access ports inside the container. Note that if you're using Google Chrome, you need to allow flash player to watch the video.


## File transfer in container
To copy files into or out from your container, you use:
```
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
```
Refer [here](https://docs.docker.com/engine/reference/commandline/cp/) for more info.
* Another way to share a file or directory with a container is by using `bind mounts` or `volume`, which are like a shared folder between your machine and the container. You can specify such a mapping when you start your container using `docker run`. For example,
`docker run -it -p 7778:7778 -p 7779:7779 -v /tmp:/home 15441-project3:latest /bin/bash` will replace the contents of the container’s `/home/` directory with the `/tmp/` directory on your machine. Note that you shouldn't replace the directory which contains the files we provided. You can find more info about this [here](https://docs.docker.com/storage/bind-mounts/).


## Starter Proxy Code

The `starter_proxy` directory contains some code to help you get started with 15-441/641 Project 3. See the project handout for a detailed description of the proxy's command line arguments. 


### File Description

- `proxy.c`: Contains the major network and multiplexing related code
- `httpparser.c`: Contains some HTTP parsing and header value extraction code
- `customsocket.c` Contains some helper functions for creating sockets
- `grapher.py`: Generate plots for CP1 writeup. Usage: python grapher.py \<netsim log\> \<proxy1 log\> \<proxy2 log\>


### Minimal example of running the proxy:

1. Run `echo_server.py`. By default it listens on (127.0.0.1, 10000) - please note that this requires python 3 or above
2. Run `make` in the root directory
3. Run `./proxy` by default it listens on (127.0.0.1, 8888)
4. Run `telnet localhost 8888` to test with telnet
