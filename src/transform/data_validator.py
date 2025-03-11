from typing import Dict
from src.utils import logger
from utils.logger import get_logger

# Configura o logger
log = logger.get_logger(__name__)

def validate_data(data: Dict) -> bool:
    """
    Valida os dados extraídos.
    Args:
        data (Dict): Dicionário contendo os dados a serem validados.
    Returns:
        bool: True se os dados são válidos, False caso contrário.
    """
    try:
        # Exemplo de validação: verificar se as chaves necessárias estão presentes
        required_keys = ["numero_documento", "data_emissao", "valor"]
        if not all(key in data for key in required_keys):
            log.warning(f"Dados incompletos: {data}")
            return False
        
        # Adicione outras validações conforme necessário (ex: formato da data, tipo do valor)
        
        return True
    
    except Exception as e:
        log.error(f"Erro ao validar dados: {e}")
        return False

if __name__ == "__main__":
    # Exemplo de uso
    data = {"numero_documento": "12345", "data_emissao": "20/05/2024", "valor": "1000.00"}
    is_valid = validate_data(data)
    print(f"Os dados são válidos? {is_valid}")