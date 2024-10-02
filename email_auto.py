# *-* coding: utf-8 *-*

import smtplib
import traceback
import gerenciador
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


# FUNÇÃO QUE RECEBE OS PARÂMETROS DE EMAIL PARA FAZER O ENVIO
def enviar_email(remetente, senha, destinatario, assunto, mensagem, anexo=None, anexo_nome=None, empresa=None, categoria=None, data_vencimento=None):
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

        if empresa and categoria and data_vencimento is not None:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Enviado', data_vencimento=data_vencimento)
            return f'Email enviado com sucesso {destinatario}'
        else:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Enviado', erro="Empresa, Categoria ou Data Vencimento Vazios", data_vencimento=data_vencimento)
            return f'Email enviado com sucesso!! Aviso: sem categoria, empresa ou data vencimento'
    
    except smtplib.SMTPAuthenticationError as e:
        erro_msg = f'Erro de autenticação: {e}'
        if empresa and categoria and data_vencimento:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=erro_msg, data_vencimento=data_vencimento)
        else:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=f"Smtplib Vazio: {e}", data_vencimento=data_vencimento)
        return erro_msg

    except smtplib.SMTPException as e:

        erro_msg = f'Erro SMTP: {e}'
        if empresa and categoria and data_vencimento:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=erro_msg, data_vencimento=data_vencimento)
        else:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=f"SMTP Vazio: {e}", data_vencimento=data_vencimento)          
        return erro_msg

    except Exception as e:
        erro_trace = traceback.format_exc()
        erro_msg = f'Erro inesperado: {e}\n{erro_trace}'
        if empresa and categoria and data_vencimento:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=erro_msg, data_vencimento=data_vencimento)
        else:
            gerenciador.relatorios(empresa=empresa, documento=categoria, status='Falha', erro=f"Exception Vazio: {e}", data_vencimento=data_vencimento)
        return erro_msg

    finally:
        servidor.quit()