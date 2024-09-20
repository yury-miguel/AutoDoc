# *-* coding: utf-8 *-*

import os
import re
import PyPDF2
import gerenciador


# REALIZA PROCESSO DE LEITURA DO PDF
class ExtracaoPdf:
    def __init__(self, caminho_pdf):
        self.nome = None
        self.categoria = None
        self.caminho_pdf = caminho_pdf
        self.processar_pdf()

    # REPRESENTAÇÃO DA CLASSE IMPRESSA
    def __repr__(self):
        return f"Nome: {self.nome}, Categoria: {self.categoria}"

    # PROCESSA PDF E REALIZA EXTRAÇÃO
    def processar_pdf(self):
        self.categoria = self.classificar_por_nome_arquivo()

        if self.categoria:
            texto_pdf = self.extrair_texto_pdf()

            if texto_pdf:
                self.nome = self.extrair_nome(texto_pdf, self.categoria)
            else:
                gerenciador.registros(f"Erro ao processar pdf: Texto não extraído")
                return 'erro'

        elif self.categoria is None:
            texto_pdf = self.extrair_texto_pdf()

            if texto_pdf:
                texto_categoria = self.normalizar_texto(texto_pdf)
                self.categoria = self.classificar_pdf(texto_categoria)

                if self.categoria:
                    self.nome = self.extrair_nome(texto_pdf, self.categoria)

                    if self.nome is None:
                        gerenciador.registros(f"Erro ao processar pdf: Nome não encontrado no documento")
                else:
                    gerenciador.registros(f"Erro ao processar pdf: Categoria não encontrada no nome ou documento")
                    return 'erro'
            else:
                gerenciador.registros(f"Erro ao processar pdf: Texto não extraído")
                return 'erro'

    # EXTRAI O TEXTO
    def extrair_texto_pdf(self):
        try:
            with open(self.caminho_pdf, 'rb') as arquivo:
                leitor_pdf = PyPDF2.PdfReader(arquivo)
                texto_pdf = "".join([leitor_pdf.pages[pagina].extract_text() for pagina in range(len(leitor_pdf.pages))])
            return texto_pdf
        
        except Exception as e:
            gerenciador.registros(f"Erro ao ler o PDF: {e}")
            return None

    # NORMALIZA  TEXTO PARA UM PADRÃO DE LEITURA DIFERENTE
    def normalizar_texto(self, texto_pdf):
        return re.sub(r'\s+', ' ', texto_pdf.strip()).lower()

    # FUNÇÃO PARA CLASSIFICAR PELO NOME DO ARQUIVO PDF
    def classificar_por_nome_arquivo(self):
        nome_arquivo = os.path.basename(self.caminho_pdf).lower()

        padroes_nome_arquivo = {
            "CNPJ": r"cnpj",
            "CND ESTADUAL": r"cnd[_\s]?estadual",
            "CND FEDERAL": r"cnd[_\s]?federal",
            "CND MUNICIPAL": r"cnd[_\s]?municipal",
            "CND TRABALHISTA": r"cnd[_\s]?trabalhista",
            "COFINS": r"cofins",
            "CSLL": r"csll",
            "DAS": r"das",
            "FGTS": r"fgts",
            "INSS": r"inss",
            "IRPJ": r"irpj",
            "PARCELAMENTO MEI": r"parcelamento[_\s]?mei",
            "PARCELAMENTO SIMPLES": r"parcelamento[_\s]?simples",
            "PIS": r"pis",
            "RECIBO PAGAMENTO": r"recibo[_\s]?pagamento|recibo pagamento|recibo"
        }

        for categoria, padrao in padroes_nome_arquivo.items():
            if re.search(padrao, nome_arquivo):
                return categoria

        return None

    # CLASSIFICA O PDF EM CATEGORIAS
    def classificar_pdf(self, texto_pdf):
        padroes = {
            "CNPJ": r"república federativa do brasil|república federa tiva do brasil|cadastro nacional da pessoa jurídica",
            "CND FEDERAL": r"fazenda receita federal|certidão negativa de débitos tributários e de dívida ativa federal|tributos federais|tributo federal|débito federal|débitos federais",
            "CND ESTADUAL": r"fazenda receita estadual|certidão negativa de débitos tributários e de dívida ativa estadual|tributos estaduais|tributo estadual|débito estadual|débitos estaduais",
            "CND MUNICIPAL": r"municipio|municipais|municipal|certidão negativa de débitos municipais",
            "CND TRABALHISTA": r"certidão negativa de débitos trabalhistas",
            "CNPJ": r"cadastro nacional da pessoa jurídica",
            "COFINS": r"cofins sobre o faturamento",
            "CSLL": r"csll - lucro presumido",
            "DAS": r"documento de arrecadação do simples nacional",
            "FGTS": r"gfd - guia do fgts digital",
            "INSS": r"documento de arrecadação de receitas federais",
            "IRPJ": r"irpj - lucro presumido",
            "PARCELAMENTO MEI": r"das de parcmei",
            "PARCELAMENTO SIMPLES": r"das de parcsn",
            "PIS": r"pis sobre o faturamento",
            "RECIBO PAGAMENTO": r"recibo de pagamento"
        }


        if "certidão negativa de débitos municipais" in texto_pdf:
            if "certidão negativa de débitos trabalhistas" in texto_pdf:
                return "CND TRABALHISTA"
            return "CND MUNICIPAL"
        
        if "documento de arrecadação de receitas federais" in texto_pdf:
            if "pis sobre o faturamento" in texto_pdf:
                return "PIS"
            elif "irpj - lucro presumido" in texto_pdf:
                return "IRPJ"
            elif "cofins sobre o faturamento" in texto_pdf:
                return "COFINS"
            elif "csll - lucro presumido" in texto_pdf:
                return "CSLL"
            return "INSS"
        
        if "documento de arrecadação do simples nacional" in texto_pdf:
            if "das de parcmei" in texto_pdf:
                return "PARCELAMENTO MEI"
            elif "das de parcsn" in texto_pdf:
                return "PARCELAMENTO SIMPLES"

        for categoria, padrao in padroes.items():
            if re.search(rf'\b{padrao}\b', texto_pdf):
                return categoria

        return None

    # EXTRAI OS NOMES COM BASE EM PADRÕES DE CATEGORIAS
    def extrair_nome(self, texto_pdf, classificacao):
        padroes_nomes = {
            "CNPJ": r"NOME EMPRESARIAL\s*([A-Z\s&\.]+)",
            "CND MUNICIPAL": r"(?i)nome:\s*([A-Z\s]+)",
            "CND FEDERAL": r"(?i)nome:\s*([A-Z\s]+)",
            "CND ESTADUAL": r"(?i)nome:\s*([A-Z\s]+)",
            "CND TRABALHISTA": r"(?i)nome:\s*([A-Z\s]+)\s*\(MATRIZ E FILIAIS\)?",
            "COFINS": r"01 NOME / TELEFONE\s*([A-Z\s.]+)",
            "CSLL": r"01 NOME / TELEFONE\s*([A-Z\s.]+)",
            "DAS": r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\s+([A-Z\s&\.]+)",
            "FGTS": r"Nome\/Razão Social do Empregador\s*([A-Z\s]+)",
            "INSS": r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\s+([A-Z\s&\.]+)",
            "IRPJ": r"01 NOME / TELEFONE\s*([A-Z\s.]+)",
            "PARCELAMENTO MEI": r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\s+([A-Z\s]+)",
            "PARCELAMENTO SIMPLES": r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\s+([A-Z\s]+)",
            "PIS": r"01 NOME / TELEFONE\s*([A-Z\s.]+)",
            "RECIBO PAGAMENTO": r"^([A-Z\s&\.]+)\s*\(\d+\)\s*Recibo de Pagamento"
        }

        if classificacao in padroes_nomes:
            padrao = padroes_nomes[classificacao]
            resultado = re.search(padrao, texto_pdf)

            if resultado:
                nome = resultado.group(1).strip()
                nome_limpo = nome.split('\n')[0].strip()

                return nome_limpo

        return None