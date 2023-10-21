import os

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_file(self, content=""):
        """Cria um arquivo com o conteúdo opcional fornecido."""
        try:
            with open(self.file_path, 'w') as file:
                file.write(content)
            return True, "Arquivo criado com sucesso."
        except Exception as e:
            return False, str(e)

    def write_to_file(self, content):
        """Escreve (ou sobrescreve) no arquivo com o conteúdo fornecido."""
        try:
            with open(self.file_path, 'w') as file:
                file.write(content)
            return True, "Conteúdo escrito com sucesso."
        except Exception as e:
            return False, str(e)

    def append_to_file(self, content):
        """Adiciona conteúdo ao final do arquivo."""
        try:
            with open(self.file_path, 'a') as file:
                file.write(content)
            return True, "Conteúdo adicionado com sucesso."
        except Exception as e:
            return False, str(e)

    def read_file(self):
        """Lê o conteúdo do arquivo."""
        try:
            with open(self.file_path, 'r') as file:
                return True, file.read()
        except Exception as e:
            return False, str(e)

    def delete_file(self):
        """Deleta o arquivo."""
        try:
            os.remove(self.file_path)
            return True, "Arquivo deletado com sucesso."
        except Exception as e:
            return False, str(e)

# Exemplo de uso:

# Crie uma instância do gerenciador para um caminho de arquivo específico.
file_manager = FileManager("example.txt")

# Crie um arquivo com algum conteúdo.
success, message = file_manager.create_file("Olá, Mundo!")
print(message)

# Adicione mais conteúdo ao arquivo.
success, message = file_manager.append_to_file("\nComo você está?")
print(message)

# Leia o conteúdo do arquivo.
success, content = file_manager.read_file()
if success:
    print(content)
else:
    print("Erro:", content)

# Delete o arquivo.
success, message = file_manager.delete_file()
print(message)
