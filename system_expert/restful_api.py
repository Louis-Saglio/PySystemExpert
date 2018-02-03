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
            # todo state is bool
            raw_json = request.stream.read()
            new_fact = Fact(**json.loads(raw_json, encoding='utf-8'))
            engine.facts.add(new_fact)
            response.media = {"message": "Fact sucessfully created", "fact_id": hash(new_fact)}
            response.status = status(HTTPStatus.CREATED)
        except TypeError:
            response.media = {"message": "Bad post variable name"}
            response.status = status(HTTPStatus.BAD_REQUEST)
        except json.decoder.JSONDecodeError:
            response.media = {"message": f"Post data do not match JSON format. Received : {raw_json}"}
            response.status = status(HTTPStatus.BAD_REQUEST)
        except Exception as e:
            response.media = {"message": f"Unmanaged error : {e}. Please fix it here : "
                                         f"https://github.com/Louis-Saglio/PySystemExpert"}
            response.status = status(HTTPStatus.INTERNAL_SERVER_ERROR)
            raise e


api = falcon.API()
api.add_route('/fact', FactResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    simple_server.make_server('127.0.0.1', 8000, api).serve_forever()
