import streamlit as st
import urllib.parse
from google import genai
from streamlit_mic_recorder import mic_recorder

# Configuração da página
st.set_page_config(
    page_title="Mentor IA", 
    page_icon="⚡", 
    layout="centered"
)

# Estilização com a cor da fonte alterada para PRETO
st.markdown("""
<style>
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppViewerFooter {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Fundo geral */
    .stApp {
        background: linear-gradient(180deg, #0a0c10 0%, #121824 100%);
        color: #000000;
    }
    
    /* Balões de Mensagem com fundo claro e texto preto para alto contraste */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 16px !important;
        padding: 14px;
        margin-bottom: 12px;
        color: #000000 !important;
    }

    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
    }

    /* Correção do Campo de Texto (Input) - Fonte em PRETO com fundo claro */
    .stChatInput textarea, 
    .stChatInput input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #ffffff !important;
        caret-color: #0072ff !important;
    }

    /* Textos auxiliares e marcadores em preto */
    .stChatInput textarea::placeholder {
        color: #555555 !important;
        -webkit-text-fill-color: #555555 !important;
    }
    
    /* Botões */
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

aba_chat, aba_voz, aba_midia = st.tabs(["💬 Conversa Livre", "🎙️ Chat de Voz", "📁 Enviar Arquivos & Fotos"])

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
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content_stream(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                def stream_wrapper():
                    for chunk in response:
                        yield chunk.text

                texto_final = st.write_stream(stream_wrapper())
                st.session_state.historico.append({"role": "assistant", "content": texto_final})
            except Exception as e:
                st.error(f"Erro ao processar: {str(e)}")

# ABA 2: CHAT DE VOZ
with aba_voz:
    st.subheader("🎙️ Enviar mensagem de voz")
    st.write("Clique no botão abaixo para gravar seu áudio:")
    
    audio = mic_recorder(
        start_prompt="🔴 Iniciar Gravação",
        stop_prompt="⬛ Parar Gravação",
        key='recorder'
    )

    if audio:
        st.audio(audio['bytes'], format='audio/wav')

# ABA 3: ENVIO DE ARQUIVOS
with aba_midia:
    st.subheader("📷 Análise de Arquivos")
    arquivo = st.file_uploader("Escolha um arquivo para enviar:", type=["png", "jpg", "jpeg", "pdf", "txt"])
    
    if arquivo and st.button("Analisar Arquivo"):
        st.success(f"Arquivo '{arquivo.name}' recebido com sucesso!")
