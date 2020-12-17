import decimal
import os

import boto3
import flask

app = flask.Flask(__name__)

if not os.environ.get("USE_AWS"):
    import moto

    moto.mock_dynamodb2().start()


db = boto3.resource("dynamodb")


class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            if int(obj) == obj:
                return int(obj)
            else:
                return float(obj)
        return super().default(obj)


app.json_encoder = JSONEncoder


@app.route("/table", methods=["GET"])
@app.route("/table/<string:name>", methods=["GET", "POST"])
def tables(name=None):
    if flask.request.method == "GET":
        if name:
            return "Can't give specific table details", 500
        app.logger.info("Listing tables")
        return flask.jsonify(db.meta.client.list_tables()["TableNames"])
    elif flask.request.method == "POST":
        app.logger.info("Creating table %s", name)
        table = db.create_table(
            TableName=name,
            KeySchema=[{"AttributeName": "key", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "key", "AttributeType": "S"}],
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=name)
        return str(table.creation_date_time)


@app.route("/table/<string:table_name>/item", methods=["GET"])
@app.route("/table/<string:table_name>/item/<string:key>", methods=["GET", "POST"])
def table_items(table_name: str, key=None):
    if flask.request.method == "GET":
        if key:
            app.logger.info(f"Getting item %s from %s", key, table_name)
            table = db.Table(table_name)
            return table.get_item(Key={"key": key})["Item"]
        else:
            app.logger.info(f"Listing all items in %s", table_name)
            table = db.Table(table_name)
            return flask.jsonify(list(table.scan()["Items"]))
    elif flask.request.method == "POST":
        item = {**flask.request.args, "key": key}
        app.logger.info(f"Creating item in %s: %s", table_name, item)
        table = db.Table(table_name)
        return table.put_item(Item=item)


if __name__ == "__main__":
    app.run()
