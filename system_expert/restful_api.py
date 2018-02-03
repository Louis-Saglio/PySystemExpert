import falcon
from falcon import Response, Request, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_INTERNAL_SERVER_ERROR

from core import Engine, Fact
from exceptions import BadFactField

engine = Engine(set(), set())


class FactResource:

    @staticmethod
    def on_post(request: Request, response: Response):
        try:
            new_fact = Fact(**request.media)
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
        except Exception as e:
            response.media = {"message": f"Unmanaged error : {e}. Please fix it here : "
                                         f"https://github.com/Louis-Saglio/PySystemExpert"}
            response.status = HTTP_INTERNAL_SERVER_ERROR
            raise e


class FactsResource:

    @staticmethod
    def on_get(request: Request, response: Response):
        """Process facts according to rules and list facts"""
        try:
            engine.process()
            response.media = {
                "facts": [{"name": fact.NAME, "value": fact.VALUE, "state": fact.STATE} for fact in engine.facts]
            }
        except Exception as e:
            raise e


api = falcon.API()
api.add_route('/fact', FactResource())
api.add_route('/facts', FactsResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    simple_server.make_server('127.0.0.1', 8000, api).serve_forever()
