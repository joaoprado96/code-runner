import jwt
from jwt.exceptions import DecodeError

class JWTHandler:
    def decode_token(self, token):
        try:
            # Decodificar o token sem verificar a assinatura
            decoded = jwt.decode(token, options={"verify_signature": False})
            return True, decoded
        except DecodeError:
            return False, "Token inválido ou mal formatado."
        except Exception as e:
            return False, f"Erro desconhecido: {str(e)}"

# Uso da classe
token_handler = JWTHandler()

# Substitua 'seu_jwt_token' pelo seu token JWT
token = "seu_jwt_token"

success, result = token_handler.decode_token(token)
if success:
    print("Token decodificado com sucesso:", result)
else:
    print("Erro ao decodificar o token:", result)
