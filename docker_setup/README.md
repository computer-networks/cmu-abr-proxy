# Development Environment
## Introduction
This is the files to build a Docker image that have all the dependencies you need for project 3. Before starting to install this, you should have installed docker in your machine. With Docker, you could build a development image using these files or get one from DockerHub. After you have the development image, you could open a container of this image and then finish your project inside. You could use port mapping to watch video outside of a container. It is recommended to read [Docker Document](https://docs.docker.com/) to have a basic understanding of what is docker doing and how to use it. 

## Installation Step
  1. Install Docker, if you get this image from DockerHub, go to step 4.
  2. Enter this directory inside a command line terminal.
  3. Run `docker build -t 15441-project3:latest -f ./DockerFile .`, it may takes a few mintues to build the image. You could use `docker images` to check images you have in your docker.
  4. Now you have the image, you could run 
  `docker run -it -p 7778:7778 -p 7779:7779 15441-project3:latest /bin/bash` to run a container inside your machines with port mapping at port number 7778 and 7779. With port mapping, you could access port 7778 and 7779 of your container from your machine's web browser outside. You could find more info at [Docker Document](https://docs.docker.com/config/containers/container-networking/) in port mapping.
  
## Usage
  ### 1. Container
  * You could use command `docker ps` to check all the running container and their ID and status.
  * You could use CTRL+D to exit a container. Note that exiting a container will stop it but **not** remove it, you could still find it using command `docker ps -a`. If you want to enter that container again, you could use command `docker start <CONTAINER_ID>` and `docker attach <CONTAINER_ID>` to enter that container again.
  * The file inside container will be kept if you exit a container, it could still find them by the time you re-enter that container. **Pay attention that you will lose all files inside container by the time you remove your container using `docker rm <CONTAINER_ID>`, so be sure you push your code or copy it outside before you remove your container.**
  * You could find more info about container at [Get Started](https://docs.docker.com/get-started/) and more command at [Docker Document](https://docs.docker.com/engine/reference/commandline/container/)
  ### 2. Netsim
  * Netsim is the tools used to provide a simulated network environment locate at `/autograder/netsim` inside container, which contains video content apache servers and the bandwidth limited link in front of the servers.
  * It provide three topologies: **onelink**, **twolink** and **sharelink**. It also has a topology called **servers** to provide multiple servers without bandwidth limitation according to a servers port file specified by `-s`. You could find detailed decription in [writeup](https://www.overleaf.com/project/5e8e2e175cc9d70001c08adb).
  * You could start, stop or restart the network using command like 
    ```
    ./netsim.py {onelink,twolink,sharelink} {start,stop,restart}
    ```
    
    or 
    
    ```
    ./netsim.py servers {start,stop,restart} -s {port file}
    ```
    For example, `./netsim.py sharelink start` would start a new sharelink topology inside container. You could find some port file inside `./servers` directory.
  * You also could use the `run` command in netsim to change the bandwidth of links according to a event file. You should run command like 
    ```
    ./netsim.py {onelink,twolink,sharelink} {run} -e EVENTS_FILE
    ```
    We provide two sample event files, but feel free to create your own events files and test your implementation with it. We recommend you to do so. Noted that in **servers** topology, the Netsim are not limiting the bandwidth of each server, so it you can't run event file when using **servers** topology.
    
  ### 3. Multiple terminal
  * Sometimes you may need to run multiple command terminal for a container, you could use following command to do that.
  ```
  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
  ```
  * For example, `docker exec -it a12a00861c4a /bin/bash` would open a new terminal for container whose ID is `a12a00861c4a`, you could use `docker ps` to check all the running containers. You could find more info at [Docker Document](https://docs.docker.com/engine/reference/commandline/exec/) in running command terminal.
  ### 4. Use browser outside of your container
  * You could use your own browser in your machine to access port inside container if you do the port mapping correctly. Note that if you're using Google Chrome, you need to allow flash player to watch the video.
  ### 5. File transfer in container
  * You may lose your data by the time you terminate your 
  * To copy the file into or out from your container, you could use command:
    ```
    docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
    docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
    ```
    You could refer to [Docker Document](https://docs.docker.com/engine/reference/commandline/cp/) for more info.
  * Another way to share file with container is by using `bind mounts` or `volume`, which are like a shared folder between your machine and container. You could specify a mapping by the time you start your container using `docker run`. For example,
  `docker run -it -p 7778:7778 -p 7779:7779 -v /tmp:/home 15441-project3:latest /bin/bash` will replace the contents of the container’s `/home/` directory with the `/tmp/` directory on your machine. Note that you shouldn't replace the directory which contains the file we provided. You could find more info about this at [Docker Document](https://docs.docker.com/storage/bind-mounts/).
  ### 6. Load Generator
  * For checkpoint 2 and 3, we create a simple load generator inside `/autograder/netsim/` called `loadgen.py` to simulate the load in the real life. The load generator will send HTTP request to fetch video chunk from a target port and its access pattern is defined in a load event file.
  * You could use command below to run the load generator:
    ```
    ./loadgen.py -e {load event file}
    ```
    It also has some arguments like `-v` or `-l` to provide more detailed output or log.
  * We provided some sample load event files in `./loads` directory. But it is recommended that you write you own load event and test with the load you created. Please refer to instructions inside `.load` file and [writeup](https://www.overleaf.com/project/5e8e2e175cc9d70001c08adb) to write new loads event file.
  ### 7. Load Monitor
  * To measure the load generated by load generator, we also provide a load monitor inside `/autograder/netsim/` called `monitor.py` to calculate the load for each server. It takes the same port file you used in Netsim **servers** topology and will monitor the load on these ports. You could use `CTRL + C` to stop the load monitor and it will print out the load on each server.
  * You could commmand below to run the load monitor:
    ```
    ./monitor.py -s {port file}
    ```
  * We recommand you use Load Monitor to measure your load balancer and maybe calculate the [Jain Fairness Index](https://en.wikipedia.org/wiki/Fairness_measure) using the load on each server. It is the way we test your load balancer implementation.
