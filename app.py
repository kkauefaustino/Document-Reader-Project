import streamlit as st
from pypdf import PdfReader
import os
from dotenv import load_dotenv

#Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

#Agora conseguimos acessar a chave de forma segura
api_key = os.getenv("GEMINI_API_KEY")

#Config inicial da página
st.set_page_config(page_title="DocReader AI", page_icon="🤖", layout="centered")

#Inicializa as variáveis de memória da sessão
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "tela_upload"
if "pdf_txt" not in st.session_state:
    st.session_state.pdf_txt = ""

#Tela do upload
if st.session_state.tela_atual == "tela_upload":

    st.markdown("<h1><br><br>Leitor de Documentos Inteligente</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-left: 110px;'> Suba um arquivo PDF e faça perguntas diretamente para a IA.</p>", unsafe_allow_html=True)

    #Aceita apenas o PDF
    arqv_pdf = st.file_uploader("Envie seu Arquivo PDF", type=["pdf"])

    if arqv_pdf is not None:
        st.info("Arquivo carregado") 
              
        if st.button("Analisar PDF"):
            #Leitor do PDF
            leitor_pdf = PdfReader(arqv_pdf)
            texo_extraido = ""

            #Extraindo o texto
            for pagina in leitor_pdf.pages:
                texo_extraido += pagina.extract_text() + "/n"
                 
            st.session_state.pdf_txt = texo_extraido
            
            #Mudança para a tela de chat
            st.session_state.tela_atual = "tela_chat"
            st.rerun()
    
elif st.session_state.tela_atual == "tela_chat":
    st.title("Conteúdo do PDF")

    st.text_area("Texto extraído: ", value=st.session_state.pdf_txt, height=400)