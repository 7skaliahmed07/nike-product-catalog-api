
def test_create_product(client):
    product_data = {
        "name": "Nike Air Max",
        "description": "Running shoes",
        "category": "Shoes",
        "price": 120.00,
        "stock": 50
    }

    response = client.post("/products", json=product_data)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Nike Air Max"
    assert data["category"] == "Shoes"
    assert data["stock"] == 50
    assert "id" in data


def test_get_product(client):
    product_data = {
        "name": "Nike Pegasus",
        "description": "Running shoes",
        "category": "Shoes",
        "price": 100.00,
        "stock": 30
    }

    create_response = client.post("/products", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Nike Pegasus"


def test_get_missing_product(client):
    response = client.get(
        "/products/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404



def test_filter_products_by_category(client):
    client.post("/products", json={
        "name": "Nike Air Max",
        "category": "Shoes",
        "price": 120,
        "stock": 50
    })

    client.post("/products", json={
        "name": "Nike T-Shirt",
        "category": "Clothing",
        "price": 40,
        "stock": 20
    })

    response = client.get("/products?category=Shoes")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["products"][0]["name"] == "Nike Air Max"


def test_filter_products_by_price(client):
    client.post("/products", json={
        "name": "Nike Air Max",
        "category": "Shoes",
        "price": 120,
        "stock": 50
    })

    client.post("/products", json={
        "name": "Nike T-Shirt",
        "category": "Clothing",
        "price": 40,
        "stock": 20
    })

    response = client.get("/products?min_price=50&max_price=150")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["products"][0]["name"] == "Nike Air Max"


def test_update_product(client):
    create_response = client.post("/products", json={
        "name": "Nike Air Max",
        "category": "Shoes",
        "price": 120,
        "stock": 50
    })

    product_id = create_response.json()["id"]

    updated_data = {
        "name": "Nike Air Max Updated",
        "category": "Shoes",
        "price": 110,
        "stock": 60
    }

    response = client.put(
        f"/products/{product_id}",
        json=updated_data
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Nike Air Max Updated"
    assert response.json()["stock"] == 60


def test_delete_product(client):
    create_response = client.post("/products", json={
        "name": "Nike Air Max",
        "category": "Shoes",
        "price": 120,
        "stock": 50
    })

    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204

    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404




def test_product_pagination(client):
    for i in range(5):
        client.post("/products", json={
            "name": f"Nike Product {i}",
            "category": "Shoes",
            "price": 100 + i,
            "stock": 10
        })

    response = client.get("/products?page=1&limit=2")

    assert response.status_code == 200
    assert response.json()["total"] == 5
    assert response.json()["page"] == 1
    assert response.json()["limit"] == 2
    assert len(response.json()["products"]) == 2

    second_page = client.get("/products?page=2&limit=2")

    assert second_page.status_code == 200
    assert len(second_page.json()["products"]) == 2


def test_reject_negative_price(client):
    response = client.post("/products", json={
        "name": "Nike Shoes",
        "category": "Shoes",
        "price": -10,
        "stock": 10
    })

    assert response.status_code == 422


def test_reject_negative_stock(client):
    response = client.post("/products", json={
        "name": "Nike Shoes",
        "category": "Shoes",
        "price": 100,
        "stock": -5
    })

    assert response.status_code == 422


def test_reject_invalid_pagination(client):
    response = client.get("/products?page=0&limit=20")

    assert response.status_code == 400


def test_reject_invalid_price_range(client):
    response = client.get("/products?min_price=200&max_price=100")

    assert response.status_code == 400



def test_patch_product(client):
    response = client.post(
        "/products",
        json={
            "name": "Nike Air Max",
            "description": "Running shoes",
            "category": "Shoes",
            "price": 100.00,
            "stock": 20
        }
    )

    product_id = response.json()["id"]

    patch_response = client.patch(
        f"/products/{product_id}",
        json={"price": 129.99}
    )

    assert patch_response.status_code == 200
    assert float(patch_response.json()["price"]) == 129.99
    assert patch_response.json()["name"] == "Nike Air Max"
    assert patch_response.json()["stock"] == 20


def test_patch_missing_product(client):
    import uuid

    response = client.patch(
        f"/products/{uuid.uuid4()}",
        json={"price": 129.99}
    )

    assert response.status_code == 404


def test_patch_empty_request(client):
    response = client.post(
        "/products",
        json={
            "name": "Nike Air Max",
            "description": "Running shoes",
            "category": "Shoes",
            "price": 100.00,
            "stock": 20
        }
    )

    product_id = response.json()["id"]

    patch_response = client.patch(
        f"/products/{product_id}",
        json={}
    )

    assert patch_response.status_code == 400
    assert patch_response.json()["detail"] == (
        "At least one field must be provided for update"
    )