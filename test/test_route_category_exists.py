from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_category_exists(route_matcher):
    try:
        assert route_matcher("/category")
    except NotFound:
        fail('Verifique se a rota "/category" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/category", essa rota não é capaz de processar uma requisição')


def test_route_category_especific_exists(route_matcher):
    try:
        assert route_matcher("/category/category_id")
    except NotFound:
        fail('Verifique se a rota "/category/category_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/category/category_id", essa rota não é capaz de processar uma requisição')
