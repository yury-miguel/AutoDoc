## 💡 AutoDoc 
Sistema de controle de ficheiros, com leitura automática de PDFs e extração de 14 categorias de documentos sendo, CND ESTADUAL, FEDERAL, MUNICIPAL e TRABALHISTA, CNPJ, COFINS, CSLL, DAS, FGTS, INSS, IRPJ, PARCELAMENTO MEI, PARCELAMENTO SIMPLES, PIS e RECIBO PAGAMENTO, também realiza extração de nomes empresarias e razões sociais dos documentos.

!! Recomendo não mover o sistema da pasta na qual foi enviado, e não adicionar ele na área de trabalho.Além do mais para que os PDFs sejam lidos e movidos o sistema deve estar em funcionamento, é necessário permitir a autorização de uso das redes privadas e publicas quando solicitado.

## Sistema AutoDoc
![Captura de Tela (39)](https://github.com/user-attachments/assets/c313b2f2-1f36-44c5-831c-d6e9743844c1)

![Captura de Tela (40)](https://github.com/user-attachments/assets/de8d4e5f-af0c-43ff-81eb-6d9825e6a8e4)

![Captura de Tela (41)](https://github.com/user-attachments/assets/c3b7767c-0928-4eb0-81d3-a2d30cac1731)

![Captura de Tela (42)](https://github.com/user-attachments/assets/d2d2f25c-38f8-4bf2-b822-5dc7e3d967a2)


## 🚀 Recursos

- **Documentos:** Visualize os status e as extrações e busque por documentos baixados.

- **Email Manual:** Permite o envio de emails usando configuração APP do google.

- **Configurações:** Cadastre clientes e seus emails em um arquivo XLSX, e adicione mensagens, email, assuntos padrões automáticos, também possui a opção de cofigurar os caminhos de leitura e movimentação dos documentos.

- **Logs:** Registra operações e possíveis problemas ou erros do sistema.


## 📋 Funcionalidades

### Documentos

Quando um documento com formato .PDF é baixado e ele vai diretamente para pasta downloads da máquina,
o sistema pega automaticamente esse documento verifica o nome do arquivo, formato, conteúdo do doc e
realiza as extrações de nome e categoria, após isso é registrado no arquivo status_pdf.txt os dados.
Se for encontrado nome e categoria ele move o documento para a pasta correspondente a empresa, 
se a pasta não existir é criada automaticamente também. Se não for encontrado ele deixa o arquivo na pasta 
downloads e registra o status. Além do mais quando é encontrado nome, categoria e é movido para a pasta o 
sistema envia o email automaticamente se o cliente tiver cadastrado e nas configurações tiver definido os campos.


### Email Manual

Usa o email definido no campo das configurações e a senha, para enviar um email como o usuário desejar, 
permite a anexação de arquivos pdfs e sua pré visualização, e retorna para o usuário se o email foi ou não enviado.


### Configurações

- Campo Documentos: é o caminho onde estão as subpastas das empresas, onde os arquivos PDFs devem ser movidos.

- Campo Downloads: é o caminho onde fica a pasta downloads da máquina, onde os documentos baixados vão automaticamentes.

- Campo Ano: campo que permite configurar o ano do documento para salvar na pasta correspondente.

- Campo Email Padrão e Senha Email: são os campos que define o email usado como remetente e a senha configurada.
                                    para configurar é necessário ir no Minha Conta Google -> Ativar Verificação Duas Etapas
                                    -> Pesquisar Senhas de app (ou aplicativos) -> Criar e anotar a senha que o google exibir.

- Campo Assunto Parão: campo que define o assunto padrão ao fazer o envio automático dos emails aos clientes.

- Campo Mensagem Padrão: campo que define a mensagem de corpo ao fazer o envio automático dos emails aos clientes.

- Campo Nome Empresa e Email Empresa: campos que cadastram dados dos clientes para envio de emails automáticos.


### Logs

Visualização das operações durante o funcionamento do sistema, permite ver erros ou falhas que podem ou não acontecer
no sistema. O sistema foi muito bem feito, é apenas para facilitar a identificação de qualquer problema.


## 📦 Atenção:

- **Email Automático:** O email automático só será enviado se o cliente e o seu email estiver cadastrado no arquivo .xlsx,
para isso precisa ir nas configurações e fazer o cadastro.

- **Documentos:** Os nomes das pastas devem estar exatamentes iguais aos nomes que vem nos documentos, se não tiverem, será 
criadas novas pastas. Já o nome das subpastas das categorias de documentos devem ser iguais aos disponibilizados para testes e os que foram citados acima.

- **Caso Aconteça:** De algum documento estiver com status "Não verificado" é devido a um problema ao tentar extraír o nome da empresa ou a categoria do documento, por favor fazer uma cópia ou guardar esses documentos. Quando acontecer o documento permanecerá na pasta de Downloads.


## 🛠️ Tecnologias
 - Python
 - Flask
 - Bootstrap


## 📧 Contato

- **Email:** yurymiguelc1@gmail.com
- **Linkedin:** https://www.linkedin.com/in/yury-miguel-827478315/
