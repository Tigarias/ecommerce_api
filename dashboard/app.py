import streamlit as st
import requests
import pandas as pd
import os

# Configuração da URL base da API (usando o nome do serviço no Docker Compose)
API_URL = os.getenv("API_URL", "http://app:8000")

# Configuração da página do Streamlit com o nome da empresa
st.set_page_config(page_title="Eyes on Technology - Gestão de Inventário", layout="wide")

# Estilo customizado para o cabeçalho e elementos visuais
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .delete-btn>button {
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal da aplicação corporativa
st.markdown('<div class="main-title">👁️ Eyes on Technology</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistema de Gestão de Inventário de Hardware e Componentes</div>', unsafe_allow_html=True)

# Barra lateral para navegação entre as seções
st.sidebar.image("https://img.icons8.com/fluency/96/000000/processor.png", width=100)
menu = st.sidebar.selectbox("Navegação", [
    "📊 Dashboard Geral", 
    "🔍 Monitoramento de Estoque",
    "📁 Gerenciar Categorias", 
    "📦 Gerenciar Produtos"
])

# --- FUNÇÕES AUXILIARES ---
def get_categories():
    # Busca todas as categorias cadastradas na API
    try:
        resp = requests.get(f"{API_URL}/categories/")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def get_products():
    # Busca todos os produtos cadastrados na API
    try:
        resp = requests.get(f"{API_URL}/products/")
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def delete_item(item_type, item_id):
    # Envia requisição DELETE para a API
    try:
        endpoint = "categories" if item_type == "category" else "products"
        resp = requests.delete(f"{API_URL}/{endpoint}/{item_id}")
        return resp.status_code == 200
    except:
        return False

# --- SEÇÃO: DASHBOARD GERAL (KPIs) ---
if menu == "📊 Dashboard Geral":
    st.header("📊 Visão Geral do Negócio")
    
    products = get_products()
    if products:
        df_prod = pd.DataFrame(products)
        
        # Cálculo de métricas financeiras e de estoque
        total_items = len(df_prod)
        total_stock = df_prod['stock'].sum()
        inventory_value = (df_prod['price'] * df_prod['stock']).sum()
        
        # Exibição dos KPIs em colunas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Produtos", total_items)
        with col2:
            st.metric("Itens em Estoque", total_stock)
        with col3:
            st.metric("Valor Total do Inventário", f"R$ {inventory_value:,.2f}")
            
        # Gráfico de distribuição por categoria
        st.subheader("Distribuição de Produtos por Categoria")
        st.bar_chart(df_prod['category_id'].value_counts())
    else:
        st.info("Nenhum dado disponível. Comece cadastrando categorias e produtos.")

# --- SEÇÃO: MONITORAMENTO DE ESTOQUE (NOVA) ---
elif menu == "🔍 Monitoramento de Estoque":
    st.header("🔍 Monitoramento de Estoque em Tempo Real")
    
    products = get_products()
    if products:
        df_prod = pd.DataFrame(products)
        
        # Filtros de Monitoramento
        st.subheader("Filtros de Inventário")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filtrar por Status",
                ["Em Estoque", "Estoque Crítico ( < 5 )", "Esgotado"],
                default=["Em Estoque", "Estoque Crítico ( < 5 )", "Esgotado"]
            )
        
        # Lógica de Status
        def get_status(stock):
            if stock == 0: return "Esgotado"
            if stock < 5: return "Estoque Crítico ( < 5 )"
            return "Em Estoque"
        
        df_prod['Status'] = df_prod['stock'].apply(get_status)
        
        # Aplicar filtro
        df_filtered = df_prod[df_prod['Status'].isin(status_filter)]
        
        # Exibição com cores e formatação
        st.dataframe(
            df_filtered[['id', 'name', 'stock', 'price', 'Status']].sort_values(by='stock'),
            use_container_width=True,
            hide_index=True
        )
        
        # Alertas Visuais
        critical_count = len(df_prod[df_prod['stock'] < 5])
        if critical_count > 0:
            st.error(f"🚨 Existem {critical_count} itens que precisam de reposição imediata!")
    else:
        st.info("Nenhum produto para monitorar.")

# --- SEÇÃO: GERENCIAR CATEGORIAS ---
elif menu == "📁 Gerenciar Categorias":
    st.header("📁 Gestão de Categorias")
    
    # Formulário de Cadastro
    with st.expander("➕ Adicionar Nova Categoria"):
        with st.form("form_cat", clear_on_submit=True):
            cat_name = st.text_input("Nome da Categoria", placeholder="Ex: Processadores")
            cat_desc = st.text_area("Descrição")
            if st.form_submit_button("Salvar"):
                if cat_name:
                    resp = requests.post(f"{API_URL}/categories/", json={"name": cat_name, "description": cat_desc})
                    if resp.status_code == 200:
                        st.success("Categoria criada!")
                        st.rerun()
                else:
                    st.warning("Nome é obrigatório.")

    # Listagem com Opção de Exclusão
    st.subheader("Categorias Existentes")
    categories = get_categories()
    if categories:
        for cat in categories:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{cat['name']}** (ID: {cat['id']})")
                st.caption(cat['description'])
            with col2:
                if st.button(f"Excluir", key=f"del_cat_{cat['id']}"):
                    if delete_item("category", cat['id']):
                        st.success("Excluído!")
                        st.rerun()
                    else:
                        st.error("Erro ao excluir (verifique se há produtos vinculados).")
            st.divider()
    else:
        st.info("Nenhuma categoria cadastrada.")

# --- SEÇÃO: GERENCIAR PRODUTOS ---
elif menu == "📦 Gerenciar Produtos":
    st.header("📦 Gestão de Produtos")
    
    categories = get_categories()
    if categories:
        cat_options = {c['name']: c['id'] for c in categories}
        
        # Formulário de Cadastro
        with st.expander("➕ Adicionar Novo Produto"):
            with st.form("form_prod", clear_on_submit=True):
                p_name = st.text_input("Nome do Produto", placeholder="Ex: RTX 4090")
                p_desc = st.text_area("Descrição")
                col1, col2 = st.columns(2)
                with col1:
                    p_price = st.number_input("Preço (R$)", min_value=0.0, value=1000.0)
                with col2:
                    p_stock = st.number_input("Estoque", min_value=0, value=10)
                p_cat = st.selectbox("Categoria", list(cat_options.keys()))
                
                if st.form_submit_button("Salvar Produto"):
                    if p_name:
                        payload = {
                            "name": p_name, "description": p_desc, 
                            "price": p_price, "stock": p_stock, 
                            "category_id": cat_options[p_cat]
                        }
                        resp = requests.post(f"{API_URL}/products/", json=payload)
                        if resp.status_code == 200:
                            st.success("Produto adicionado!")
                            st.rerun()
                    else:
                        st.warning("Nome é obrigatório.")

    # Listagem com Opção de Exclusão
    st.subheader("Produtos no Catálogo")
    products = get_products()
    if products:
        for prod in products:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{prod['name']}** - R$ {prod['price']:,.2f}")
                st.caption(f"Estoque: {prod['stock']} | Categoria ID: {prod['category_id']}")
            with col2:
                if st.button(f"Excluir", key=f"del_prod_{prod['id']}"):
                    if delete_item("product", prod['id']):
                        st.success("Excluído!")
                        st.rerun()
            st.divider()
    else:
        st.info("Nenhum produto cadastrado.")
