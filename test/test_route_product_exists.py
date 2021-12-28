from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_product_exists(route_matcher):
    try:
        assert route_matcher("/product")
    except NotFound:
        fail('Verifique se a rota "/product" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/product", essa rota não é capaz de processar uma requisição')


def test_route_product_especific_exists(route_matcher):
    try:
        assert route_matcher("/product/product_id")
    except NotFound:
        fail('Verifique se a rota "/product/product_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/product/product_id", essa rota não é capaz de processar uma requisição')
