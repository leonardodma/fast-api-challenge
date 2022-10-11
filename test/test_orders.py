from test import client


def test_create_order():
    response = client.post(
        "/order/",
        json={
            "name": "test",
            "address": "test",
            "orders": [{"product_id": 1, "quantity": 1}],
        },
    )
    assert response.status_code == 201
    for key, value in response.json().items():
        if key == "Total Price":
            assert type(value) == float
        elif key == "Purchased Items":
            assert type(value) == list

            if len(value) > 0:
                for order in value:
                    for key, value in order.items():
                        if key == "name":
                            assert type(value) == str
                        elif key == "price":
                            assert type(value) == float
                        elif key == "quantity":
                            assert type(value) == int
                        else:
                            assert False


def test_create_order_invalid():
    response = client.post(
        "/order/",
        json={
            "name": "test",
            "address": "test",
            "orders": [{"product_id": 1}],
        },
    )
    assert response.status_code == 422


def test_create_order_invalid_2():
    response = client.post(
        "/order/",
        json={
            "name": "test",
            "orders": [{"quantity": 1}],
        },
    )
    assert response.status_code == 422
