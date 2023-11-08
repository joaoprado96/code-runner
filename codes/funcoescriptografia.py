from cryptography.fernet import Fernet

# Função para gerar uma chave. Você deve guardar essa chave em um local seguro!
def generate_key():
    return Fernet.generate_key()

# Função para carregar a chave. Você deve usar a mesma chave que usou para criptografar os dados.
def load_key(key_file):
    return open(key_file, "rb").read()

# Função para criptografar a mensagem
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Função para descriptografar a mensagem
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Exemplo de uso
key = generate_key()  # Guarde essa chave em um arquivo ou variável de ambiente

# Imagine que você guarda a chave em um arquivo para uso posterior
with open("secret.py", "w") as key_file:
    key_file.write(f"CHAVE_CRIPTOGRAFADA = {str(key)}")

# Criptografa a senha
senha = "minha_senha_super_secreta"
senha_criptografada = encrypt_message(senha, key)
print(f"Senha criptografada: {senha_criptografada}")

# Para descriptografar, precisamos carregar a mesma chave
key_loaded = load_key("secret.key")

# Descriptografa a senha
senha_descriptografada = decrypt_message(senha_criptografada, key_loaded)
print(f"Senha descriptografada: {senha_descriptografada}")
