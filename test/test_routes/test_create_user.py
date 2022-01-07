def test_create_user(client):
    url = "/api/user"
    data = {
        "name": "Maria Silva",
        "email": "MARIA@email.com",
        "username": "maria",
        "password": "123456"
    }

    expected = {
        "user_id": 1,
        "name": "maria silva",
        "email": "maria@email.com",
        "username": "maria",
        "role": "user"
    }
    res = client.post(url, json=data, headers={'Content-Type': 'application/json'})
    assert res.get_json() == expected
