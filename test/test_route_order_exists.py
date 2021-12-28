from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_order_exists(route_matcher):
    try:
        assert route_matcher("/order")
    except NotFound:
        fail('Verifique se a rota "/order" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/order", essa rota não é capaz de processar uma requisição')


def test_route_order_especific_exists(route_matcher):
    try:
        assert route_matcher("/order/order_id")
    except NotFound:
        fail('Verifique se a rota "/order/order_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/order/order_id", essa rota não é capaz de processar uma requisição')


def test_route_order_especific_customer_exists(route_matcher):
    try:
        assert route_matcher("/order/order_id/customer")
    except NotFound:
        fail('Verifique se a rota "/order/order_id/customer" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/order/order_id/customer", essa rota não é capaz de processar uma requisição')


def test_route_order_especific_item_exists(route_matcher):
    try:
        assert route_matcher("/order/order_id/item")
    except NotFound:
        fail('Verifique se a rota "/order/order_id/item" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/order/order_id/item", essa rota não é capaz de processar uma requisição')


def test_route_order_especific_item_especific_exists(route_matcher):
    try:
        assert route_matcher("/order/order_id/item/item_id")
    except NotFound:
        fail('Verifique se a rota "/order/order_id/item/item_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/order/order_id/item/item_id", essa rota não é capaz de processar uma requisição')
