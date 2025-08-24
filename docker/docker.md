Docker is an incredibly powerful platform that has revolutionized how developers build, ship, and run applications. It uses a concept called "containerization" to package an application and all its dependencies into a single, isolated unit.

Let's break down the core components and related concepts:

---

# Docker: The Containerization Platform

**What is Docker?**

Docker is an open-source platform that enables developers to automate the deployment, scaling, and management of applications using a technology called **containerization**. In simpler terms, Docker packages an application and all its dependencies (libraries, system tools, code, runtime) into a standardized unit called a **container**.

**Why Docker?**

*   **Consistency:** "It works on my machine" problem solved. The container includes everything needed, so it runs identically regardless of the underlying infrastructure.
*   **Isolation:** Containers isolate applications from each other and from the host system, preventing conflicts and improving security.
*   **Portability:** A Docker container can run on any system that has Docker installed – a developer's laptop, a test server, a production cloud, or a virtual machine.
*   **Efficiency:** Containers share the host OS kernel, making them much lighter and faster to start than traditional virtual machines.
*   **Scalability:** Easy to replicate and scale applications by simply running more instances of a container.

**Analogy:** Think of Docker as a standardized shipping container system. A physical shipping container can hold anything – clothes, electronics, food – and be shipped on any truck, train, or ship because its interface (size, locking mechanisms) is standardized. Docker containers work similarly for software.

---

# Docker Image

**What is a Docker Image?**

A Docker Image is a **read-only template** that contains a set of instructions for creating a container. It's essentially a snapshot of an application and its environment at a specific point in time. Images are built from a `Dockerfile`.

**Key Characteristics:**

*   **Read-Only:** Once built, an image cannot be changed. When you run a container from an image, Docker adds a thin, writable layer on top of the image.
*   **Layered File System:** Images are composed of multiple layers, each representing an instruction in the `Dockerfile`. This layering enables efficiency, as common layers can be shared between different images, and only changed layers need to be rebuilt/transferred.
*   **Blueprint:** An image is the blueprint; the container is the actual running instance built from that blueprint.

**Analogy:** An image is like a class in object-oriented programming, or a recipe for a cake. It defines what goes into the cake and how to make it, but it's not the cake itself.

**Example: Pulling and Listing Images**

You can pull pre-built images from Docker Hub (a public registry) or build your own.

**Input:**
```bash
docker pull ubuntu:latest
docker pull nginx:stable
docker images
```

**Output:**
```
# docker pull ubuntu:latest
Using default tag: latest
latest: Pulling from library/ubuntu
... (download progress) ...
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest

# docker pull nginx:stable
stable: Pulling from library/nginx
... (download progress) ...
Status: Downloaded newer image for nginx:stable
docker.io/library/nginx:stable

# docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
ubuntu        latest    97a337ae1365   3 weeks ago     77.9MB
nginx         stable    170f2ed2901a   3 weeks ago     136MB
hello-world   latest    d2c94e258dcb   3 months ago    13.3kB
```

---

# Docker Container

**What is a Docker Container?**

A Docker Container is a **runnable instance of a Docker Image**. It's a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.

**Key Characteristics:**

*   **Isolated:** Each container runs in isolation from other containers and the host system.
*   **Ephemeral (by default):** Changes made inside a container are lost when the container is removed, unless data is explicitly persisted using volumes.
*   **Portable:** Can run consistently on any environment that has Docker.
*   **Process:** When you run a container, you're essentially running a process (or processes) isolated from the rest of the system.

**Analogy:** A container is like an actual cake baked from the recipe (image), or an object created from a class.

**Example: Running and Managing Containers**

**Input:**
```bash
# Run an Nginx container and map port 80 of the container to port 8080 of the host
docker run -d -p 8080:80 --name my-nginx-container nginx:stable

# List running containers
docker ps

# Access the Nginx server (from your host machine's terminal)
# curl http://localhost:8080

# Stop the container
docker stop my-nginx-container

# List all containers (including stopped ones)
docker ps -a

# Remove the container
docker rm my-nginx-container
```

**Output:**
```
# docker run -d -p 8080:80 --name my-nginx-container nginx:stable
e7a8b6c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7

# docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
e7a8b6c9d0e1   nginx:stable   "/docker-entrypoint.…"   2 seconds ago   Up 1 second    0.0.0.0:8080->80/tcp   my-nginx-container

# curl http://localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
... (HTML content of Nginx default page) ...
</html>

# docker stop my-nginx-container
my-nginx-container

# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
# (No running containers listed)

# docker ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED              STATUS                      PORTS     NAMES
e7a8b6c9d0e1   nginx:stable   "/docker-entrypoint.…"   About a minute ago   Exited (0) 10 seconds ago             my-nginx-container

# docker rm my-nginx-container
my-nginx-container

# docker ps -a
# (No containers listed)
```

