import os
from dotenv import load_dotenv

#Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

#Agora conseguimos acessar a chave de forma segura
api_key = os.getenv("GEMINI_API_KEY")

print("Chave carregada com sucesso")