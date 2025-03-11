import logging
import logging.config

def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado.
    Args:
        name (str): Nome do logger.
    Returns:
        logging.Logger: Logger configurado.
    """
    logging.config.fileConfig('config/logging.conf')
    return logging.getLogger(name)

if __name__ == "__main__":
    # Exemplo de uso
    log = get_logger(__name__)
    log.info("Este é um exemplo de log.")