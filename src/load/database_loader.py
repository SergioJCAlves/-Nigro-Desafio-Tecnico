import psycopg2
import configparser
from typing import Dict
from src.utils import logger

# Carrega as configurações
config = configparser.ConfigParser()
config.read('config/config.ini')

# Configura o logger
log = logger.get_logger(__name__)

class DatabaseLoader:
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados PostgreSQL.
        """
        self.host = config['database']['host']
        self.port = config['database']['port']
        self.dbname = config['database']['dbname']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.conn = None

    def connect(self):
        """
        Conecta ao banco de dados.
        """
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            log.info("Conexão com o banco de dados estabelecida com sucesso.")
        except psycopg2.Error as e:
            log.error(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        """
        Desconecta do banco de dados.
        """
        if self.conn:
            self.conn.close()
            log.info("Desconexão do banco de dados realizada com sucesso.")

    def create_table(self):
        """
        Cria a tabela no banco de dados, se ela não existir.
        """
        if not self.conn:
            log.error("Não há conexão com o banco de dados.")
            return
        
        try:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documentos (
                    id SERIAL PRIMARY KEY,
                    numero_documento VARCHAR(255),
                    data_emissao DATE,
                    valor NUMERIC,
                    fonte VARCHAR(50)
                );
            """)
            self.conn.commit()
            log.info("Tabela 'documentos' criada (se não existia) com sucesso.")
            cur.close()
        except psycopg2.Error as e:
            log.error(f"Erro ao criar a tabela: {e}")
            self.conn.rollback()

    def insert_data(self, data: Dict):
        """
        Insere os dados no banco de dados.
        Args:
            data (Dict): Dicionário contendo os dados a serem inseridos.
        """
        if not self.conn:
            log.error("Não há conexão com o banco de dados.")
            return
        
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO documentos (numero_documento, data_emissao, valor, fonte)
                VALUES (%s, %s, %s, %s);
            """, (data["numero_documento"], data["data_emissao"], data["valor"], data["fonte"]))
            self.conn.commit()
            log.info(f"Dados inseridos com sucesso: {data}")
            cur.close()
        except psycopg2.Error as e:
            log.error(f"Erro ao inserir dados: {e}")
            self.conn.rollback()

if __name__ == "__main__":
    # Exemplo de uso
    loader = DatabaseLoader()
    loader.connect()
    loader.create_table()
    
    data = {"numero_documento": "12345", "data_emissao": "2024-05-20", "valor": 1000.00, "fonte": "Planilha"}
    loader.insert_data(data)
    
    loader.disconnect()