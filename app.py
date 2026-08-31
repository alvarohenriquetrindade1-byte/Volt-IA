import streamlit as st
import urllib.parse
from google import genai

# Ocultar cabeçalhos, rodapés e avisos do Streamlit
st.set_page_config(
    page_title="Mentor IA", 
    page_icon="⚡", 
    layout="centered"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppViewerFooter {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
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

st.title("⚡ Mentor IA")
st.caption("Converse sobre qualquer assunto: ideias, jogos, dúvidas, códigos, histórias e bate-papo!")

# BARRA LATERAL
with st.sidebar:
    st.subheader("📱 QR Code para Testar")
    link_app = "https://volt-ia-2kwmutczjgrrjoihrepobg.streamlit.app/"
    
    link_enc = urllib.parse.quote(link_app)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={link_enc}"
    st.image(qr_url, caption="Escaneie com a câmera do celular")

aba_chat, aba_midia = st.tabs(["💬 Conversa Livre", "📁 Enviar Arquivos & Fotos"])

# ABA 1: CHAT LIVRE
with aba_chat:
    if "historico" not in st.session_state:
        st.session_state.historico = [
            {"role": "assistant", "content": "Olá! Sou o Mentor IA. Podemos conversar sobre qualquer assunto! Como posso te ajudar hoje?"}
        ]

    for msg in st.session_state.historico:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua mensagem aqui..."):
        st.session_state.historico.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Puxa a chave cadastrada nos Secrets
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                st.markdown(response.text)
                st.session_state.historico.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao processar: {str(e)}")

# ABA 2: ENVIO DE ARQUIVOS
with aba_midia:
    st.subheader("📷 Análise de Arquivos")
    arquivo = st.file_uploader("Escolha um arquivo para enviar:", type=["png", "jpg", "jpeg", "pdf", "txt"])
    
    if arquivo and st.button("Analisar Arquivo"):
        st.success(f"Arquivo '{arquivo.name}' recebido com sucesso!")
