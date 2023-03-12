# reality-crawler

Python crawler of reality offers

# Basic flask server

## How to run

### Using docker

    ```sh
    docker build --rm -t flask_server .
    docker run -ti -d -p 5000:5000 flask_server
    ```

#### Privileged mode

    ```sh
    # if you need GPIO use the following (privileged)
    docker run -ti --restart=always --privileged -d -p 5000:5000 flask_server
    docker exec -it “container-id” /bin/bash
    ```

### Without docker

    ```sh
    pip install -r requirements.txt
    python app.py
    ```

### Without docker
