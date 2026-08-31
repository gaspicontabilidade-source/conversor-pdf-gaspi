import os
try:
    import fitz
except ImportError:
    import pymupdf as fitz

from pdf2docx import Converter
import streamlit as st

# Configuração da página e visual
st.set_page_config(
    page_title="Conversor de Documentos - GASPI Contabilidade",
    page_icon="📄",
    layout="centered"
)

# Estilização CSS para fontes e cores
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .main-title {
        color: #1A365D;
        font-weight: 700;
        font-size: 26px;
        margin-top: -10px;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #4A5568;
        font-size: 15px;
        margin-bottom: 25px;
    }
    
    div.stButton > button {
        background-color: #1A365D !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        border: none !important;
        width: 100% !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    
    div.stButton > button:hover {
        background-color: #2B6CB0 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Exibição da Logo
if os.path.exists("logo.png"):
    st.image("logo.png", width=220)
elif os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=220)

st.markdown('<div class="main-title">Conversor Interno de Documentos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Plataforma segura da <b>GASPI Contabilidade</b> para conversão de arquivos.</div>', unsafe_allow_html=True)

# Upload de arquivos
uploaded_files = st.file_uploader(
    "Arraste ou selecione os arquivos PDF aqui", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    opcao = st.radio(
        "Escolha o formato desejado:",
        ["Converter PDF para Word (.docx)", "Converter PDF para PDF/A (Padrão de Arquivamento)"]
    )

    if st.button("Iniciar Conversão"):
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            original_name = os.path.splitext(uploaded_file.name)[0]
            
            # --- CONVERSÃO PARA WORD ---
            if opcao == "Converter PDF para Word (.docx)":
                temp_pdf_path = f"temp_{uploaded_file.name}"
                docx_output_path = f"{original_name}.docx"
                
                with open(temp_pdf_path, "wb") as f:
                    f.write(file_bytes)
                
                cv = Converter(temp_pdf_path)
                cv.convert(docx_output_path)
                cv.close()
                
                with open(docx_output_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Baixar {original_name}.docx",
                        data=f,
                        file_name=f"{original_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
                if os.path.exists(docx_output_path):
                    os.remove(docx_output_path)

            # --- CONVERSÃO PARA PDF/A (ARQUIVAMENTO) ---
            elif opcao == "Converter PDF para PDF/A (Padrão de Arquivamento)":
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                pdfa_output_path = f"{original_name}_PDFA.pdf"
                
                doc.save(
                    pdfa_output_path,
                    garbage=4,
                    deflate=True,
                    clean=True
                )
                doc.close()

                with open(pdfa_output_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Baixar {original_name}_PDFA.pdf",
                        data=f,
                        file_name=f"{original_name}_PDFA.pdf",
                        mime="application/pdf"
                    )
                    
                if os.path.exists(pdfa_output_path):
                    os.remove(pdfa_output_path)
                    
        st.success("Processamento concluído com sucesso!")
