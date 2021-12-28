from flask import Flask


def test_app_is_created(app: Flask):
    assert app.name == 'app'
