import requests
import openaq
import dateutil
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import json
import os
import time
import logging
import uuid

api = openaq.OpenAQ()
API_KEY = os.environ["API_KEY"]
logger = logging.getLogger()
handler = logging.StreamHandler()


def flatten_message(message: dict) -> dict:
    message["id"] = str(uuid.uuid4())
    message["latitude"] = message["coordinates"]["latitude"]
    message["longitude"] = message["coordinates"]["longitude"]
    message["local"] = message["date"]["local"]
    message["utc"] = message["date"]["utc"]
    message.pop("coordinates")
    message.pop("date")
    return message


def start_pull(config: dict):
    while True:
        oldtime = time.time()
        logging.info("Start Cycle")
        message_total = 0
        message_stat = 0
        for country in config["countries"]:
            for city in country["cities"]:
                page = 1
                num_pages = 1

                while page <= num_pages:
                    try:
                        date_from = (datetime.utcnow() - timedelta(minutes=config["frequency"])).strftime(
                            "%Y-%m-%dT%H:%M:%S")
                        logging.info("Getting from "+date_from + "page " + str(page))
                        mesaurement = api.measurements(country=country["code"], city=city,
                                                       date_from=date_from,
                                                       page=page)
                        num_pages = mesaurement[1]["meta"]["pages"]

                        for measure in mesaurement[1]["results"]:
                            message = flatten_message(measure)
                            r = requests.post(
                                'https://www.streamr.com/api/v1/streams/' + country["stream_name"] + '/data',
                                json=message,
                                headers={'Authorization': 'token ' + API_KEY})

                            if r.status_code != 200:
                                print(r.content)
                                raise Exception("Failed")
                            else:
                                message_stat = message_stat + 1
                                message_total = message_total + 1

                            # check
                            if time.time() - oldtime > 59:
                                logging.info("Rate:  " + str(message_stat) + "/minute")
                                message_stat = 0
                                oldtime = time.time()
                        page = page + 1
                    except Exception as e:
                        logging.exception(e)

        logging.info("End Cycle")
        logging.info("Messages sent during cycle: " + str(message_total))
        time.sleep(config["frequency"] * 60)


def main():
    with open('config.json') as f:
        config = json.load(f)
    formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
    logger.info("Starting openaq")
    logger.debug("Config:")
    logger.debug(config)
    start_pull(config)


if __name__ == '__main__':
    main()



