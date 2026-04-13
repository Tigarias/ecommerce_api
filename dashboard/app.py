import streamlit as st
import requests
import pandas as pd
import os

# Configuração da URL base da API (usando o nome do serviço no Docker Compose)
API_URL = os.getenv("API_URL", "http://app:8000")

# Configuração da página do Streamlit
st.set_page_config(page_title="Ecommerce Admin Dashboard", layout="wide")

# Título principal da aplicação
st.title("🛒 Ecommerce Admin Dashboard")
st.markdown("Gerencie seus produtos e categorias de forma simples e intuitiva.")

# Barra lateral para navegação entre as seções
menu = st.sidebar.selectbox("Navegação", ["Categorias", "Produtos"])

# --- SEÇÃO DE CATEGORIAS ---
if menu == "Categorias":
    st.header("📁 Gerenciamento de Categorias")
    
    # Formulário para criar uma nova categoria
    with st.expander("➕ Adicionar Nova Categoria"):
        # Campo de texto para o nome da categoria
        cat_name = st.text_input("Nome da Categoria")
        # Área de texto para a descrição da categoria
        cat_desc = st.text_area("Descrição")
        # Botão para enviar os dados para a API
        if st.button("Salvar Categoria"):
            # Verifica se o nome foi preenchido
            if cat_name:
                # Envia a requisição POST para a API
                response = requests.post(f"{API_URL}/categories/", json={"name": cat_name, "description": cat_desc})
                # Se a resposta for sucesso (200), mostra mensagem positiva
                if response.status_code == 200:
                    st.success(f"Categoria '{cat_name}' criada com sucesso!")
                # Caso contrário, mostra o erro retornado pela API
                else:
                    st.error(f"Erro ao criar categoria: {response.text}")
            # Alerta se o nome estiver vazio
            else:
                st.warning("O nome da categoria é obrigatório.")

    # Listagem de categorias existentes
    st.subheader("Categorias Cadastradas")
    # Faz a requisição GET para buscar todas as categorias
    cat_list_resp = requests.get(f"{API_URL}/categories/")
    # Se a busca for bem-sucedida
    if cat_list_resp.status_code == 200:
        # Converte o JSON da resposta em uma lista Python
        categories = cat_list_resp.json()
        # Se houver categorias, mostra em uma tabela formatada pelo Pandas
        if categories:
            df_cat = pd.DataFrame(categories)
            st.table(df_cat)
        # Caso contrário, informa que não há dados
        else:
            st.info("Nenhuma categoria cadastrada ainda.")

# --- SEÇÃO DE PRODUTOS ---
elif menu == "Produtos":
    st.header("📦 Gerenciamento de Produtos")
    
    # Primeiro, buscamos as categorias para preencher o seletor no formulário de produtos
    cat_list_resp = requests.get(f"{API_URL}/categories/")
    # Se as categorias forem encontradas
    if cat_list_resp.status_code == 200:
        categories = cat_list_resp.json()
        # Criamos um dicionário para mapear o nome da categoria ao seu ID
        cat_options = {c['name']: c['id'] for c in categories}
        
        # Formulário para criar um novo produto
        with st.expander("➕ Adicionar Novo Produto"):
            # Campo de texto para o nome do produto
            prod_name = st.text_input("Nome do Produto")
            # Área de texto para a descrição do produto
            prod_desc = st.text_area("Descrição do Produto")
            # Colunas para organizar os campos de preço e estoque lado a lado
            col1, col2 = st.columns(2)
            with col1:
                # Campo numérico para o preço
                prod_price = st.number_input("Preço (R$)", min_value=0.01, step=0.01)
            with col2:
                # Campo numérico para a quantidade em estoque
                prod_stock = st.number_input("Estoque Inicial", min_value=0, step=1)
            
            # Seletor para escolher a categoria do produto
            selected_cat = st.selectbox("Categoria", list(cat_options.keys()))
            
            # Botão para salvar o produto
            if st.button("Salvar Produto"):
                # Verifica se o nome foi preenchido
                if prod_name:
                    # Monta o payload JSON para enviar à API
                    payload = {
                        "name": prod_name,
                        "description": prod_desc,
                        "price": prod_price,
                        "stock": prod_stock,
                        "category_id": cat_options[selected_cat]
                    }
                    # Envia a requisição POST para a API
                    response = requests.post(f"{API_URL}/products/", json=payload)
                    # Se a resposta for sucesso, mostra mensagem positiva
                    if response.status_code == 200:
                        st.success(f"Produto '{prod_name}' criado com sucesso!")
                    # Caso contrário, mostra o erro
                    else:
                        st.error(f"Erro ao criar produto: {response.text}")
                # Alerta se o nome estiver vazio
                else:
                    st.warning("O nome do produto é obrigatório.")
    # Se não houver categorias, avisa que é necessário criar uma primeiro
    else:
        st.warning("Crie pelo menos uma categoria antes de adicionar produtos.")

    # Listagem de produtos existentes
    st.subheader("Produtos em Estoque")
    # Faz a requisição GET para buscar todos os produtos
    prod_list_resp = requests.get(f"{API_URL}/products/")
    # Se a busca for bem-sucedida
    if prod_list_resp.status_code == 200:
        products = prod_list_resp.json()
        # Se houver produtos, mostra em uma tabela
        if products:
            df_prod = pd.DataFrame(products)
            # Reorganiza as colunas para ficar mais legível
            cols = ['id', 'name', 'price', 'stock', 'category_id', 'is_active']
            st.dataframe(df_prod[cols], use_container_width=True)
        # Caso contrário, informa que não há dados
        else:
            st.info("Nenhum produto cadastrado ainda.")
