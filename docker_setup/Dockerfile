# base image from gradescope
FROM gradescope/auto-builds:ubuntu-18.04

# make necessary directories
RUN mkdir -p \
    /var/www \
    /usr/local/apache2 \
    /home/click \
    /autograder/netsim

# copy launch and test scripts
ADD ./netsim /autograder/netsim

# copy apache binary, configuration and binary
ADD ./www /var/www

# copy video service contents
ADD ./apache2 /usr/local/apache2

# install click dependencies and useful tools
RUN apt-get update
RUN apt-get -y install net-tools psmisc gdb tcpdump build-essential python python-pip bison flex tmux telnet emacs vim iproute2 iperf3 tcpdump tshark

# install click
ADD ./click /home/click
RUN cd /home/click && \
    ./configure --enable-local && \
    make -j`nproc` elemlist && \
    make -j`nproc` install
