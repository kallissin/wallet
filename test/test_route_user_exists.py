from pytest import fail
from werkzeug.exceptions import NotFound, InternalServerError


def test_route_user_exists(route_matcher):
    try:
        assert route_matcher("/user")
    except NotFound:
        fail('Verifique se a rota "/user" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/user", essa rota não é capaz de processar uma requisição')


def test_route_user_especific_exists(route_matcher):
    try:
        assert route_matcher("/user/user_id")
    except NotFound:
        fail('Verifique se a rota "/user/user_id" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/user/user_id", essa rota não é capaz de processar uma requisição')


def test_route_user_session_exists(route_matcher):
    try:
        assert route_matcher("/user/session")
    except NotFound:
        fail('Verifique se a rota "/user/session" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/user/session", essa rota não é capaz de processar uma requisição')


def test_route_user_login_exists(route_matcher):
    try:
        assert route_matcher("/user/login")
    except NotFound:
        fail('Verifique se a rota "/user/login" existe')
    except InternalServerError:
        fail('Seu servidor está com erro interno na rota "/user/login", essa rota não é capaz de processar uma requisição')
