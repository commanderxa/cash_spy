# CashSpy

## Installation

To setup run:

```sh
source ./scripts/setup.sh
```

This command will create python virtual environment and install all the necessary python packages.


## Run

### DataBase

First ensure docker is running on your system, then run:

```sh
docker compose -f "docker-compose.yaml" up -d --build 
```

### Server
To run server:

```sh
source ./scripts/run.sh
```

### Client
To run client:

```
npm run dev
```
