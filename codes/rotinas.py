import json
class RotinaProcessor:
    def __init__(self):
        # Configuração dos tamanhos de cada campo
        self.layout = {
            "ROTINA": 8,
            "EXEC_TS2": 3,
            "EXEC_TS6": 3,
            "EXEC_TS8": 3,
            "EXEC_TT7": 3,
            "ULTIMO_PROCESSAMENTO": 12,
            "ARQUIVO_TS2": 3,
            "ARQUIVO_TS6": 3,
            "ARQUIVO_TS8": 3,
            "ARQUIVO_TT7": 3,
            "MOTOR": 3,
            "E_S": 3,
            "NOME_DO_ARQUIVO": 46,
            "INCLUDE": 8
        }
        self.rotinas = {}

    def process_line(self, line):
        current_pos = 0
        data = {}
        for field, length in self.layout.items():
            extraido = line[current_pos:current_pos + length].strip()
            if extraido == "X":
                data[field] = "Sim"
            else:
                if len(extraido) == 0:
                    data[field] = "Nao"
                else:
                    data[field] = extraido
            current_pos += length + 1  # Considerando a coluna em branco
        return data

    def validate_line(self, line):
        expected_length = sum(self.layout.values()) + len(self.layout) - 1
        if len(line) != expected_length:
            print(f"Linha inválida (esperado {expected_length}, encontrado {len(line)}): {line}")
            return False
        return True

    def process_file_content(self, file_content):
        for line in file_content.split('\n'):
            if line.strip() and self.validate_line(line):
                data = self.process_line(line)
                rotina = data["ROTINA"]
                if rotina not in self.rotinas:
                    self.rotinas[rotina] = {"LISTA DE ARQUIVOS": [], "ARQUIVOS": {}}
                nome_arquivo = data["NOME_DO_ARQUIVO"]
                self.rotinas[rotina]["LISTA DE ARQUIVOS"].append(nome_arquivo)
                arquivo_key = f"ARQUIVO{len(self.rotinas[rotina]['ARQUIVOS']) + 1}"
                self.rotinas[rotina]["ARQUIVOS"][arquivo_key] = data

    def get_json(self):
        return self.rotinas

# Conteúdo de exemplo do arquivo
file_content = """
ROTINA01  X   X          123456789012 123 456 789 012 XYZ 123 Nome do arquivo 1                              INCLUDE1
ROTINA01      X       X  123456789012 123 456 789 012 XYZ 123 Nome do arquivo 2                              INCLUDE2
ROTINA02  X           X  123456789012 123 456 789 012 XYZ 123 Nome do arquivo 3                              INCLUDE3
"""


# Uso da classe
processor = RotinaProcessor()
processor.process_file_content(file_content)
rotinas_json = processor.get_json()
print(json.dumps(rotinas_json))
