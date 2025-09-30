import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
    
    def enviar_email(self, destinatario, assunto, corpo_html, corpo_texto=None):
        """
        Envia um email
        
        Args:
            destinatario (str): Email do destinatário
            assunto (str): Assunto do email
            corpo_html (str): Corpo do email em HTML
            corpo_texto (str): Corpo do email em texto simples (opcional)
        
        Returns:
            dict: Resultado do envio
        """
        try:
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Adicionar corpo em texto simples se fornecido
            if corpo_texto:
                part1 = MIMEText(corpo_texto, 'plain', 'utf-8')
                msg.attach(part1)
            
            # Adicionar corpo em HTML
            part2 = MIMEText(corpo_html, 'html', 'utf-8')
            msg.attach(part2)
            
            # Conectar ao servidor SMTP e enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "message": "Email enviado com sucesso"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def gerar_email_cobranca(self, dados_cobranca, payment_url):
        """
        Gera o HTML do email de cobrança
        
        Args:
            dados_cobranca (dict): Dados da cobrança
            payment_url (str): URL de pagamento
        
        Returns:
            tuple: (assunto, corpo_html, corpo_texto)
        """
        assunto = f"Cobrança: {dados_cobranca['titulo']}"
        
        corpo_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nova Cobrança</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #009ee3;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 8px 8px;
                }}
                .cobranca-info {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #009ee3;
                }}
                .valor {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #009ee3;
                    text-align: center;
                    margin: 20px 0;
                }}
                .botao-pagar {{
                    display: inline-block;
                    background-color: #009ee3;
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    margin: 20px 0;
                }}
                .botao-pagar:hover {{
                    background-color: #007bb3;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Nova Cobrança</h1>
            </div>
            
            <div class="content">
                <p>Olá <strong>{dados_cobranca['cliente_nome']}</strong>,</p>
                
                <p>Você recebeu uma nova cobrança. Veja os detalhes abaixo:</p>
                
                <div class="cobranca-info">
                    <h3>{dados_cobranca['titulo']}</h3>
                    {f'<p><strong>Descrição:</strong> {dados_cobranca["descricao"]}</p>' if dados_cobranca.get('descricao') else ''}
                    
                    <div class="valor">
                        R$ {dados_cobranca['valor']:.2f}
                    </div>
                    
                    <p><strong>Referência:</strong> {dados_cobranca['external_reference']}</p>
                </div>
                
                <div style="text-align: center;">
                    <a href="{payment_url}" class="botao-pagar">PAGAR AGORA</a>
                </div>
                
                <p>Ou copie e cole o link abaixo no seu navegador:</p>
                <p style="word-break: break-all; background-color: #f0f0f0; padding: 10px; border-radius: 4px;">
                    {payment_url}
                </p>
                
                <p><strong>Importante:</strong> Este link de pagamento é seguro e processado pelo Mercado Pago.</p>
            </div>
            
            <div class="footer">
                <p>Este é um email automático, não responda a esta mensagem.</p>
                <p>Em caso de dúvidas, entre em contato conosco.</p>
            </div>
        </body>
        </html>
        """
        
        corpo_texto = f"""
        Nova Cobrança
        
        Olá {dados_cobranca['cliente_nome']},
        
        Você recebeu uma nova cobrança:
        
        Título: {dados_cobranca['titulo']}
        {f"Descrição: {dados_cobranca['descricao']}" if dados_cobranca.get('descricao') else ''}
        Valor: R$ {dados_cobranca['valor']:.2f}
        Referência: {dados_cobranca['external_reference']}
        
        Para pagar, acesse o link: {payment_url}
        
        Este é um email automático, não responda a esta mensagem.
        """
        
        return assunto, corpo_html, corpo_texto
    
    def gerar_email_confirmacao_pagamento(self, dados_cobranca, dados_pagamento):
        """
        Gera o HTML do email de confirmação de pagamento
        
        Args:
            dados_cobranca (dict): Dados da cobrança
            dados_pagamento (dict): Dados do pagamento do Mercado Pago
        
        Returns:
            tuple: (assunto, corpo_html, corpo_texto)
        """
        assunto = f"Pagamento Confirmado: {dados_cobranca['titulo']}"
        
        corpo_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagamento Confirmado</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #00a650;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 8px 8px;
                }}
                .pagamento-info {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #00a650;
                }}
                .valor {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #00a650;
                    text-align: center;
                    margin: 20px 0;
                }}
                .status {{
                    background-color: #00a650;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 20px;
                    display: inline-block;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✅ Pagamento Confirmado</h1>
            </div>
            
            <div class="content">
                <p>Olá <strong>{dados_cobranca['cliente_nome']}</strong>,</p>
                
                <p>Seu pagamento foi processado com sucesso!</p>
                
                <div class="pagamento-info">
                    <h3>{dados_cobranca['titulo']}</h3>
                    
                    <div class="valor">
                        R$ {dados_cobranca['valor']:.2f}
                    </div>
                    
                    <p><strong>Status:</strong> <span class="status">APROVADO</span></p>
                    <p><strong>Referência:</strong> {dados_cobranca['external_reference']}</p>
                    <p><strong>ID do Pagamento:</strong> {dados_pagamento.get('id', 'N/A')}</p>
                    <p><strong>Data do Pagamento:</strong> {dados_pagamento.get('date_approved', 'N/A')}</p>
                </div>
                
                <p>Obrigado por utilizar nossos serviços!</p>
            </div>
            
            <div class="footer">
                <p>Este é um email automático, não responda a esta mensagem.</p>
                <p>Em caso de dúvidas, entre em contato conosco.</p>
            </div>
        </body>
        </html>
        """
        
        corpo_texto = f"""
        Pagamento Confirmado
        
        Olá {dados_cobranca['cliente_nome']},
        
        Seu pagamento foi processado com sucesso!
        
        Título: {dados_cobranca['titulo']}
        Valor: R$ {dados_cobranca['valor']:.2f}
        Status: APROVADO
        Referência: {dados_cobranca['external_reference']}
        ID do Pagamento: {dados_pagamento.get('id', 'N/A')}
        Data do Pagamento: {dados_pagamento.get('date_approved', 'N/A')}
        
        Obrigado por utilizar nossos serviços!
        
        Este é um email automático, não responda a esta mensagem.
        """
        
        return assunto, corpo_html, corpo_texto
