from http import HTTPStatus

from flask import Flask, request, jsonify

from system_expert import Engine, Fact

APP = Flask("SystemExpert")


def to_json(func):
    def wrap():
        data, code = func()
        with APP.app_context():
            return jsonify(status=code, **data)
    return wrap()


engine = Engine(set(), set())


@APP.route('/add_fact', methods=["POST"])
def add_fact():
    try:
        engine.facts.add(Fact(**request.form.to_dict()))
        return jsonify("Fact succesfully created", HTTPStatus.CREATED), HTTPStatus.CREATED
    except TypeError:
        return jsonify(message="Bad post variable", status=HTTPStatus.BAD_REQUEST), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify(message=f"Unmanaged server error : {e}", status=HTTPStatus.INTERNAL_SERVER_ERROR), HTTPStatus.INTERNAL_SERVER_ERROR
    # todo test without keyword
    # decorator


@APP.route('/test')
@to_json
def test():
    return {"message": "text"}, 333


if __name__ == '__main__':
    APP.run('127.0.0.1', 8000, True)
