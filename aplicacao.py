# *-* coding: utf-8 *-*

import os
import webbrowser
import threading
import gerenciador
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, jsonify, redirect, request, send_file


# INICIALIZAÇÃO DAS VARIÁVEIS PREDEFINÇÃO DO SISTEMA TOP_VPN
load_dotenv()
sistema = Flask(__name__)
sistema.secret_key = os.getenv('SECRET_KEY')
CORS(sistema)


# ROTA DE REDIRECIONAMENTO PADRÃO PARA SISTEMA LOCAL
@sistema.route("/", methods=["GET"])
def padrao():
    return redirect('/AutoDoc')


# ROTA PRINCIPAL DE CONTROLE PARA FUNCIONALIDADES DO SISTEMA
@sistema.route("/AutoDoc", methods=["GET", "POST"])
def principal():
    if request.method == "GET":
        ultimos_dados = gerenciador.ultimos_dados()
        return render_template("documentos.html", dados=ultimos_dados)
    
    elif request.method == "POST":
        filtro = request.form.get("documentFilter", "").lower()
        dados_filtrados = gerenciador.filtrar_dados(filtro)
        return render_template("documentos.html", dados=dados_filtrados)


# ROTA PARA ENVIAR EMAIL MANUALMENTE NO SISTEMA
@sistema.route("/Email", methods=["GET", "POST"])
def email():
    if request.method == "GET":
        return render_template("email.html")
    
    elif request.method == "POST":
        destinatario = request.form.get('emailDestinatario')
        assunto  = request.form.get('assunto')
        mensagem = request.form.get('mensagem')
        anexo = request.files.get('anexarDocumento')
        categoria = request.form.get('categoria')
        data_vencimento = request.form.get('dataVencimento')

        if data_vencimento:
            data_vencimento = datetime.strptime(data_vencimento, '%Y-%m-%d').strftime('%d-%m-%Y %H:%M:%S')

        if anexo:
            status = gerenciador.emails_manuais(destinatario=destinatario, assunto=assunto, mensagem=mensagem, caminho_anexo=anexo, categoria=categoria, data_vencimento=data_vencimento)
        else:
            status = gerenciador.emails_manuais(destinatario=destinatario, assunto=assunto, mensagem=mensagem, categoria=categoria, data_vencimento=data_vencimento)
  
        return status
    

# ROTA PARA CONFIGURAR O SISTEMA E CADASTRAR CONFIGURAÇÕES
@sistema.route("/Config", methods=["GET", "POST"])
def config():
    if request.method == "GET":
        load_dotenv()
        dados = dotenv_values(".env")
        config_dados = {
            "documentos": dados['DOCS'],
            "downloads": dados['DOWN'],
            "email_padrao": dados['EMAIL'],
            "senha_padrao": dados['SENHA'],
            "assunto_padrao": dados['ASSUNTO'],
            "mensagem_padrao": dados['MENSAGEM'],
            "ano_docs": dados['ANO']
            }

        return render_template("config.html", config=config_dados)
    
    if request.method == "POST":
        documentos = request.form.get("documentos")
        downloads = request.form.get("downloads")
        email_padrao = request.form.get("emailPadrao")
        senha_padrao = request.form.get("senhaPadrao")
        assunto_padrao = request.form.get("assuntoEmail")
        mensagem_padrao = request.form.get("mensagemEmail")
        ano_docs = request.form.get("anodocs")

        gerenciador.atualiza_env(documentos, downloads, email_padrao, senha_padrao, assunto_padrao, mensagem_padrao, ano_docs) 
        return jsonify({"message": "sucesso"})


# ROTA PARA CADASTRAR DADOS DE CLIENTES
@sistema.route("/Cadastrar", methods=["POST"])
def clientes():
    if request.method == "POST":
        nome_cliente = request.form.get("nomeEmpresa")
        email_cliente  = request.form.get("emailCliente")

        if nome_cliente and email_cliente:
            gerenciador.cadastra_dados(nome_cliente, email_cliente)
            return jsonify({"message": "sucesso"})
        
    return jsonify({"messagem": "error"})


# ROTA PARA EXIBIR OS LOGS DO SISTEMA
@sistema.route("/Logs", methods=["GET", "POST"])
def logs():
    data_filtro = request.form.get("logDateFilter")
    registros = gerenciador.retorna_registros(data_filtro)
    return render_template("logs.html", registros=registros)


# ROTA PARA EXIBIR O RELATORIO DE ENVIOS
@sistema.route("/Relatorios", methods=["GET", "POST"])
def relatorios():
    data_filtro = request.args.get('data')
    empresa_filtro = request.args.get('empresa')
    documento_filtro = request.args.get('documento')

    relatorios = gerenciador.retorna_relatorios(data_filtro=data_filtro, empresa_filtro=empresa_filtro, documento_filtro=documento_filtro)
    return render_template('relatorios.html', relatorios=relatorios)


# ROTA PARA EXPORTAR ARQUIVO .TXT NA MÁQUINA CLIENTE
@sistema.route("/exportar_logs", methods=["POST"])
def exportar_logs():
    data_filtro = request.form.get("logDateFilter")
    registros = gerenciador.retorna_registros(data_filtro)
    caminho_arquivo = "logs_filtrados.txt"

    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(registros)

    return send_file(caminho_arquivo, as_attachment=True)



# INICIA MONITORAMENTO DOS DOWNLOADS DE ARQUIVOS .PDFs
def iniciar_monitoramento():
    monitoramento_thread = threading.Thread(target=gerenciador.monitorar_pdfs)
    monitoramento_thread.daemon = True 
    monitoramento_thread.start()

# INICIA SERVIÇO FLASK
def iniciar_servidor():
    sistema.run(host='0.0.0.0', port=8010)

# FUNÇÃO QUE INICIALIZA SISTEMA WEB FLASK
if __name__ == '__main__':
    iniciar_monitoramento()
    thread = threading.Thread(target=iniciar_servidor)
    thread.start()
    webbrowser.open("http://127.0.0.1:8010")