from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Cobranca(db.Model):
    __tablename__ = 'cobrancas'
    
    id = db.Column(db.Integer, primary_key=True)
    mercadopago_id = db.Column(db.String(100), unique=True, nullable=True)
    external_reference = db.Column(db.String(100), unique=True, nullable=False)
    
    # Dados do cliente
    cliente_nome = db.Column(db.String(200), nullable=False)
    cliente_email = db.Column(db.String(200), nullable=False)
    cliente_telefone = db.Column(db.String(50), nullable=True)
    cliente_documento = db.Column(db.String(50), nullable=True)
    
    # Dados da cobrança
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    valor = db.Column(db.Float, nullable=False)
    
    # Status e datas
    status = db.Column(db.String(50), default='pending', nullable=False)
    # Status possíveis: pending, approved, rejected, cancelled, in_process
    
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    data_vencimento = db.Column(db.DateTime, nullable=True)
    data_pagamento = db.Column(db.DateTime, nullable=True)
    
    # URLs e links
    payment_url = db.Column(db.Text, nullable=True)
    
    # Dados adicionais em JSON
    dados_mercadopago = db.Column(db.Text, nullable=True)  # JSON string
    
    def __init__(self, **kwargs):
        super(Cobranca, self).__init__(**kwargs)
    
    def to_dict(self):
        return {
            'id': self.id,
            'mercadopago_id': self.mercadopago_id,
            'external_reference': self.external_reference,
            'cliente_nome': self.cliente_nome,
            'cliente_email': self.cliente_email,
            'cliente_telefone': self.cliente_telefone,
            'cliente_documento': self.cliente_documento,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'valor': self.valor,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'payment_url': self.payment_url,
            'dados_mercadopago': json.loads(self.dados_mercadopago) if self.dados_mercadopago else None
        }
    
    def set_dados_mercadopago(self, dados):
        """Converte um dicionário para JSON string"""
        self.dados_mercadopago = json.dumps(dados) if dados else None
    
    def get_dados_mercadopago(self):
        """Retorna os dados do Mercado Pago como dicionário"""
        return json.loads(self.dados_mercadopago) if self.dados_mercadopago else None
