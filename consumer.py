"""Creates a kafka consumer for the museum database and checks if messages are valid."""
#pylint: disable=W0718, W1203, R1710, R0911, R0912, R0801, W0612, W0622, C0301
from datetime import datetime, time
import json
from os import environ
import logging

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from requests.exceptions import ConnectionError

from confluent_kafka import Consumer

MINIMUM_RATING_VALUE=0
MAX_RATING_VAL=4
MIN_SITE_VAL=0
MAX_SITE_VAL=5
RATING_POSITION=2
TYPE_POSITION=3
ASSISTANCE=0
EMERGENCY=1
EMERGENCY_OR_ASSISTANCE=-1
START_HOUR=8
START_MIN=45
END_HOUR=18
END_MIN=15

logging.basicConfig(filename="errors.txt",
					format='%(asctime)s %(message)s',
					filemode='w')

logger=logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_db_connection(config: environ) -> connection:
    """Establishes a database connection to the database specified."""
    logger.info("...Establishing a database connection.")
    try:
        conn = connect(dbname=config["DATABASE_NAME"],
                        host=config["DATABASE_HOST"],
                        user=config["DATABASE_USER"],
                        password=config["DATABASE_PASSWORD"],
                        port=config["DATABASE_PORT"])
        return conn
    except ConnectionError as error:
        logging.error(f"An error has occurred: {error}.")


def consume_messages(cons: Consumer, topic) -> None:
    """Processes Kafka messages."""

    cons.subscribe([topic])

    while True:

        msg = cons.poll(1)

        if msg:
            decoded_msg = json.loads(msg.value().decode())

            return decoded_msg


def check_msg_valid(decoded_msg: dict) -> dict:
    """Checks the message is valid."""
    if "at" not in decoded_msg:
        return {"error": True,
                "message": "Invalid: at missing from message."}
    if "site" not in decoded_msg:
        return {"error": True,
                "message": "Invalid: site missing from message."}
    if "val" not in decoded_msg:
        return {"error": True,
                "message": "Invalid: val missing from message."}
    if "site" in decoded_msg:
        try:
            site_val = int(decoded_msg["site"])
            if not MIN_SITE_VAL <= site_val <= MAX_SITE_VAL:
                return {"error": True,
                        "message": "Invalid: site number does not exist."}
        except ValueError:
            return {"error": True,
                    "message": "Invalid: site is not a valid integer."}
    if "val" in decoded_msg:
        try:
            if decoded_msg["val"] is None:
                return {"error": True,
                        "message": "Invalid: val number cannot be none."}

            val_val = int(decoded_msg["val"])
            if not EMERGENCY_OR_ASSISTANCE <= val_val <= MAX_RATING_VAL:
                return {"error": True,
                        "message": "Invalid: val number not within valid range."}
        except ValueError:
            return {"error": True,
                    "message": "Invalid: val is not a valid integer."}

    if decoded_msg["val"] == EMERGENCY_OR_ASSISTANCE and "type" not in decoded_msg:
        return {"error": True,
                "message": "Invalid: type is not present when it should be."}

    if decoded_msg["val"] == EMERGENCY_OR_ASSISTANCE and decoded_msg["type"] is None:
        return {"error": True,
                "message": "Invalid: type cannot be None (must be 0 or 1)."}

    if decoded_msg["val"] == EMERGENCY_OR_ASSISTANCE and decoded_msg["type"] is not None and decoded_msg["type"] != ASSISTANCE and decoded_msg["type"] != EMERGENCY:
        return {"error": True,
                "message": "Invalid: type is not a valid integer."}

    time_at = datetime.strptime(decoded_msg['at'], "%Y-%m-%dT%H:%M:%S.%f+00:00").time()
    if not time(START_HOUR,START_MIN) <= time_at <= time(END_HOUR,END_MIN):
        return {"error": True,
                "message": "Invalid: Must be between 8:45am and 6:15pm."}

    return decoded_msg



if __name__ == "__main__":

    load_dotenv()

    db_conn = get_db_connection(environ)

    consumer = Consumer({
        "bootstrap.servers": environ["BOOTSTRAP_SERVERS"],
        "group.id": environ["GROUP"],
        "auto.offset.reset": environ["AUTO_OFFSET"],
        'security.protocol': environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': environ["SASL_MECHANISM"],
        'sasl.username': environ["USERNAME"],
        'sasl.password': environ["PASSWORD"]                                           
    })


    consumer.subscribe([environ["TOPIC"]])

    try:
        while True:

            decoded_message = consume_messages(consumer,environ["TOPIC"])
            message = check_msg_valid(decoded_message)
            if "error" in message:
                logger.error(message["message"])
            else:
                print(message)

    except KeyboardInterrupt:
        pass
