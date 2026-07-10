# DocReader AI 

O **DocReader AI** é um assistente inteligente de análise de documentos baseado na arquitetura **RAG (Retrieval-Augmented Generation)**. A aplicação permite que o usuário faça o upload de arquivos PDF e converse diretamente com o documento em tempo real, obtendo respostas rápidas, precisas e sem alucinações da Inteligência Artificial.

Este projeto foi desenvolvido com foco em **Ciência de Dados** e **Engenharia de Software**, aplicando técnicas modernas de fatiamento de texto (*chunking*) e armazenamento vetorial.

---

## Funcionalidades

* **Upload e Processamento Dinâmico**: Extração de texto puro de arquivos binários PDF.
* **Arquitetura RAG Local**: Integração com banco de dados vetorial para buscar apenas os trechos relevantes do documento, economizando tokens e aumentando a velocidade da resposta.
* **Interface Amigável**: Construída inteiramente em Python com troca dinâmica de telas (Upload ➔ Chat).
* **Memória de Sessão**: Histórico de conversa persistente durante o uso da aplicação.
* **Segurança contra Alucinações**: O modelo identifica se o documento possui ou não a resposta, evitando criar informações falsas.

---

## Tecnologias e Ferramentas

* **Linguagem**: [Python (v3.12+)](https://www.python.org/)
* **Interface Web**: [Streamlit](https://streamlit.io/)
* **Orquestração e Processamento de PDF**: [PyPDF](https://pypdf.readthedocs.io/)
* **Fatiamento de Texto (Chunking)**: [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
* **Banco de Dados Vetorial**: [ChromaDB](https://www.trychroma.com/) (Armazenamento persistente e busca por similaridade local)
* **Modelo de Linguagem (LLM)**: [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash`)

---

## Como Funciona a Arquitetura (Por trás dos panos)

1.  **Ingestão de Dados**: O documento PDF é carregado e processado pelo `pypdf`.
2.  **Fatiamento Inteligente**: O texto extraído é quebrado em blocos de 1000 caracteres com sobreposição (*overlap*) de 200 caracteres utilizando o `RecursiveCharacterTextSplitter`.
3.  **Vetorização**: O ChromaDB gera os *embeddings* e armazena os blocos de texto em um banco de dados persistente local (`./meu_chromadb`).
4.  **Recuperação e Prompt**: Quando o usuário faz uma pergunta, o ChromaDB recupera os 3 trechos mais semelhantes e os injeta como contexto no prompt enviado ao `gemini-2.5-flash`.

---

## Como Executar o Projeto Localmente

### 1. Clonar o Repositório
```bash
git clone [https://github.com/kkauefaustino/Nome-Do-Seu-Repositorio.git](https://github.com/kkauefaustino/Nome-Do-Seu-Repositorio.git)
cd Nome-Do-Seu-Repositorio
