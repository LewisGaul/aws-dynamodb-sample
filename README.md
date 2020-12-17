
## AWS DynamoDB interaction via Flask app

This repository contains a sample Flask app for testing interaction with AWS DynamoDB, and a local development mock (using the [`moto` package](https://github.com/spulec/moto)).

Python3.6+, tested on Ubuntu (under WSL 1).


### One-time setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### Test it out

`flask run`

This will start the flask server on `http://localhost:5000` in development mode, using a local mock version of DynamoDB by default. 

To use a real AWS DynamoDB connection, set the environment variable `USE_AWS=1`, and set up AWS credentials/config under `~/.aws/` (see https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/quickstart.html#configuration).

Endpoints:
 - `GET /table`: list tables
 - `POST /table/<name>`: create table
 - `GET /table/<name>/item`: list table items
 - `GET /table/<name>/item/<key>`: get single table item
 - `POST /table/<name>/item/<key>?<args>`: create table item

`GET` requests can be performed and easily visualised using a browser, e.g. go to `http:localhost:5000/table` to list tables.

Example usage:
 - Create table: `curl -X POST localhost:5000/table/test-table`
 - List tables: `curl localhost:5000/table`
 - Create item: `curl -X POST localhost:5000/table/test-table/item/foo`
 - Create another item: `curl -X POST "localhost:5000/table/test-table/item/bar?arg1=hello&arg2=42"`
 - List items: `curl localhost:5000/table/test-table/item`
 - Get single item: `curl localhost:5000/table/test-table/item/bar`

Note that whenever you edit the server, flask will automatically restart the server, and the local DB will be reset (i.e. emptied).
