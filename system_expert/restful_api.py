import json
from http import HTTPStatus

import falcon
from falcon import Response, Request

from core import Engine, Fact
from helpers import status

engine = Engine(set(), set())


class FactResource:

    @staticmethod
    def on_post(request: Request, response: Response):
        try:
            raw_json = request.stream.read()
            engine.facts.add(Fact(**json.loads(raw_json, encoding='utf-8')))
            response.media = {"message": "Fact sucessfully created"}
            response.status = status(HTTPStatus.CREATED)
        except TypeError:
            response.media = {"message": "Bad post variable name"}
            response.status = status(HTTPStatus.BAD_REQUEST)
        except Exception as e:
            response.media = {"message": f"Unmanaged error : {e}"}
            response.status = status(HTTPStatus.INTERNAL_SERVER_ERROR)


api = falcon.API()
api.add_route('/fact', FactResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    simple_server.make_server('127.0.0.1', 8000, api).serve_forever()
