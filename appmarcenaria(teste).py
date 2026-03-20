import streamlit as st
import smtplib
from email.message import EmailMessage
import tempfile
import os

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="PRmarcenaria | Premium", page_icon="🪵", layout="centered")

# 2. CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp { background: #fdfbfb; }
    h1, h2 { font-family: 'Playfair Display', serif; color: #3e2723; text-align: center; }
    [data-testid="stForm"] { background: white !important; border-radius: 20px !important; padding: 40px !important; }
    .stButton>button { background: #3e2723 !important; color: white !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNÇÃO PARA GERAR O TXT BEM FORMATADO
def gerar_txt_formatado(dados):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8')
    
    # Criando um visual "bonito" dentro do TXT usando caracteres
    layout = f"""
    ====================================================
                P R M A R C E N A R I A
               Briefing de Projeto Premium
    ====================================================
    
    DATA DO PEDIDO: {st.session_state.get('data_atual', '20/03/2026')}
    
    [ DADOS DO CLIENTE ]
    ----------------------------------------------------
    NOME: {dados['Nome'].upper()}
    WHATSAPP: {dados['WhatsApp']}
    
    [ DETALHES DO AMBIENTE ]
    ----------------------------------------------------
    AMBIENTE: {dados['Ambiente']}
    ESTILO: {dados['Estilo']}
    MÓVEL DESEJADO: {dados['Movel']}
    
    [ DESCRIÇÃO ADICIONAL ]
    ----------------------------------------------------
    {dados['Descricao']}
    
    ====================================================
      Design que transforma, marcenaria que perdura.
    ====================================================
    """
    tmp.write(layout)
    tmp.close()
    return tmp.name

# 4. FUNÇÃO PARA ENVIAR E-MAIL
def enviar_email(arquivo_path, dados):
    msg = EmailMessage()
    msg['Subject'] = f"✨ Novo Projeto: {dados['Nome']}"
    msg['From'] = "SEU_EMAIL@gmail.com"
    msg['To'] = "victormoreiraicnv@gmail.com"
    msg.set_content(f"Olá, você recebeu um novo briefing de {dados['Nome']}. O arquivo detalhado está em anexo.")
    
    with open(arquivo_path, 'rb') as f:
        msg.add_attachment(
            f.read(), 
            maintype='text', 
            subtype='plain', 
            filename=f"Briefing_{dados['Nome']}.txt"
        )
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("victormoreiraicnv@gmail.com", "wepj tsnr mont tlmm")
        smtp.send_message(msg)

# 5. INTERFACE
st.markdown("<h1>PRmarcenaria</h1>", unsafe_allow_html=True)

with st.form("orcamento_luxo", clear_on_submit=True):
    st.subheader("🖋️ Solicitar Consultoria")
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp com DDD")
    
    col1, col2 = st.columns(2)
    with col1:
        ambiente = st.selectbox("Ambiente", ["Cozinha", "Dormitório", "Sala de Estar", "Banheiro", "Gourmet", "Escritório"])
    with col2:
        estilo = st.radio("Estilo", ["Moderno", "Clássico", "Minimalista", "Industrial"])
        
    movel = st.text_input("Qual móvel você imagina?")
    descricao = st.text_area("Conte-nos mais detalhes (opcional)")
    
    enviar = st.form_submit_button("ENVIAR PROJETO")

if enviar:
    if nome and whatsapp:
        try:
            with st.spinner('Organizando seu briefing...'):
                dados = {
                    "Nome": nome, 
                    "WhatsApp": whatsapp, 
                    "Ambiente": ambiente, 
                    "Movel": movel, 
                    "Estilo": estilo,
                    "Descricao": descricao
                }
                path = gerar_txt_formatado(dados)
                enviar_email(path, dados)
                st.success(f"Tudo pronto, {nome}! Recebemos sua solicitação.")
                st.balloons()
                os.remove(path)
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
    else:
        st.warning("Por favor, preencha os campos obrigatórios.")
