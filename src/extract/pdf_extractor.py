import os
import re
import io
import configparser
from typing import List, Dict
from pdfminer.high_level import extract_text
from src.utils import logger
from utils.logger import get_logger

# Carrega as configurações
config = configparser.ConfigParser()
config.read('config/config.ini')

# Configura o logger
log = logger.get_logger(__name__)

def extract_data_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extrai dados de um arquivo PDF.
    Args:
        pdf_path (str): Caminho para o arquivo PDF.
    Returns:
        List[Dict]: Lista de dicionários contendo os dados extraídos.
    """
    data = []
    try:
        text = extract_text(pdf_path)
        
        # Exemplo de extração com regex (ajuste conforme necessário)
        numero_documento = re.search(r"Número:\s*(\d+)", text)
        data_emissao = re.search(r"Emissão:\s*(\d{2}/\d{2}/\d{4})", text)
        valor = re.search(r"Valor:\s*([\d.,]+)", text)
        
        if numero_documento and data_emissao and valor:
            data.append({
                "numero_documento": numero_documento.group(1),
                "data_emissao": data_emissao.group(1),
                "valor": valor.group(1),
                "fonte": "PDF"
            })
        else:
            log.warning(f"Dados não encontrados no PDF: {pdf_path}")
            
    except Exception as e:
        log.error(f"Erro ao extrair dados do PDF {pdf_path}: {e}")
    
    return data

def process_pdfs_from_dir(pdf_dir: str) -> List[Dict]:
    """
    Processa todos os PDFs em um diretório.
    Args:
        pdf_dir (str): Caminho para o diretório contendo os PDFs.
    Returns:
        List[Dict]: Lista de dicionários contendo os dados extraídos de todos os PDFs.
    """
    all_data = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            all_data.extend(extract_data_from_pdf(pdf_path))
    return all_data

if __name__ == "__main__":
    pdf_directory = config['paths']['pdf_dir']
    extracted_data = process_pdfs_from_dir(pdf_directory)
    
    for item in extracted_data:
        print(item)