---

# Dockerfile

**What is a Dockerfile?**

A `Dockerfile` is a plain text file that contains a series of instructions and arguments used to **automatically build a Docker Image**. Each instruction in the `Dockerfile` creates a new layer in the image, making images lightweight and efficient.

**Key Instructions:**

*   **`FROM`**: Specifies the base image (e.g., `ubuntu`, `alpine`, `node`).
*   **`RUN`**: Executes commands in a new layer on top of the current image, committing the results. Used for installing packages, creating directories, etc.
*   **`COPY`**: Copies files/directories from the host to the image.
*   **`ADD`**: Similar to `COPY`, but can also extract tar files or fetch URLs.
*   **`WORKDIR`**: Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, or `ADD` instructions that follow it.
*   **`EXPOSE`**: Informs Docker that the container listens on the specified network ports at runtime. (Doesn't actually publish the port).
*   **`ENV`**: Sets environment variables.
*   **`CMD`**: Provides defaults for an executing container. Can be overridden when `docker run` is executed. Only the last `CMD` in a `Dockerfile` takes effect.
*   **`ENTRYPOINT`**: Configures a container that will run as an executable. `ENTRYPOINT` arguments are always executed, while `CMD` arguments are appended to `ENTRYPOINT`.

**Analogy:** A Dockerfile is like a detailed recipe script that tells a robot how to build the cake, step-by-step.

**Example: Building a Simple Python Flask App Image**

Let's create a `Dockerfile` for a simple Flask web application.

**1. Create Project Files:**

`app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Dockerized Flask App! Version 1.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

`requirements.txt`:
```
Flask
```

`Dockerfile`:
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY app.py .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
```

**2. Build the Image:**

**Input:**
```bash
docker build -t my-flask-app:1.0 .
```
(Make sure you are in the directory containing `Dockerfile`, `app.py`, and `requirements.txt`)

**Output:**
```
# docker build -t my-flask-app:1.0 .
[+] Building 3.8s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                    0.0s
 => => transferring dockerfile: 282B                                                    0.0s
 => [internal] load .dockerignore                                                       0.0s
 => => transferring context: 2B                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim-buster               1.5s
 => [1/6] FROM docker.io/library/python:3.9-slim-buster@sha256:f52...                   0.0s
 => [internal] load build context                                                       0.0s
 => => transferring context: 531B                                                       0.0s
 => [2/6] WORKDIR /app                                                                  0.1s
 => [3/6] COPY requirements.txt .                                                       0.0s
 => [4/6] COPY app.py .                                                                 0.0s
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt                            2.0s
 => [6/6] EXPOSE 5000                                                                   0.0s
 => [7/6] CMD ["python", "app.py"]                                                      0.0s
 => exporting to image                                                                  0.0s
 => => exporting config c8a7d1a2b3c4...                                                 0.0s
 => => pushing layers                                                                   0.0s
 => => writing image docker.io/library/my-flask-app:1.0                                 0.0s
 => => naming to docker.io/library/my-flask-app:1.0                                     0.0s

# Verify the image is built
docker images my-flask-app
```

**Output (continued):**
```
# docker images my-flask-app
REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
my-flask-app   1.0       c8a7d1a2b3c4   6 seconds ago   139MB
```

---

# Docker Hub

**What is Docker Hub?**

Docker Hub is a **cloud-based registry service** provided by Docker for finding and sharing Docker images. It's the default registry for Docker, meaning `docker pull` and `docker push` commands default to Docker Hub if no other registry is specified.

**Key Features:**

*   **Public Repositories:** Store and share images publicly (e.g., `ubuntu`, `nginx`).
*   **Private Repositories:** Store images securely for your team or organization.
*   **Automated Builds:** Automatically build images from source code repositories (like GitHub or Bitbucket) and push them to Docker Hub.
*   **Webhooks:** Trigger actions after a successful push.
*   **Organizations and Teams:** Manage access to private repositories.

**Analogy:** Docker Hub is like GitHub for Docker images. You can find public projects, or store your private projects there.

**Example: Logging in and Pushing/Pulling from Docker Hub**

First, you need a Docker Hub account. Replace `your-dockerhub-username` with your actual username.

**Input:**
```bash
docker login

# Tag your image with your Docker Hub username
docker tag my-flask-app:1.0 your-dockerhub-username/my-flask-app:1.0

# Push the tagged image to Docker Hub
docker push your-dockerhub-username/my-flask-app:1.0

# (Optional) Remove local image and pull it back to verify
docker rmi your-dockerhub-username/my-flask-app:1.0
docker pull your-dockerhub-username/my-flask-app:1.0
```

**Output:**
```
# docker login
Login with your Docker ID to push and pull images, etc.
Username: your-dockerhub-username
Password:
Login Succeeded

# docker tag my-flask-app:1.0 your-dockerhub-username/my-flask-app:1.0
# (No output on success)

# docker push your-dockerhub-username/my-flask-app:1.0
The push refers to repository [docker.io/your-dockerhub-username/my-flask-app]
d2c94e258dcb: Pushed
... (layers being pushed) ...
1.0: digest: sha256:a1b2c3d4e5f6... size: 2192

# docker rmi your-dockerhub-username/my-flask-app:1.0
Untagged: your-dockerhub-username/my-flask-app:1.0
Deleted: sha256:c8a7d1a2b3c4...
Deleted: sha256:f5e6d7c8b9a0...
...

# docker pull your-dockerhub-username/my-flask-app:1.0
Using default tag: 1.0
1.0: Pulling from your-dockerhub-username/my-flask-app
... (download progress) ...
Status: Downloaded newer image for your-dockerhub-username/my-flask-app:1.0
docker.io/your-dockerhub-username/my-flask-app:1.0
```

---

# Docker Networking

**What is Docker Networking?**

Docker networking allows containers to communicate with each other, with the host machine, and with the outside world. Docker provides several networking drivers for different use cases.

**Common Network Drivers:**

1.  **`bridge` (Default):**
    *   Creates a private internal network for containers on a single host.
    *   Containers on the same bridge can communicate by IP address.
    *   User-defined bridge networks are recommended over the default bridge for better isolation and service discovery by container name.
    *   Traffic to/from the outside world is routed through the host's IP and port mapping.
2.  **`host`:**
    *   Removes network isolation between the container and the Docker host.
    *   The container shares the host's network stack directly. Faster, but less secure and less portable.
3.  **`none`:**
    *   Disables all networking for the container. The container will have a loopback interface only.
4.  **`overlay` (for Swarm):**
    *   Creates a distributed network that spans across multiple Docker hosts. Essential for multi-host container orchestration.
5.  **`macvlan`:**
    *   Assigns a MAC address to a container, making it appear as a physical device on the network. Useful for legacy applications that expect to be directly connected to the physical network.

**Service Discovery with User-Defined Bridge Networks:**

When you create a user-defined bridge network, containers connected to it can communicate with each other using their container names (which act as DNS hostnames).

**Example: Container Communication on a User-Defined Bridge Network**

Let's create two containers, `web` (our Flask app) and `db` (an `alpine` container simulating a database for demonstration), and have them communicate.

**1. Create a custom bridge network:**

**Input:**
```bash
docker network create my-app-network
```

**Output:**
```
# docker network create my-app-network
e1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2
```

**2. Run the `my-flask-app` container on the network:**

**Input:**
```bash
docker run -d --name web --network my-app-network -p 8000:5000 my-flask-app:1.0
```

**Output:**
```
# docker run -d --name web --network my-app-network -p 8000:5000 my-flask-app:1.0
f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2
```

**3. Run an `alpine` container (simulating a DB) on the same network and test connectivity:**

**Input:**
```bash
docker run -it --rm --name db --network my-app-network alpine sh

# Once inside the alpine container's shell, try to ping the web container
ping web
```

**Output (inside the `alpine` container):**
```
/ # ping web
PING web (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.081 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.076 ms
^C
--- web ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.076/0.078/0.081 ms
/ # exit
```
This shows the `db` container can resolve `web` by its name and communicate with it.

---

# Docker Volumes

**What are Docker Volumes?**

Docker containers are designed to be stateless and ephemeral. This means that any data written inside a container's writable layer is lost when the container is removed. **Docker Volumes** provide a way to persist data generated by or used by Docker containers.

**Why use Volumes?**

*   **Persistence:** Data survives container removal.
*   **Data Sharing:** Data can be shared between multiple containers.
*   **Performance:** Volumes can offer better performance than writing data directly to the container's writable layer.
*   **Portability:** Docker volumes are easier to back up and migrate than bind mounts.

**Types of Volumes:**

1.  **Docker Managed Volumes (Recommended):**
    *   Docker manages the storage on the host system (creates a directory under `/var/lib/docker/volumes/` on Linux).
    *   Best practice for persisting container data.
    *   Created and managed using `docker volume` commands.
2.  **Bind Mounts:**
    *   Allows you to mount any existing directory or file from the host system directly into a container.
    *   The host system controls the location and permissions.
    *   Often used for development purposes (e.g., mounting source code into a container for live reloading).
3.  **`tmpfs` Mounts:**
    *   Mounts a temporary file system into the container.
    *   Data is stored in the host's memory, not on disk.
    *   Ideal for sensitive data that doesn't need to persist or for non-persistent state.

**Example: Using a Docker Managed Volume**

Let's use a volume to persist data for a simple Nginx web server.

**1. Create a Docker volume:**

**Input:**
```bash
docker volume create my-nginx-data
```

**Output:**
```
# docker volume create my-nginx-data
my-nginx-data
```

**2. Run an Nginx container, mounting the volume to Nginx's HTML directory:**

**Input:**
```bash
docker run -d --name nginx-with-volume -p 8081:80 -v my-nginx-data:/usr/share/nginx/html nginx:stable

# Wait a few seconds for Nginx to start, then write some content into the volume via the running container
docker exec nginx-with-volume sh -c "echo '<h1>Hello from Persistent Nginx!</h1>' > /usr/share/nginx/html/index.html"

# Verify content by curling
# curl http://localhost:8081
```

**Output:**
```
# docker run -d --name nginx-with-volume -p 8081:80 -v my-nginx-data:/usr/share/nginx/html nginx:stable
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2

# docker exec nginx-with-volume sh -c "echo '<h1>Hello from Persistent Nginx!</h1>' > /usr/share/nginx/html/index.html"
# (No output on success)

# curl http://localhost:8081
<h1>Hello from Persistent Nginx!</h1>
```

**3. Remove the container, then run a new one with the *same* volume:**

**Input:**
```bash
docker stop nginx-with-volume
docker rm nginx-with-volume

# Run a new container using the *same* volume
docker run -d --name new-nginx-with-volume -p 8081:80 -v my-nginx-data:/usr/share/nginx/html nginx:stable

# Verify content again
# curl http://localhost:8081
```

**Output:**
```
# docker stop nginx-with-volume
nginx-with-volume

# docker rm nginx-with-volume
nginx-with-volume

# docker run -d --name new-nginx-with-volume -p 8081:80 -v my-nginx-data:/usr/share/nginx/html nginx:stable
f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2

# curl http://localhost:8081
<h1>Hello from Persistent Nginx!</h1>
```
The content persisted even after the original container was removed, because it was written to the `my-nginx-data` volume.

---

# Docker Compose

**What is Docker Compose?**

Docker Compose is a tool for **defining and running multi-container Docker applications**. With Compose, you use a YAML file (`docker-compose.yml`) to configure your application's services, networks, and volumes. Then, with a single command, you can create and start all the services from your configuration.

**Why Docker Compose?**

*   **Simplifies multi-container app management:** Instead of running multiple `docker run` commands, you define everything in one file.
*   **Declarative:** Describes the desired state of your application stack.
*   **Orchestration for local development/testing:** Ideal for setting up complex local development environments.
*   **Version control:** The `docker-compose.yml` file can be version-controlled, ensuring consistent environments across developers and stages.

**Analogy:** Docker Compose is like a conductor for an orchestra. Instead of giving individual instructions to each musician, the conductor reads a single musical score (the `docker-compose.yml` file) and orchestrates all the musicians (containers) to play together harmoniously.

**Example: A Simple Web App with Nginx and Flask**

Let's use our Flask app from earlier and add an Nginx reverse proxy to it using Docker Compose.

**1. Create Project Structure:**

```
my-flask-nginx-app/
├── app.py
├── requirements.txt
├── Dockerfile          # For the Flask app
├── nginx/
│   └── nginx.conf      # For Nginx configuration
└── docker-compose.yml
```

**2. Files (as created earlier, plus `nginx.conf` and `docker-compose.yml`):**

`app.py`: (same as before)
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Dockerized Flask App! Version 1.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

`requirements.txt`: (same as before)
```
Flask
```

`Dockerfile`: (same as before)
```dockerfile
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
COPY app.py .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

`nginx/nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000; # 'web' is the service name defined in docker-compose.yml
    }

    server {
        listen 80;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

`docker-compose.yml`:
```yaml
version: '3.8' # Specify Compose file format version

services:
  web:
    build: . # Build from the Dockerfile in the current directory
    container_name: flask_web
    restart: always # Always restart if it stops
    environment:
      - PYTHONUNBUFFERED=1 # Important for Python logs to show immediately
    networks:
      - app-network

  nginx:
    image: nginx:stable-alpine # Use a pre-built Nginx image
    container_name: nginx_proxy
    ports:
      - "80:80" # Map host port 80 to container port 80
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro # Mount our custom nginx.conf
    depends_on:
      - web # Ensure 'web' service starts before Nginx
    networks:
      - app-network

networks:
  app-network:
    driver: bridge # Define a custom bridge network for the services
```

**3. Deploy the application with Docker Compose:**

**Input:**
```bash
cd my-flask-nginx-app
docker-compose up -d
```

**Output:**
```
# docker-compose up -d
[+] Running 4/4
 ⠿ Network my-flask-nginx-app_app-network  Created                                  0.0s
 ⠿ Container flask_web                     Started                                  0.0s
 ⠿ Container nginx_proxy                   Started                                  0.0s
# You might see build output for 'web' service if it's the first time or image changed

# Check running containers
docker ps
```

**Output (continued):**
```
# docker ps
CONTAINER ID   IMAGE                                COMMAND                  CREATED         STATUS         PORTS                  NAMES
f1a2b3c4d5e6   my-flask-nginx-app_nginx             "/docker-entrypoint.…"   2 seconds ago   Up 1 second    0.0.0.0:80->80/tcp     nginx_proxy
e1a2b3c4d5e6   my-flask-nginx-app-web               "python app.py"          2 seconds ago   Up 1 second    5000/tcp               flask_web
```

**4. Access the application:**

**Input:**
```bash
curl http://localhost
```

**Output:**
```
# curl http://localhost
Hello from Dockerized Flask App! Version 1.0
```

**5. Tear down the application:**

**Input:**
```bash
docker-compose down
```

**Output:**
```
# docker-compose down
[+] Running 3/3
 ⠿ Container nginx_proxy                   Removed                                  0.1s
 ⠿ Container flask_web                     Removed                                  0.1s
 ⠿ Network my-flask-nginx-app_app-network  Removed                                  0.0s
```

---

# Docker Swarm

**What is Docker Swarm?**

Docker Swarm is Docker's **native orchestration solution** for deploying and managing a cluster of Docker nodes. It turns a pool of Docker hosts into a single, virtual Docker host. Swarm enables you to scale applications across multiple machines, provide high availability, and perform rolling updates.

**Key Concepts:**

*   **Node:** A Docker engine instance participating in the Swarm.
    *   **Manager Nodes:** Handle cluster management tasks, maintain the Swarm state, and dispatch tasks to worker nodes.
    *   **Worker Nodes:** Run the containers (tasks) that are deployed as part of the Swarm services.
*   **Service:** A definition of the tasks to be executed on the Swarm. It defines which Docker image to use, what commands to run, which ports to expose, the desired number of replicas (instances), etc.
*   **Task:** A running container instance as defined by a service. Manager nodes assign tasks to worker nodes.
*   **Stack:** A group of interrelated services, defined in a `docker-compose.yml` (or similar `stack.yml`) file, deployed together as a single unit on the Swarm.

**Why Docker Swarm?**

*   **Built-in to Docker:** No extra installation for the orchestrator itself.
*   **Simplicity:** Easier to set up and manage compared to more complex orchestrators like Kubernetes, especially for simpler use cases.
*   **Scalability:** Easily scale services up or down.
*   **High Availability:** Services can be configured with multiple replicas, and Swarm will automatically restart failed tasks on healthy nodes.
*   **Load Balancing:** Built-in load balancing distributes requests across service replicas.

**Analogy:** If Docker Compose is a conductor for a local orchestra, Docker Swarm is a concert organizer for multiple distributed orchestras (nodes) that play different parts of a large symphony (services) to a massive audience (users).

**Example: Initializing a Swarm and Deploying a Service (Simplified)**

This example assumes you have two machines (or VMs/Cloud instances) with Docker installed: `manager-node` and `worker-node`.

**1. Initialize the Swarm (on `manager-node`):**

**Input (on `manager-node`):**
```bash
docker swarm init --advertise-addr <MANAGER_NODE_IP_ADDRESS>
```
(Replace `<MANAGER_NODE_IP_ADDRESS>` with the IP of your manager machine)

**Output (on `manager-node`):**
```
# docker swarm init --advertise-addr 192.168.1.100
Swarm initialized: current node (abcde12345) is now a manager.

To add a worker to this swarm, run the following command:
    docker swarm join --token SWMTKN-1-xxxxxxxxxxxxxxxxx-yyyyyyyyyyyyyyyyy 192.168.1.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```
**Important:** Copy the `docker swarm join` command from the output.

**2. Join the Swarm as a worker (on `worker-node`):**

**Input (on `worker-node`, using the command from manager's output):**
```bash
docker swarm join --token SWMTKN-1-xxxxxxxxxxxxxxxxx-yyyyyyyyyyyyyyyyy 192.168.1.100:2377
```

**Output (on `worker-node`):**
```
# docker swarm join --token SWMTKN-1-xxxxxxxxxxxxxxxxx-yyyyyyyyyyyyyyyyy 192.168.1.100:2377
This node joined a swarm as a worker.
```

**3. Verify Swarm nodes (on `manager-node`):**

**Input (on `manager-node`):**
```bash
docker node ls
```

**Output (on `manager-node`):**
```
# docker node ls
ID                            HOSTNAME      STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
abcde12345 *                  manager-node  Ready     Active         Leader           24.0.5
fghij67890                    worker-node   Ready     Active                          24.0.5
```

**4. Deploy a Service (on `manager-node`):**

Let's deploy our Flask app as a service with 3 replicas.

**Input (on `manager-node`):**
```bash
docker service create --name my-flask-service --publish 8000:5000 --replicas 3 my-flask-app:1.0
```

**Output (on `manager-node`):**
```
# docker service create --name my-flask-service --publish 8000:5000 --replicas 3 my-flask-app:1.0
t1u2v3w4x5y6
overall progress: 3 out of 3 tasks / 3 running
```

**5. Check Service Status and Tasks (on `manager-node`):**

**Input (on `manager-node`):**
```bash
docker service ls
docker service ps my-flask-service
```

**Output (on `manager-node`):**
```
# docker service ls
ID             NAME              MODE         REPLICAS   IMAGE             PORTS
t1u2v3w4x5y6   my-flask-service  Replicated   3/3        my-flask-app:1.0  *:8000->5000/tcp

# docker service ps my-flask-service
ID             NAME                IMAGE             NODE          DESIRED STATE   CURRENT STATE         ERROR     PORTS
z0y9x8w7v6     my-flask-service.1  my-flask-app:1.0  manager-node  Running         Running 5 seconds ago
a1b2c3d4e5     my-flask-service.2  my-flask-app:1.0  worker-node   Running         Running 5 seconds ago
c3d4e5f6g7     my-flask-service.3  my-flask-app:1.0  worker-node   Running         Running 5 seconds ago
```
This shows the 3 replicas of the Flask app running across the manager and worker nodes. You could then access the app via `http://MANAGER_NODE_IP_ADDRESS:8000` or `http://WORKER_NODE_IP_ADDRESS:8000`, and Swarm's built-in load balancing would distribute requests.

**6. Scale the Service (on `manager-node`):**

**Input (on `manager-node`):**
```bash
docker service scale my-flask-service=5
docker service ps my-flask-service
```

**Output (on `manager-node`):**
```
# docker service scale my-flask-service=5
my-flask-service scaled to 5
overall progress: 5 out of 5 tasks
```
(New tasks will start up)
```
# docker service ps my-flask-service
ID             NAME                IMAGE             NODE          DESIRED STATE   CURRENT STATE           ERROR     PORTS
z0y9x8w7v6     my-flask-service.1  my-flask-app:1.0  manager-node  Running         Running 2 minutes ago
a1b2c3d4e5     my-flask-service.2  my-flask-app:1.0  worker-node   Running         Running 2 minutes ago
c3d4e5f6g7     my-flask-service.3  my-flask-app:1.0  worker-node   Running         Running 2 minutes ago
d5e6f7g8h9     my-flask-service.4  my-flask-app:1.0  manager-node  Running         Running 3 seconds ago
e7f8g9h0i1     my-flask-service.5  my-flask-app:1.0  worker-node   Running         Running 3 seconds ago
```
Now you have 5 instances of your Flask app running.

---