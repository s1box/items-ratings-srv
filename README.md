## Items rating microservice

This is a microservice written in Python 3 that manages `Item` Ratings.

The microservice exposes `Item Rating` REST API:

| Method | Path  | Description |
|--------|-------|-------------|
| GET    | /items/\<item-id\>/rating  | Returns average rating of the `Item` |
| GET    | /items/\<item-id\>/ratings | Returns list of the `Item` ratings |
| GET    | /items/\<item-id\>/random  | Returns randomly picked existing `Item` rating |
| POST   | /items/\<item-id\>/rating  | Adds a new `Item` Rating record |

Additional endpoints:

| Method | Path    | Description  |
|--------|---------|--------------|
| GET    | /status | Shows stats of the service |

### How to run tests

To run all unit tests, execute:

```sh
python -m unittest discover srv
```

### How to run the microservice

1. Setup SQL database.
2. Configure microservice by setting the following environment variables:

| Environment variable name | Example value | Description |
|---------------------------|---------------|-------------|
| `HOSTNAME`                | `0.0.0.0`     | Host on which the service is listening |
| `PORT`                    | `8080`        | Port on which the servie is listening |
| `DB_USERNAME`             | `user`        | Database user login |
| `DB_PASSWORD`             | `password`    | Database user password |
| `DB_HOSTNAME`             | `sql-host`    | Host on which the database is running |
| `DB_PORT`                 | `3306`        | Port on which the database is running |
| `ITEMS_SERVICE_HOSTNAME`  | `items.net`   | Host on which items service is running |
| `ITEMS_SERVICE_PORT`      | `8080`        | Port on which items service is running |

3. Run the service by executing `python srv/main.py`.
4. Check the service status by quering `/status` endpoint (optional).

### How to run the microservice in debug mode

1. Install `debugpy`:
```sh
pip install debugpy
```

2. Run the microservice with `debugpy` module:
```sh
python -m debugpy --listen 0.0.0.0:2345 main.py
```

3. Connect with your debugger.

#### Debugger configuration for VSCode

1. Install official Python extension.
2. Configure the debugger:
```json
{   
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: connect to remote",
            "type": "python",
            "request": "attach",     
            "justMyCode": true,
            "connect": {
                "host": "localhost",
                "port": 2345
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/srv",
                    "remoteRoot": "/path/in/container"
                }
            ]
        }
    ]
}
```

### License

GNU GPL v2 or any later version.
