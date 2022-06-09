import logging
import warnings
import requests
import urllib3
import dpath.util as xpath


class ApiRequest:
    def __init__(
        self, api: str, path: str, data: dict = None, session: bool = True
    ):
        self.api = api
        self.path = path
        self.data = data
        self.request = requests
        self.session = session

    def logger_debug(self) -> None:
        logging.debug('<h2><code>Request url & endpoint</code></h2>')
        logging.debug(f'\nURL: {self.api}\nPATH: {self.path}')

    @property
    def call_api(self):
        if self.session:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            with self.request.Session() as session:
                with warnings.catch_warnings():
                    warnings.simplefilter(
                        action="ignore", category=ResourceWarning
                    )
                    self.logger_debug()
                    return session
        else:
            return self.request

    def get(self):
        return self.call_api.get(url=self.api + self.path, verify=False)

    def post(self):
        return self.call_api.post(
            url=self.api + self.path, json=self.data, verify=False
        )

    def patch(self):
        return self.call_api.patch(
            url=self.api + self.path, json=self.data, verify=False
        )

    def put(self):
        return self.call_api.put(
            url=self.api + self.path, json=self.data, verify=False
        )

    def delete(self):
        return self.call_api.delete(
            url=self.api + self.path, json=self.data, verify=False
        )


class JPath:

    def __init__(self, response):
        self.response = response

    def get(self, glob, separator="/"):
        if self.response:
            logging.debug('<h2><code>Response type JSON perform search glob </code></h2>')
            logging.debug(f"\n{self.response.json()} search {glob=}")
            return xpath.get(obj=self.response.json(), glob=glob, separator=separator)

    def values(self, glob, separator="/"):
        if self.response:
            logging.debug('<h2><code>Response type JSON perform search: </code></h2>')
            logging.debug(f"\n{self.response.json()} search {glob=}")
            return xpath.values(
                obj=self.response.json(), glob=glob, separator=separator
            )


if __name__ == '__main__':
    request = ApiRequest(
        "http://127.0.0.1:5000/api/v1",
        "/get-all-publications?from_date=07-06-2022&to_date=07-06-2022"
    ).get()
    x = JPath(request).values('data/*/id')
    print(len(x))