import mercadopago
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class MercadoPagoService:
    def __init__(self):
        self.access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN', 'TEST-token-placeholder')
        self.sdk = mercadopago.SDK(self.access_token)
    
    def criar_pagamento(self, dados_cobranca):
        """
        Cria um pagamento no Mercado Pago
        
        Args:
            dados_cobranca (dict): Dados da cobrança contendo:
                - titulo: Título do produto/serviço
                - descricao: Descrição
                - valor: Valor em reais
                - cliente_nome: Nome do cliente
                - cliente_email: Email do cliente
                - cliente_documento: CPF/CNPJ do cliente
                - external_reference: Referência externa única
        
        Returns:
            dict: Resposta da API do Mercado Pago
        """
        
        # Preparar dados do pagamento
        payment_data = {
            "transaction_amount": float(dados_cobranca['valor']),
            "description": dados_cobranca['descricao'] or dados_cobranca['titulo'],
            "external_reference": dados_cobranca['external_reference'],
            "payer": {
                "email": dados_cobranca['cliente_email'],
                "first_name": dados_cobranca['cliente_nome'].split()[0] if dados_cobranca['cliente_nome'] else "",
                "last_name": " ".join(dados_cobranca['cliente_nome'].split()[1:]) if len(dados_cobranca['cliente_nome'].split()) > 1 else "",
            },
            "notification_url": os.getenv('WEBHOOK_URL'),
            "auto_return": "approved",
            "back_urls": {
                "success": f"{os.getenv('FRONTEND_URL')}/success",
                "failure": f"{os.getenv('FRONTEND_URL')}/failure",
                "pending": f"{os.getenv('FRONTEND_URL')}/pending"
            }
        }
        
        # Adicionar identificação se fornecida
        if dados_cobranca.get('cliente_documento'):
            payment_data["payer"]["identification"] = {
                "type": "CPF" if len(dados_cobranca['cliente_documento'].replace('.', '').replace('-', '')) == 11 else "CNPJ",
                "number": dados_cobranca['cliente_documento'].replace('.', '').replace('-', '').replace('/', '')
            }
        
        # Adicionar informações adicionais do item
        payment_data["additional_info"] = {
            "items": [
                {
                    "id": dados_cobranca['external_reference'],
                    "title": dados_cobranca['titulo'],
                    "description": dados_cobranca['descricao'] or dados_cobranca['titulo'],
                    "quantity": 1,
                    "unit_price": float(dados_cobranca['valor']),
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "first_name": dados_cobranca['cliente_nome'].split()[0] if dados_cobranca['cliente_nome'] else "",
                "last_name": " ".join(dados_cobranca['cliente_nome'].split()[1:]) if len(dados_cobranca['cliente_nome'].split()) > 1 else "",
            }
        }
        
        # Criar preferência de pagamento
        try:
            preference_data = {
                "items": [
                    {
                        "id": dados_cobranca['external_reference'],
                        "title": dados_cobranca['titulo'],
                        "description": dados_cobranca['descricao'] or dados_cobranca['titulo'],
                        "quantity": 1,
                        "currency_id": "BRL",
                        "unit_price": float(dados_cobranca['valor'])
                    }
                ],
                "payer": payment_data["payer"],
                "back_urls": payment_data["back_urls"],
                "auto_return": "approved",
                "notification_url": payment_data["notification_url"],
                "external_reference": dados_cobranca['external_reference'],
                "expires": True,
                "expiration_date_from": datetime.now().isoformat(),
                "expiration_date_to": (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            preference_response = self.sdk.preference().create(preference_data)
            
            if preference_response["status"] == 201:
                return {
                    "success": True,
                    "preference_id": preference_response["response"]["id"],
                    "init_point": preference_response["response"]["init_point"],
                    "sandbox_init_point": preference_response["response"]["sandbox_init_point"],
                    "response": preference_response["response"]
                }
            else:
                return {
                    "success": False,
                    "error": preference_response.get("response", {}).get("message", "Erro desconhecido"),
                    "response": preference_response
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
    
    def obter_pagamento(self, payment_id):
        """
        Obtém informações de um pagamento específico
        
        Args:
            payment_id (str): ID do pagamento no Mercado Pago
        
        Returns:
            dict: Dados do pagamento
        """
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] == 200:
                return {
                    "success": True,
                    "payment": payment_response["response"]
                }
            else:
                return {
                    "success": False,
                    "error": payment_response.get("response", {}).get("message", "Pagamento não encontrado")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def validar_webhook_signature(self, x_signature, x_request_id, data_id):
        """
        Valida a assinatura do webhook do Mercado Pago
        
        Args:
            x_signature (str): Cabeçalho x-signature
            x_request_id (str): Cabeçalho x-request-id
            data_id (str): ID dos dados da notificação
        
        Returns:
            bool: True se a assinatura for válida
        """
        import hmac
        import hashlib
        
        try:
            # Extrair ts e v1 do x-signature
            parts = x_signature.split(',')
            ts = None
            signature = None
            
            for part in parts:
                key_value = part.strip().split('=', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    if key == "ts":
                        ts = value
                    elif key == "v1":
                        signature = value
            
            if not ts or not signature:
                return False
            
            # Criar o manifest
            manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
            
            # Gerar HMAC
            secret = os.getenv('WEBHOOK_SECRET', '')
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                manifest.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Comparar assinaturas
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            print(f"Erro ao validar assinatura do webhook: {e}")
            return False
