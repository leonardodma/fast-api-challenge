from test import client

def test_create_item():
    response = client.post("/item/", json={"name": "test", "price": 5.5})
    assert response.status_code == 201
    assert response.json() == {"message": "Item created successfully"}


def test_create_item_invalid():
    response = client.post("/item/", json={"name": "test"})
    assert response.status_code == 422


def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    for key, value in response.json().items():
        if key == "name":
            assert type(value) == str
        elif key == "price":
            assert type(value) == float
        elif key == "id":
            assert type(value) == int
        else:
            assert False
