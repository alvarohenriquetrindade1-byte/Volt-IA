import streamlit as st
import urllib.parse
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(
    page_title="Volt IA", 
    page_icon="⚡", 
    layout="centered"
)

# Estilização em Preto e Azul Neon
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0c10 0%, #121824 100%);
        color: #e6edf3;
    }
    h1, h2, h3, p, span {
        color: #e6edf3 !important;
    }
    .stChatMessage {
        background-color: rgba(22, 27, 34, 0.7) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 210, 255, 0.25);
        border-radius: 16px !important;
        padding: 14px;
        margin-bottom: 12px;
    }
    .stChatInputContainer input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #00d2ff !important;
        border-radius: 20px !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0072ff, #00d2ff) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: bold !important;
        padding: 8px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Volt IA")
st.caption("Converse sobre qualquer assunto: ideias, jogos, dúvidas, códigos, histórias e bate-papo!")

# BARRA LATERAL
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Sua Chave API Gemini:", type="password")
    
    st.markdown("---")
    st.subheader("📱 QR Code para Testar")
    link_app = st.text_input("Link do site:", "https://meu-app.streamlit.app")
    
    if link_app:
        # Gerador de QR Code ultra leve via API
        link_enc = urllib.parse.quote(link_app)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={link_enc}"
        st.image(qr_url, caption="Escaneie com a câmera do celular")

aba_chat, aba_midia = st.tabs(["💬 Conversa Livre", "📁 Enviar Arquivos & Fotos"])

# ABA 1: CHAT LIVRE
with aba_chat:
    if "historico" not in st.session_state:
        st.session_state.historico = [
            {"role": "assistant", "content": "Olá! Sou a Volt IA. Podemos conversar sobre qualquer assunto! Como posso te ajudar hoje?"}
        ]

    for msg in st.session_state.historico:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        st.session_state.historico.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if api_key:
                try:
                    client = genai.Client(api_key=api_key)
                    
                    contents = []
                    for m in st.session_state.historico:
                        role = "user" if m["role"] == "user" else "model"
                        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
                    
                    response = client.models.generate_content_stream(
                        model='gemini-2.5-flash',
                        contents=contents
                    )
                    
                    def stream_wrapper():
                        for chunk in response:
                            yield chunk.text

                    texto_final = st.write_stream(stream_wrapper())
                    st.session_state.historico.append({"role": "assistant", "content": texto_final})
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                resposta_demo = f"Você disse: **'{prompt}'**.\n\nPara responder com inteligência total sobre qualquer tema, insira sua Chave API no menu lateral!"
                st.markdown(resposta_demo)
                st.session_state.historico.append({"role": "assistant", "content": resposta_demo})

# ABA 2: ENVIO DE ARQUIVOS
with aba_midia:
    st.subheader("📷 Análise de Arquivos")
    arquivo = st.file_uploader("Escolha um arquivo para enviar:", type=["png", "jpg", "jpeg", "pdf", "txt"])
    
    if arquivo and st.button("Analisar Arquivo"):
        st.success(f"Arquivo '{arquivo.name}' recebido com sucesso!")
