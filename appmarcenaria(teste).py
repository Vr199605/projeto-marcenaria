import streamlit as st
import smtplib
from email.message import EmailMessage
import tempfile
import os

# Tenta importar a ferramenta de PDF
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    PDF_DISPONIVEL = True
except ImportError:
    PDF_DISPONIVEL = False

# 1. ESTILO E CONFIGURAÇÃO
st.set_page_config(page_title="PRmarcenaria", page_icon="🪵")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1 { color: #3e2723; text-align: center; font-family: 'serif'; }
    .stButton>button { background-color: #3e2723; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. INTERFACE PRINCIPAL
st.title("PRmarcenaria")
st.write("---")

if not PDF_DISPONIVEL:
    st.error("O servidor ainda está configurando as ferramentas de PDF. Por favor, aguarde 30 segundos e dê um 'F5'.")
    st.stop()

# Galeria de Fotos Fixa (Substitui o expander que estava quebrado)
st.subheader("⭐ Nossos Projetos")
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg", caption="Cozinhas")
with col2:
    st.image("https://images.pexels.com/photos/2724748/pexels-photo-2724748.jpeg", caption="Salas")

st.write("---")

# 3. FORMULÁRIO
with st.form("meu_form"):
    st.subheader("🖋️ Solicitar Orçamento")
    nome = st.text_input("Seu Nome")
    whatsapp = st.text_input("Seu WhatsApp")
    ambiente = st.selectbox("Ambiente", ["Cozinha", "Quarto", "Sala", "Banheiro"])
    movel = st.text_area("Descreva o móvel desejado")
    
    btn_enviar = st.form_submit_button("ENVIAR PROJETO")

# 4. LÓGICA DE ENVIO
if btn_enviar:
    if nome and whatsapp:
        try:
            # Gerar PDF Simples
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(tmp.name, pagesize=A4)
            c.drawString(100, 800, f"Projeto: {nome}")
            c.drawString(100, 780, f"WhatsApp: {whatsapp}")
            c.drawString(100, 760, f"Ambiente: {ambiente}")
            c.drawString(100, 740, f"Detalhes: {movel}")
            c.save()

            # Enviar E-mail
            msg = EmailMessage()
            msg['Subject'] = f"Novo Briefing - {nome}"
            msg['From'] = "SEU_EMAIL@gmail.com" # Coloque seu e-mail
            msg['To'] = "victormoreiraicnv@gmail.com"
            msg.set_content(f"Novo pedido de orçamento recebido.")
            
            with open(tmp.name, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"{nome}.pdf")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("SEU_EMAIL@gmail.com", "SUA_SENHA_DE_APP") # Coloque sua senha de app
                smtp.send_message(msg)

            st.success("Tudo certo! Projeto enviado para análise.")
            st.balloons()
            os.remove(tmp.name)
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Preencha os campos obrigatórios.")
