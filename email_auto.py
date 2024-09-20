# *-* coding: utf-8 *-*

import smtplib
import gerenciador
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# FUNÇÃO QUE RECEBE OS PARÂMETROS DE EMAIL PARA FAZER O ENVIO
def enviar_email(remetente, senha, destinatario, assunto, mensagem, anexo=None, anexo_nome=None):
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    try:
        servidor.login(remetente, senha)

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem,'plain'))

        if anexo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(anexo.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={anexo_nome if anexo_nome!=None else anexo.filename}')
            msg.attach(part)
        
        servidor.send_message(msg)
        gerenciador.registros(f"Email enviado: {destinatario}")
        return f'Email enviado com sucesso {destinatario}'
    
    except Exception as e:
        gerenciador.registros(f"Erro ao enviar email para {destinatario}: {e}")

    finally:
        servidor.quit()