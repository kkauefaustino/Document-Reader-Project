import streamlit as st
from pypdf import PdfReader
import os
from dotenv import load_dotenv

#Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

#Agora conseguimos acessar a chave de forma segura
api_key = os.getenv("GEMINI_API_KEY")

print("Chave carregada com sucesso")

st.set_page_config(page_title="DocReader AI", page_icon="🤖", layout="centered")

st.title("Leitor de Documentos Inteligente")
st.write("Suba um arquivo PDF e faça perguntas diretamente para a IA.")
