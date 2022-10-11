# Fast Api Challenge

## Run the API

#### Config dotenv

The first step to run the API is to create on the root directory of the project a `.env` file, and then create a variable called `SQLITE_DATA_PATH`, where the SQL alchemy will store in a file called `data.db`, that will be the storage of this project, such as in the following example:

```python
SQLITE_DATA_PATH = "/your/path"
```

After that, you will need to install de dependencies, using [poetry](https://python-poetry.org/docs/). With poetry installed, run:

```console
poetry install
```

To start the API, on the root directory of the project, run:

```console
poetry run uvicorn app.main:app --reload
```

After that, on http://127.0.0.1:8000/docs it is possible to see the documentation, where you can view the endpoints, and do some tests.

## Test

On the root directory of the project, run:

```console
poetry run pytest
```