import datetime
import logging
import traceback
from dcentrapi.Base import Base, DapiError
from dcentrapi.requests_dappi import requests_get

logger = logging.getLogger()
logger.setLevel("INFO")


class HackMitigation(Base):

    def are_addresses_blacklisted(self, addresses: [str]):
        url = self.url + "generic_freeze_signal/are_addresses_blacklisted"
        data = {
            "addresses": addresses,
        }
        response = None
        tries = 7
        while tries > 0:
            logger.info(f"{tries} more tries")
            before = datetime.datetime.now()
            logger.info(f"before request: {before}")
            try:
                response = requests_get(url, params=data, headers=self.headers)

                after = datetime.datetime.now()
                logger.info(f"after request: {after}")
                logger.info(f"time elapsed: {after-before}")
                if response.status_code == 200:
                    # Parse the JSON data using the json() method
                    data = response.json()
                    logger.info(f"data={data}")  # This will logger.info the parsed JSON data as a Python dictionary
                    return data
                else:
                    logger.error(f"Request failed with status code: {response.status_code} and error message: {response.error_message}")
                    tries -= 1

            except Exception as e:
                return DapiError(response=response.__dict__, exception=f"e: {e}, traceback: {traceback.format_exc()}")
