import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

class EmailSender:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    def _create_email(self, from_addr, subject, body, is_html=False):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['Subject'] = subject

        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        return msg

    def add_table(self, msg, table_data):
        html_table = "<table border='1'>"
        for row in table_data:
            html_table += "<tr>"
            for cell in row:
                html_table += f"<td>{cell}</td>"
            html_table += "</tr>"
        html_table += "</table>"
        
        table_part = MIMEText(html_table, 'html')
        msg.attach(table_part)

    def add_attachment(self, msg, filepath, filename=None):
        if not filename:
            filename = filepath.split("/")[-1]
        
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)

    def add_image(self, msg, image_path, image_id):
        with open(image_path, "rb") as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header('Content-ID', f'<{image_id}>')
            msg.attach(mime_img)

    def send_email(self, from_addr, to_addr, subject, body, is_html=False):
        msg = self._create_email(from_addr, subject, body, is_html)

        try:
            with smtplib.SMTP(self.server_address, self.server_port) as server:
                server.sendmail(from_addr, to_addr, msg.as_string())
                print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar o email: {str(e)}")

# Exemplo de uso:
sender = EmailSender("smtp.server.com", 25)
email_body = "Olá! Veja a tabela e imagem abaixo.<br>"
msg = sender._create_email("your_email@example.com", "Teste de Tabela e Imagem", email_body, True)

table_data = [
    ["Nome", "Idade", "Cidade"],
    ["Alice", 28, "São Paulo"],
    ["Bob", 30, "Rio de Janeiro"]
]
sender.add_table(msg, table_data)
sender.add_image(msg, "path_to_image.jpg", "image1")
sender.send_email("your_email@example.com", "recipient@example.com", "Teste", msg.as_string(), True)
