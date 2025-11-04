# NEW CHANGES IN NEW BRANCH

# docker :school_satchel: :whale:

<div align="center">
	<img width="300" src="/resources/docker_meme_0.jpg">
</div>

<p align="center">
  <sub>- a teammate once said at a certain point in your life</sub>
</p>

Working on projects with crazy amount of dependencies cause issues depicted above, where portability breaks down. Docker is a great tool that solves these issues by allowing users to build images and containers that represent the ideal development environment for such projects or applications to run flawlessly.

I don't claim to be a Docker expert, however some of these layman concepts helped me greatly to understand the uses of Docker and what is happening under the hood.

In short, Docker is a tool that chisels a divide between the underlying kernel of your work station, and the rest of the required components for your application, this would normally include the OS, libraries and binaries. A good analogy would be that Docker separates the system kernel/hardware-land from the user-land.

I likened the kernel level to be more hardware oriented, and therefore you could run an application that requires `Ubuntu 16.04` using Docker on an `Ubuntu 18.04` machine with no problems at all.

There are however exceptions, for example GPU interfaces, drivers and compatibility would fall under hardware related operations, therefore more advanced features of Docker will be needed to work with any dockerized applications that required GUI or GPU computations.

These notes cover basic applications, while more advanced features of Docker should be referenced from their [documentation](https://docs.docker.com/). The focus here would be for `Linux` machines, however after the initial installation differences, the core ideas and commands should remain the same.

## Contents

- [Installation](#installation)
- [Docker images](#docker-images)
- [Docker containers](#docker-containers)
- [Removing docker images and containers](#removing-docker-images-and-containers)
- [Running docker container in the background](#running-docker-container-in-the-background)
- [Docker port mapping](#docker-port-mapping)
- [Docker mount](#docker-mount)
- [Create docker image example](#create-docker-image-example)

## Installation

Just in case there is an old version

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

Set up the dependencies, add and verify the key, before setting up the repository,

```bash
sudo apt update
sudo apt install apt-transport-https ca-certifications curl gnupg-agent software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

Install docker,

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Verify installation

```bash
sudo docker run hello-world
```

References [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

## Docker images

Docker images are the equivalent system images or virtual machine images, but starting from above the kernel level, while the latter ones contain the emulated kernels as well. This allows docker images to be relatively small, and depending on the application, should still work across multiple machines without a hitch.

Existing docker images on the system can be checked using,

```bash
docker images
```

Docker images can be created locally on your machine, or passed around, but the most common way to get a docker image is through [Docker Hub](https://hub.docker.com). They host a great number of docker images for all sorts of applications and environments.

To pull down a docker image, you would do this

```bash
docker pull ubuntu
```

To pull down a specific version/tag of a docker image, this could be done

```bash
docker pull ubuntu:17.10
```

Alternatively, you could run docker images regardless of having a copy of it or not, docker will help you pull it down if it can't find it on your machine,

```bash
docker run -it ubuntu
```

The above starts a new docker container from the image called `ubuntu`, and allows the user to interact with the dockerized OS through `bash`, due to the `i` flag which stands for interactive and `t` for `tty`.

To exit such a container, just use `Ctrl + d`.

The installation verification `hello-world` docker image is an example where no interaction is needed when running the docker image.

## Docker containers

Docker containers are spawned using docker images, each of them are enclosed instances and do not interact with each other, except for when ports and mounts are involved (which will be covered below).

To check existing containers and their statuses,

```bash
docker ps -a
```

After using `docker run -it ubuntu` or other `docker run` commands, the number of containers should have increased and the entry and exit statuses should also tally.

To restart an existing container, we first start it in the background then attach it to the currect terminal session,

```bash
docker start <container id>
docker attach <container id>
```

To restart the last created container,

```bash
docker start `docker ps -q -l`
docker attach `docker ps -q -l`
```

## Removing docker images and containers

To remove an existing container, get the container ID using `docker ps -a`, make sure it is stopped, then use the `docker rm` command,

```bash
docker stop <container id>
docker rm <container id>
```

In order to remove a docker image, all containers associated to that image needs to be removed as well. After the containers have been cleared away using `docker rm`, we use the `docker rmi` command,

```bash
docker rmi <image name>
```

For images with tags, we will append the suffix,

```bash

docker rmi <image name>:<tag name>
```

## Running docker container in the background

Running docker containers in the background is useful for applications that have a lifetime, a simple example using the `detach` flag,

```bash
docker run -d ubuntu sleep 30
```

This starts an `ubuntu` container in the background which does nothing and exits after 30 seconds automatically. This can be verified using the statuses reported on `docker ps -a`.

Users can also attach background docker containers into the current terminal session,

```bash
docker attach <container id>
```

## Docker exec

To execute commands within docker containers from the docker hosts, we can use the `exec` keyword,

```bash
docker exec <container id> cat ~/.bashrc
```

which should print out the `bashrc` configuration of the docker container.

## Docker port mapping

In order to have ongoing interaction with running docker containers, for example an `ubuntu` or `jenkins` container, we will need to map/connect the ports of the container and docker host. This will allow us to access port applications running on the docker container, for example,

```bash
docker run -p 8080:8080 jenkins
```

We can verify by going to `localhost:8080` on a browser. The first mention of `8080` is the docker host port, while the second is the default port that `jenkins` instance runs on.

## Docker mount

Docker containers and hosts do not share configurations or file systems, hence any changes made within a container will not be reflected on other same-image containers. One way to share databases or file systems between containers, is using `mount`.

A simple exercise to demonstrate this, we create a container using a database image `nouchka/sqlite3`, with access to the `bash` terminal of the container, with a volume driver tag mapping the host's `/root/hostdb` to the container's `/root/db`,

```bash
docker run -v /root/hostdb:/root/db -it --entrypoint=/bin/bash nouchka/sqlite3

# from within the container
sqlite3 test.db
# add stuff to the database
```

The database `test.db` should also be found on the host path, `/root/hostdb`.

## Create docker image example

Creating docker images will allow others easy access to your application. In this example a `hello-world` web application using `flask` will be created using the `ubuntu` docker image, after the installation of its dependencies.

We start by creating a `Dockerfile`,

```bash
mkdir ~/my_first_img
cd ~/my_first_img

vim Dockerfile
```

Populate the `Dockerfile` with commands as below,

```
FROM ubuntu

RUN apt update
RUN apt install -y python-pip
RUN pip install flask

COPY hello-world.py /hello-world.py

ENTRYPOINT FLASK_APP=hello-world.py flask run --host=0.0.0.0
```

We also created the `hello-world.py` script,

```bash
cd ~/my_first_img
vim hello-world.py
```

populate the script with,

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world! My first docker image created and running with a Flask based web app"

if __name__ == "__main__":
    app.run()
```

We can then start to create the docker image, named `test_web_app` designated by the `-t` flag, notice the final `.`, which calls to build the image using the `Dockerfile` within this current directory,

```bash
docker build -t test_web_app .
```

A whole bunch of stuff would start running, once its done, we can verify that the image has been built using `docker images`.

We can now run a docker container using that newly built docker image, which should start a `flask` web application,

```bash
docker run -p 5000:5000 -it test_web_app
```

Go to `localhost:5000` on any browser and it should display the string returned by the `flask` python script. :sparkles:
