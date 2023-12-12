import hvac
import os
import sys

class VaultCertificateManager:
    def __init__(self, vault_url, vault_token, secret_path, vault_folder):
        self.vault_url = vault_url
        self.vault_token = vault_token
        self.secret_path = secret_path
        self.vault_folder = os.path.join(os.path.dirname(__file__), vault_folder)
        self.cert_file = os.path.join(self.vault_folder, 'cert.pem')
        self.key_file = os.path.join(self.vault_folder, 'key.pem')
        self.client = None
        self.certificate = None
        self.private_key = None

    def connect_to_vault(self):
        try:
            self.client = hvac.Client(url=self.vault_url, token=self.vault_token)
            if not self.client.is_authenticated():
                raise ConnectionError("Falha na autenticação com o Vault.")
        except Exception as e:
            print(f"Erro ao conectar ao Vault: {e}", file=sys.stderr)
            raise

    def get_vault_credentials(self):
        if self.client is None:
            raise ValueError("Cliente Vault não inicializado. Chame 'connect_to_vault()' primeiro.")

        try:
            read_response = self.client.secrets.kv.v2.read_secret_version(path=self.secret_path)
            return read_response['data']['data']
        except Exception as e:
            print(f"Erro ao obter credenciais do Vault: {e}", file=sys.stderr)
            raise

    def load_certificates(self):
        if not os.path.exists(self.cert_file) or not os.path.exists(self.key_file):
            raise FileNotFoundError("Arquivos de certificado não encontrados.")

        try:
            with open(self.cert_file, 'r') as cert_file:
                self.certificate = cert_file.read()

            with open(self.key_file, 'r') as key_file:
                self.private_key = key_file.read()
        except Exception as e:
            print(f"Erro ao carregar certificados: {e}", file=sys.stderr)
            raise

    def initialize_certificates(self):
        if self.certificate is None or self.private_key is None:
            raise ValueError("Certificados não carregados. Chame 'load_certificates()' primeiro.")

        try:
            # Aqui você pode adicionar lógica para inicializar seus certificados
            # Por exemplo, configurar variáveis de ambiente, etc.
            pass
        except Exception as e:
            print(f"Erro ao inicializar certificados: {e}", file=sys.stderr)
            raise

# Exemplo de uso
vault_url = 'http://your-vault-server:8200'
vault_token = 'your-vault-token'
secret_path = 'path/to/your/secret'
vault_folder = 'vault'

manager = VaultCertificateManager(vault_url, vault_token, secret_path, vault_folder)
try:
    manager.connect_to_vault()
    credentials = manager.get_vault_credentials()
    print("Credenciais obtidas:", credentials)
    manager.load_certificates()
    manager.initialize_certificates()
    # A partir daqui, os certificados e credenciais estão prontos para serem usados
except Exception as e:
    print(f"Erro durante a operação: {e}", file=sys.stderr)
