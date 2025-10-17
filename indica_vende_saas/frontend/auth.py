import requests
import streamlit as st
import os
from functools import lru_cache

# Detecta automaticamente o ambiente
# Para Streamlit Cloud, use a variável de ambiente BACKEND_URL
if os.getenv("STREAMLIT_SHARING_MODE"):
    # Streamlit Cloud deployment - precisa apontar para backend deployado
    BASE_URL = os.getenv("BACKEND_URL", "https://indicavende-api.onrender.com")
elif os.getenv("REPLIT_DEPLOYMENT"):
    # Deployment Replit - usa backend do Render
    BASE_URL = os.getenv("BACKEND_URL", "https://indicavende-api.onrender.com")
elif os.getenv("REPL_SLUG"):
    # Desenvolvimento Replit - usa backend do Render
    BASE_URL = os.getenv("BACKEND_URL", "https://indicavende-api.onrender.com")
else:
    # Desenvolvimento local
    BASE_URL = os.getenv("BACKEND_URL", "https://indicavende-api.onrender.com")

def login(email: str, password: str):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login", 
            json={
                "email": email,
                "password": password
            },
            timeout=5  # Timeout de 5 segundos
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except requests.Timeout:
        st.error("⏱️ Tempo de conexão esgotado. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
        return None

def register(name: str, email: str, password: str, role: str):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register", 
            json={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            },
            timeout=5  # Timeout de 5 segundos
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            st.error("Email já está cadastrado")
            return None
        else:
            st.error(f"Erro ao criar conta: {response.text}")
            return None
    except requests.Timeout:
        st.error("⏱️ Tempo de conexão esgotado. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
        return None

def logout():
    st.session_state.user = None

def get_current_user():
    return st.session_state.get('user')

def make_authenticated_request(endpoint: str, method: str = "GET", data: dict = None):
    user = get_current_user()
    if not user:
        return None
    
    headers = {"X-User-Email": user.get('email')}
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        
        return response
    except requests.Timeout:
        st.error("⏱️ Tempo de conexão esgotado. Verifique sua internet.")
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
        return None
