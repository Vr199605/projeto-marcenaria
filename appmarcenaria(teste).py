import streamlit as st
import smtplib
from email.message import EmailMessage
import tempfile
import os

# Tenta importar o ReportLab de forma segura
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    LIB_READY = True
except ImportError:
    LIB_READY = False

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="PRmarcenaria | Premium", page_icon="🪵")

# 2. ESTILO CSS (LIMPO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: #f8f9fa; }
    h1, h2 { font-family: 'Playfair Display', serif; color: #3e2723; text-align: center; }
    .stButton>button { background: #3e2723 !important; color: white !important; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. GERAR PDF
def gerar_pdf(dados):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Briefing PRmarcenaria")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Cliente: {dados['Nome']}")
    c.drawString(50, 750, f"WhatsApp: {dados['WhatsApp']}")
    c.drawString(50, 730, f"Ambiente: {dados['Ambiente']}")
    c.drawString(50, 710, f"Móvel: {dados['Movel']}")
    c.save()
    return tmp.name

# 4. ENVIAR E-MAIL
def enviar_email(pdf_path, dados):
    msg = EmailMessage()
    msg['Subject'] = f"Novo Projeto: {dados['Nome']}"
    msg['From'] = "SEU_EMAIL@gmail.com"
    msg['To'] = "victormoreiraicnv@gmail.com"
    msg.set_content(f"Dados do projeto de {dados['Nome']}.")
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename="projeto.pdf")
    
    # IMPORTANTE: Use sua senha de app aqui
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("victormoreiraicnv@gmail.com", "wepj tsnr mont tlmm")
        smtp.send_message(msg)

# 5. INTERFACE
st.markdown("<h1>PRmarcenaria</h1>", unsafe_allow_html=True)

if not LIB_READY:
    st.warning("O sistema está finalizando a instalação das ferramentas. Atualize a página em 10 segundos.")
    st.stop()

with st.form("orcamento"):
    nome = st.text_input("Seu Nome")
    whatsapp = st.text_input("Seu WhatsApp")
    ambiente = st.selectbox("Ambiente", ["Cozinha", "Quarto", "Sala", "Banheiro", "Outro"])
    movel = st.text_input("Qual móvel deseja?")
    enviar = st.form_submit_button("ENVIAR SOLICITAÇÃO")

if enviar:
    if nome and whatsapp:
        try:
            dados = {"Nome": nome, "WhatsApp": whatsapp, "Ambiente": ambiente, "Movel": movel}
            path = gerar_pdf(dados)
            enviar_email(path, dados)
            st.success("Solicitação enviada com sucesso!")
            os.remove(path)
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
    else:
        st.error("Preencha nome e WhatsApp.")
