import streamlit as st
import smtplib
from email.message import EmailMessage
import tempfile
import os

# Tenta importar o ReportLab, se falhar, mostra um aviso amigável
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    IMPORT_ERROR = False
except ImportError:
    IMPORT_ERROR = True

# 1. CONFIGURAÇÃO DE ALTO NÍVEL
st.set_page_config(page_title="PRmarcenaria | Premium Design", page_icon="🪵", layout="centered")

# 2. CSS DE LUXO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
    .stApp { background: radial-gradient(circle at top right, #fdfbfb, #ebedee); }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #3e2723 !important; }
    p, label, span, div { font-family: 'Inter', sans-serif !important; color: #5d4037; }
    .titulo-container { text-align: center; padding: 40px 0; }
    .main-title { font-size: 3.5rem; letter-spacing: -1px; margin-bottom: 0; }
    .gold-detail { color: #8d6e63; font-style: italic; font-size: 1.2rem; }
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 50px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important;
    }
    .stButton>button {
        background: #3e2723 !important;
        color: #f4f1ee !important;
        border-radius: 20px !important;
        padding: 20px 40px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border: none !important;
        width: 100% !important;
    }
    .stImage img { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DO PDF COM REPORTLAB
def gerar_pdf_reportlab(dados):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)
    width, height = A4
    c.setFillColorRGB(0.24, 0.15, 0.14) 
    c.rect(0, 0, 15, height, fill=1)
    c.setFont("Helvetica-Bold", 24)
    c.drawRightString(width - 50, height - 50, "PRmarcenaria")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, f"CLIENTE: {dados['Nome'].upper()}")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 120, f"WhatsApp: {dados['WhatsApp']}")
    c.setFillColorRGB(0.94, 0.92, 0.90)
    c.rect(40, height - 250, 515, 100, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 170, "DETALHES DO PROJETO")
    c.setFont("Helvetica", 11)
    texto = c.beginText(50, height - 190)
    texto.textLine(f"Ambiente: {dados['Ambiente']}")
    texto.textLine(f"Estilo: {dados['Estilo']}")
    texto.textLine(f"Movel: {dados['Movel']}")
    c.drawText(texto)
    c.save()
    return tmp.name

# 4. ENVIO DE E-MAIL
def enviar_email(pdf_path, dados):
    msg = EmailMessage()
    msg['Subject'] = f"✨ Novo Projeto: {dados['Nome']}"
    msg['From'] = "SEU_EMAIL@gmail.com"
    msg['To'] = "victormoreiraicnv@gmail.com"
    msg.set_content(f"Novo projeto de {dados['Nome']}.")
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"Projeto_{dados['Nome']}.pdf")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("victormoreiraicnv@gmail.com", "wepj tsnr mont tlmm")
        smtp.send_message(msg)

# 5. IMAGENS
fotos = [
    "https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?w=800",
    "https://images.pexels.com/photos/2724748/pexels-photo-2724748.jpeg?w=800",
    "https://images.pexels.com/photos/2062426/pexels-photo-2062426.jpeg?w=800",
    "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?w=800"
]

# 6. INTERFACE
st.markdown("""
    <div class="titulo-container">
        <h1 class="main-title">PRmarcenaria</h1>
        <p class="gold-detail">Design que transforma, marcenaria que perdura.</p>
    </div>
    """, unsafe_allow_html=True)

if IMPORT_ERROR:
    st.error("O servidor está instalando as ferramentas de PDF. Por favor, aguarde 30 segundos e atualize a página.")
    st.stop()

st.write("### ⭐ Projetos em Destaque")
col1, col2 = st.columns(2)
with col1: st.image(fotos[0], caption="Cozinhas Modernas")
with col2: st.image(fotos[1], caption="Painéis de TV")

st.write("---")
st.write("### 🏺 Galeria de Referências")
c1, c2 = st.columns(2)
with c1: st.image(fotos[2], use_container_width=True)
with c2: st.image(fotos[3], use_container_width=True)

st.write("---")

with st.form("form_luxo", clear_on_submit=True):
    st.write("### 🖋️ Inicie sua Consultoria")
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp")
    ambiente = st.selectbox("Ambiente", ["Cozinha", "Living", "Suíte", "Gourmet", "Home Office"])
    estilo = st.radio("Estilo Preferido", ["Moderno", "Industrial", "Clássico", "Minimalista"])
    tipo_movel = st.text_input("Móvel desejado")
    descricao = st.text_area("Como você imagina esse projeto?")
    submit = st.form_submit_button("SOLICITAR ORÇAMENTO PREMIUM")

if submit:
    if nome and whatsapp:
        dados = {"Nome": nome, "WhatsApp": whatsapp, "Ambiente": ambiente, "Estilo": estilo, "Movel": tipo_movel, "Descricao": descricao}
        try:
            with st.spinner('Gerando briefing...'):
                path = gerar_pdf_reportlab(dados)
                enviar_email(path, dados)
                st.success(f"Obrigado, {nome}. Briefing enviado!")
                st.balloons()
                os.remove(path)
        except Exception as e:
            st.error(f"Erro: {e}")