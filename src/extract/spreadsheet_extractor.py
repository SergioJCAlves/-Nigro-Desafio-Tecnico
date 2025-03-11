import os
import pandas as pd
import configparser
from typing import List, Dict
from src.utils import logger

# Carrega as configurações
config = configparser.ConfigParser()
config.read('config/config.ini')

# Configura o logger
log = logger.get_logger(__name__)

def extract_data_from_spreadsheet(spreadsheet_path: str) -> List[Dict]:
    """
    Extrai dados de uma planilha (Excel ou CSV).
    Args:
        spreadsheet_path (str): Caminho para o arquivo da planilha.
    Returns:
        List[Dict]: Lista de dicionários contendo os dados extraídos.
    """
    data = []
    try:
        if spreadsheet_path.endswith(".xlsx"):
            df = pd.read_excel(spreadsheet_path)
        elif spreadsheet_path.endswith(".csv"):
            df = pd.read_csv(spreadsheet_path)
        else:
            log.warning(f"Formato de arquivo não suportado: {spreadsheet_path}")
            return data
        
        # Converte o DataFrame para uma lista de dicionários
        data = df.to_dict(orient="records")
        
    except Exception as e:
        log.error(f"Erro ao extrair dados da planilha {spreadsheet_path}: {e}")
    
    return data

def process_spreadsheets_from_dir(spreadsheet_dir: str) -> List[Dict]:
    """
    Processa todas as planilhas em um diretório.
    Args:
        spreadsheet_dir (str): Caminho para o diretório contendo as planilhas.
    Returns:
        List[Dict]: Lista de dicionários contendo os dados extraídos de todas as planilhas.
    """
    all_data = []
    for filename in os.listdir(spreadsheet_dir):
        if filename.endswith(".xlsx") or filename.endswith(".csv"):
            spreadsheet_path = os.path.join(spreadsheet_dir, filename)
            all_data.extend(extract_data_from_spreadsheet(spreadsheet_path))
    return all_data

if __name__ == "__main__":
    spreadsheet_directory = config['paths']['spreadsheet_dir']
    extracted_data = process_spreadsheets_from_dir(spreadsheet_directory)
    
    for item in extracted_data:
        print(item)