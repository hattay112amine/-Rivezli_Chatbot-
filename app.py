import os
import requests
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable  # Pour wrapper DeepSeek LLM
from HtmlTemplates import css, bot_template, user_template

# ===================== LOAD ENV =====================
load_dotenv()  # charge .env automatiquement
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not HF_TOKEN:
    raise ValueError("Vous devez définir la variable d'environnement HUGGINGFACEHUB_API_TOKEN")

# ===================== PDF PROCESSING =====================
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                page_text = page_text.replace("\n", " ").strip()
                text += page_text + " "
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    return splitter.split_text(text)

# ===================== VECTOR STORE =====================
def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-xl",
        model_kwargs={"device": "cpu"}
    )
    return FAISS.from_texts(text_chunks, embeddings)

# ===================== DEEPSEEK LLM WRAPPER =====================
class DeepSeekLLM(Runnable):
    """Wrapper pour DeepSeek V3.2 compatible LangChain"""
    def __init__(self, model="deepseek-ai/DeepSeek-V3.2:novita", api_token=None):
        self.model = model
        self.api_token = api_token or HF_TOKEN
        self.api_url = "https://router.huggingface.co/v1/chat/completions"

    def invoke(self, inputs, *args, **kwargs) -> str:
        # inputs peut être StringPromptValue, dict ou str
        if hasattr(inputs, "to_string"):
            prompt_text = inputs.to_string()
        elif isinstance(inputs, dict):
            prompt_text = inputs.get("question", str(inputs))
        else:
            prompt_text = str(inputs)

        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt_text}],
            "parameters": {"max_new_tokens": 512, "temperature": 0.0},
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

# ===================== CONVERSATION CHAIN =====================
def get_conversation_chain(vector_store):
    history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=history,
        return_messages=True
    )

    llm = DeepSeekLLM()

    template = """
Tu es un assistant strict et fiable.

Réponds uniquement à partir des documents fournis.
Si l'information n'est PAS présente dans les documents, dis clairement :
"Je ne trouve pas cette information dans les documents."

Documents :
{context}

Question : {question}

Réponse (en français, claire et concise) :
"""
    qa_prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        verbose=False,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    return chain

# ===================== CHAT HANDLER =====================
def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.warning("Veuillez d'abord téléverser et traiter vos PDFs.")
        return
    try:
        response = st.session_state.conversation({"question": user_question})
        answer = response.get("answer", "Je ne trouve pas cette information dans les documents.")
    except Exception as e:
        st.error(f"Erreur lors de la génération de réponse : {e}")
        return

    st.session_state.chat_history.append({"user": user_question, "bot": answer})
    for chat in st.session_state.chat_history:
        st.write(user_template.replace("{{MSG}}", chat["user"]), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", chat["bot"]), unsafe_allow_html=True)


# ===================== STREAMLIT APP =====================
def main():
    # Injection du CSS dans l'app
    st.markdown(css, unsafe_allow_html=True)
    st.set_page_config(page_title="Rivezli Chatbot", page_icon="🤖") 
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("🤖 Rivezli Chatbot - Chat avec vos PDFs")
    user_question = st.text_input("Posez une question sur vos documents")

    if st.button("Envoyer") and user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("📄 Vos documents")
        pdf_docs = st.file_uploader("Téléversez vos PDFs", accept_multiple_files=True, type=["pdf"])
        if st.button("Traiter les documents") and pdf_docs:
            with st.spinner("Analyse des documents..."):
                raw_text = get_pdf_text(pdf_docs)
                chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(chunks)
                st.session_state.conversation = get_conversation_chain(vector_store)
                if st.session_state.conversation:
                    st.success("Documents prêts. Posez vos questions !")

if __name__ == "__main__":
    main()
