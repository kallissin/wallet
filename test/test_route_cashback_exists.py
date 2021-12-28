from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_cashback_exists(route_matcher):
    try:
        assert route_matcher("/cashback")
    except NotFound:
        fail('Verifique se a rota "/cashback" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/cashback", essa rota não é capaz de processar uma requisição')


def test_route_cashback_especific_exists(route_matcher):
    try:
        assert route_matcher("/cashback/cashback_id")
    except NotFound:
        fail('Verifique se a rota "/cashback/cashback_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/cashback/cashback_id", essa rota não é capaz de processar uma requisição')