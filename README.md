# analytics-engine

Service hosting all data analytics for the project

## Requirements

Python 3.7.9+

## Usage

To run the server, please execute the following from the root directory:

```bash
pip3 install -r requirements.txt
python3 -m app
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .
```

and then follow the docker-compose details at the root of this project
