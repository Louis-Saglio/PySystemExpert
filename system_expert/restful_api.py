import falcon
from falcon import Response, Request, HTTP_BAD_REQUEST, HTTP_CREATED, HTTP_INTERNAL_SERVER_ERROR

from core import Engine, Fact, Rule
from exceptions import BadFactField

engine = Engine(set(), set())


class FactResource:

    @staticmethod
    def on_post(request: Request, response: Response):
        try:
            new_fact = Fact(**request.media)
            new_fact.check_fields()
            engine.facts.add(new_fact)
            response.media = {"message": "Fact successfully created", "fact_id": hash(new_fact)}
            response.status = HTTP_CREATED
        except BadFactField as e:
            response.media = {"message": str(e)}
            response.status = HTTP_BAD_REQUEST
        except TypeError:
            response.media = {"message": "Bad post variable name"}
            response.status = HTTP_BAD_REQUEST


class FactsResource:

    # noinspection PyUnusedLocal
    @staticmethod
    def on_get(request: Request, response: Response):
        """Process facts according to rules and list facts"""
        engine.process()
        response.media = {
            "facts": [{"name": fact.NAME, "value": fact.VALUE, "state": fact.STATE} for fact in engine.facts]
        }


class RuleResource:

    @staticmethod
    def on_post(request: Request, response: Response):
        try:
            majors, conclusions = request.media["majors"], request.media["conclusions"]
            new_rule = Rule(
                frozenset(Fact(**major) for major in majors),
                frozenset(Fact(**conclusion) for conclusion in conclusions)
            )
            engine.rules.add(new_rule)
            response.media = {"message": "Rule successfully created", "rule_id": hash(new_rule)}
            response.status = HTTP_CREATED
        except Exception as e:
            raise e


api = falcon.API()
api.add_route('/fact', FactResource())
api.add_route('/facts', FactsResource())
api.add_route('/rule', RuleResource())

if __name__ == '__main__':
    from wsgiref import simple_server
    simple_server.make_server('127.0.0.1', 8000, api).serve_forever()
