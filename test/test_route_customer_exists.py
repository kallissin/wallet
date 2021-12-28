from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_customer_exists(route_matcher):
    try:
        assert route_matcher("/customer")
    except NotFound:
        fail('Verifique se a rota "/customer" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/customer", essa rota não é capaz de processar uma requisição')


def test_route_customer_specific_exists(route_matcher):
    try:
        assert route_matcher("/customer/customer_id")
    except NotFound:
        fail('Verifique se a rota "/customer/customer_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/customer/customer_id", essa rota não é capaz de processar uma requisição')
