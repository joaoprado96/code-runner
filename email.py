from exchangelib import Credentials, Account, DELEGATE, Message, DELEGATE

# Defina suas credenciais
credentials = Credentials('your_email@example.com', 'your_password')

# Crie uma conta e especifique o servidor (opcionalmente) e as credenciais
account = Account('your_email@example.com', credentials=credentials, autodiscover=True, access_type=DELEGATE)

# Criar e enviar e-mail
m = Message(
    account=account,
    folder=account.sent,
    subject='Assunto do e-mail',
    body='Corpo do e-mail',
    to_recipients=['destinatario@example.com'],
    cc_recipients=['cc@example.com'],  # opcional
    bcc_recipients=['bcc@example.com']  # opcional
)
m.send_and_save()
