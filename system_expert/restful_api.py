import json

import falcon
from falcon import Response, Request, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_INTERNAL_SERVER_ERROR

from core import Engine, Fact
from exceptions import BadFactField

engine = Engine(set(), set())


class FactResource:

    @staticmethod
    def on_post(request: Request, response: Response):
        try:
            raw_json = request.stream.read()
            new_fact = Fact(**json.loads(raw_json, encoding='utf-8'))
            new_fact.check_fields()
            engine.facts.add(new_fact)
            response.media = {"message": "Fact sucessfully created", "fact_id": hash(new_fact)}
            response.status = HTTP_CREATED
        except BadFactField as e:
            response.media = {"message": str(e)}
            response.status = HTTP_BAD_REQUEST
        except TypeError:
            response.media = {"message": "Bad post variable name"}
            response.status = HTTP_BAD_REQUEST
        except json.decoder.JSONDecodeError:
            response.media = {"message": f"Post data do not match JSON format. Received : {raw_json}"}
            response.status = HTTP_BAD_REQUEST
        except Exception as e:
            response.media = {"message": f"Unmanaged error : {e}. Please fix it here : "
                                         f"https://github.com/Louis-Saglio/PySystemExpert"}
            response.status = HTTP_INTERNAL_SERVER_ERROR
            raise e


api = falcon.API()
api.add_route('/fact', FactResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    simple_server.make_server('127.0.0.1', 8000, api).serve_forever()
