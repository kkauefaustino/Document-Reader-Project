import streamlit as st
from pypdf import PdfReader
import os
from dotenv import load_dotenv
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

#Agora conseguimos acessar a chave de forma segura
api_key = os.getenv("GEMINI_API_KEY")

cliente_db = chromadb.PersistentClient(path="./meu_chromadb")

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

            collection = cliente_db.get_or_create_collection(name="documentos_pdf")

            fatiador = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)      

            pedacos_de_texto = fatiador.split_text(texo_extraido)

            id_list = [f"id_{i}" for i in range(len(pedacos_de_texto))]

            collection.add(documents = pedacos_de_texto, ids = id_list)
                  
            #Mudança para a tela de chat
            st.session_state.tela_atual = "tela_chat"
            st.rerun()
    
elif st.session_state.tela_atual == "tela_chat":
    from google import genai

    st.title("Converse com o seu PDF")

    #Inicializa a variável de memória do histórico
    if "historico" not in st.session_state:
        st.session_state.historico = [{"role": "assistant", "content": "Olá! Já li o seu PDF. O que gostaria de perguntar?"}]
    
    #Botão para enviar outro arquivo
    if st.button("Enviar outro arquivo"):
        st.session_state.tela_atual = "tela_upload"
        st.session_state.pdf_txt = ""
        del st.session_state.historico
        st.rerun()
    
    #Linha divisória
    st.divider()

    #Para cada mensagem no hisórico conter um tipo de mensageiro e um conteúdo
    for mensagem in st.session_state.historico:
        with st.chat_message(mensagem["role"]):
            st.write(mensagem["content"])

    #Criação do input do usuário
    if pergunta_usuario := st.chat_input("Pergunte algo sobre o documento"):

        #Setando o balão de chat do usuário
        with st.chat_message("user"):
            st.write(pergunta_usuario)
        st.session_state.historico.append({"role": "user", "content": pergunta_usuario})

        #Cliente que conversa com a API
        client = genai.Client(api_key=api_key)

        #Prompt da IA
        prompt = f"""
        Você é um assistente especializado em análise de documentos.
        Use o seguinte texto extraído de um PDF para responder à pergunta do usuário.
        
        Texto do PDF:
        {st.session_state.pdf_txt}
        
        Pergunta:
        {pergunta_usuario}
        """

        #Resposta que a IA irá fornecer
        resposta_ia = client.models.generate_content(
            model= "gemini-2.5-flash",
            contents= prompt
        )

        #Balão de chat da IA
        with st.chat_message("assistant"):
            st.write(resposta_ia.text)
        st.session_state.historico.append({"role": "assistant", "content": resposta_ia.text})

