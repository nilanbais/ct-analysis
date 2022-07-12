from typing import Optional

class APIExceptions:

    @staticmethod
    def raise_request_exception(**kwargs):
        if None in kwargs.values:
            raise Exception(
                "No header, url, or parameter object created."
            )
    
    @staticmethod
    def check_response_status(response) -> Optional[ValueError]:
        """
        check the response code
        """
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
