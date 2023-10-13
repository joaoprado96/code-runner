import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_outlook_email(subject, body, to_email, from_email, password):
    # Configurações SMTP para Outlook
    SMTP_SERVER = 'smtp-mail.outlook.com'
    SMTP_PORT = 587  # TLS port

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conexão e envio
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Exemplo de uso
if __name__ == "__main__":
    your_email = 'seu_email@outlook.com'
    your_password = 'sua_senha'
    
    recipient_email = 'destinatario@example.com'
    subject = 'Teste de E-mail'
    body = 'Olá! Isso é um teste de envio de e-mail via Outlook.'

    send_outlook_email(subject, body, recipient_email, your_email, your_password)
