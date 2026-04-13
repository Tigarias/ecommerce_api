# Testes para as rotas de Produto
# Cada teste valida uma operação CRUD específica para produtos e sua relação com categorias

def test_create_product(client):
    # Primeiro, criamos uma categoria para o produto, pois produtos dependem de categorias
    cat_response = client.post(
        "/categories/",
        json={"name": "Prod Cat", "description": "Prod Cat Desc"}
    )
    # Extraímos o ID da categoria criada para associar ao produto
    category_id = cat_response.json()["id"]
    
    # Enviamos uma requisição POST para criar um novo produto
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Test Product Description",
            "price": 100.0,
            "stock": 10,
            "category_id": category_id
        }
    )
    # Validamos se o produto foi criado com sucesso (status 200)
    assert response.status_code == 200
    # Convertemos a resposta JSON em um dicionário
    data = response.json()
    # Verificamos se o nome e o preço conferem com o que enviamos
    assert data["name"] == "Test Product"
    assert data["price"] == 100.0
    # Garante que o banco de dados gerou um ID para o novo produto
    assert "id" in data

def test_read_products(client):
    # Envia uma requisição GET para listar todos os produtos
    response = client.get("/products/")
    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 200
    # Garante que o retorno é uma lista (mesmo que vazia)
    assert isinstance(response.json(), list)

def test_read_product(client):
    # Primeiro, criamos uma categoria e um produto para garantir que existe algo para ler
    cat_response = client.post(
        "/categories/",
        json={"name": "Read Prod Cat", "description": "Read Prod Cat Desc"}
    )
    category_id = cat_response.json()["id"]
    
    # Criamos o produto associado à categoria acima
    create_response = client.post(
        "/products/",
        json={
            "name": "Read Test Product",
            "description": "Read Test Product Description",
            "price": 150.0,
            "stock": 5,
            "category_id": category_id
        }
    )
    # Extraímos o ID do produto recém-criado
    product_id = create_response.json()["id"]
    
    # Agora, buscamos esse produto específico pelo seu ID
    response = client.get(f"/products/{product_id}")
    # Validamos o sucesso da busca
    assert response.status_code == 200
    # Verificamos se os dados retornados conferem com o que criamos
    assert response.json()["name"] == "Read Test Product"

def test_update_product(client):
    # Criamos uma categoria e um produto inicial para ser atualizado
    cat_response = client.post(
        "/categories/",
        json={"name": "Update Prod Cat", "description": "Update Prod Cat Desc"}
    )
    category_id = cat_response.json()["id"]
    
    # Criamos o produto para teste de atualização
    create_response = client.post(
        "/products/",
        json={
            "name": "Update Test Product",
            "description": "Old Description",
            "price": 200.0,
            "stock": 20,
            "category_id": category_id
        }
    )
    product_id = create_response.json()["id"]
    
    # Enviamos uma requisição PUT para atualizar o nome e o preço do produto
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product Name",
            "description": "New Description",
            "price": 250.0,
            "stock": 15,
            "category_id": category_id
        }
    )
    # Validamos se a atualização foi aceita
    assert response.status_code == 200
    # Verificamos se o nome e o preço foram realmente alterados na resposta
    assert response.json()["name"] == "Updated Product Name"
    assert response.json()["price"] == 250.0

def test_delete_product(client):
    # Criamos uma categoria e um produto para testar a exclusão
    cat_response = client.post(
        "/categories/",
        json={"name": "Delete Prod Cat", "description": "Delete Prod Cat Desc"}
    )
    category_id = cat_response.json()["id"]
    
    # Criamos o produto para teste de exclusão
    create_response = client.post(
        "/products/",
        json={
            "name": "Delete Test Product",
            "description": "Delete Test Product Description",
            "price": 300.0,
            "stock": 30,
            "category_id": category_id
        }
    )
    product_id = create_response.json()["id"]
    
    # Enviamos uma requisição DELETE para remover o produto
    response = client.delete(f"/products/{product_id}")
    # Validamos se a exclusão foi confirmada
    assert response.status_code == 200
    # Verificamos se a mensagem de sucesso é retornada
    assert response.json()["message"] == "Product deleted successfully"
    
    # Tentamos buscar o produto deletado para garantir que ele não existe mais
    get_response = client.get(f"/products/{product_id}")
    # O status esperado agora é 404 (Não Encontrado)
    assert get_response.status_code == 404
