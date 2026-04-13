# Testes para as rotas de Categoria
# Cada teste valida uma operação CRUD específica

def test_create_category(client):
    # Envia uma requisição POST para criar uma nova categoria
    # O 'client' é uma fixture do FastAPI que simula chamadas HTTP
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    # Verifica se o código de status retornado é 200 (Sucesso)
    assert response.status_code == 200
    # Converte a resposta JSON em um dicionário Python
    data = response.json()
    # Valida se o nome da categoria criada é o mesmo que enviamos
    assert data["name"] == "Test Category"
    # Garante que o banco de dados gerou um ID para a nova categoria
    assert "id" in data

def test_read_categories(client):
    # Envia uma requisição GET para listar todas as categorias
    response = client.get("/categories/")
    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 200
    # Garante que o retorno é uma lista (mesmo que vazia)
    assert isinstance(response.json(), list)

def test_read_category(client):
    # Primeiro, criamos uma categoria para garantir que existe algo para ler
    create_response = client.post(
        "/categories/",
        json={"name": "Read Test", "description": "Read Test Description"}
    )
    # Extraímos o ID da categoria recém-criada
    category_id = create_response.json()["id"]
    
    # Agora, buscamos essa categoria específica pelo seu ID
    response = client.get(f"/categories/{category_id}")
    # Validamos o sucesso da busca
    assert response.status_code == 200
    # Verificamos se os dados retornados conferem com o que criamos
    assert response.json()["name"] == "Read Test"

def test_update_category(client):
    # Criamos uma categoria inicial para ser atualizada
    create_response = client.post(
        "/categories/",
        json={"name": "Update Test", "description": "Old Description"}
    )
    category_id = create_response.json()["id"]
    
    # Enviamos uma requisição PUT para atualizar o nome e a descrição
    response = client.put(
        f"/categories/{category_id}",
        json={"name": "Updated Name", "description": "New Description"}
    )
    # Validamos se a atualização foi aceita
    assert response.status_code == 200
    # Verificamos se o nome foi realmente alterado na resposta
    assert response.json()["name"] == "Updated Name"

def test_delete_category(client):
    # Criamos uma categoria para testar a exclusão
    create_response = client.post(
        "/categories/",
        json={"name": "Delete Test", "description": "Delete Test Description"}
    )
    category_id = create_response.json()["id"]
    
    # Enviamos uma requisição DELETE para remover a categoria
    response = client.delete(f"/categories/{category_id}")
    # Validamos se a exclusão foi confirmada
    assert response.status_code == 200
    # Verificamos se a mensagem de sucesso é retornada
    assert response.json()["message"] == "Category deleted successfully"
    
    # Tentamos buscar a categoria deletada para garantir que ela não existe mais
    get_response = client.get(f"/categories/{category_id}")
    # O status esperado agora é 404 (Não Encontrado)
    assert get_response.status_code == 404
