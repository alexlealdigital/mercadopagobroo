import json
import os
import subprocess
from datetime import datetime
from src.models.cobranca import Cobranca, db

class BackupService:
    def __init__(self):
        self.backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backup_data')
        self.ensure_backup_directory()
    
    def ensure_backup_directory(self):
        """Garante que o diretório de backup existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def export_cobrancas_to_json(self):
        """
        Exporta todas as cobranças para um arquivo JSON
        
        Returns:
            str: Caminho do arquivo JSON criado
        """
        try:
            # Buscar todas as cobranças
            cobrancas = Cobranca.query.all()
            
            # Converter para dicionários
            cobrancas_data = []
            for cobranca in cobrancas:
                cobranca_dict = cobranca.to_dict()
                cobrancas_data.append(cobranca_dict)
            
            # Criar estrutura do backup
            backup_data = {
                'export_date': datetime.utcnow().isoformat(),
                'total_cobrancas': len(cobrancas_data),
                'cobrancas': cobrancas_data,
                'metadata': {
                    'version': '1.0',
                    'system': 'Sistema de Cobrança Mercado Pago',
                    'format': 'JSON'
                }
            }
            
            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'cobrancas_backup_{timestamp}.json'
            filepath = os.path.join(self.backup_dir, filename)
            
            # Salvar arquivo JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Erro ao exportar cobranças: {str(e)}")
    
    def export_latest_cobrancas(self):
        """
        Exporta apenas as cobranças mais recentes (últimas 24h)
        
        Returns:
            str: Caminho do arquivo JSON criado
        """
        try:
            from datetime import timedelta
            
            # Data limite (últimas 24 horas)
            data_limite = datetime.utcnow() - timedelta(hours=24)
            
            # Buscar cobranças recentes
            cobrancas = Cobranca.query.filter(
                Cobranca.data_atualizacao >= data_limite
            ).all()
            
            # Converter para dicionários
            cobrancas_data = []
            for cobranca in cobrancas:
                cobranca_dict = cobranca.to_dict()
                cobrancas_data.append(cobranca_dict)
            
            # Criar estrutura do backup
            backup_data = {
                'export_date': datetime.utcnow().isoformat(),
                'period': 'last_24_hours',
                'total_cobrancas': len(cobrancas_data),
                'cobrancas': cobrancas_data,
                'metadata': {
                    'version': '1.0',
                    'system': 'Sistema de Cobrança Mercado Pago',
                    'format': 'JSON',
                    'filter': 'últimas 24 horas'
                }
            }
            
            # Nome do arquivo
            filename = 'cobrancas_latest.json'
            filepath = os.path.join(self.backup_dir, filename)
            
            # Salvar arquivo JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Erro ao exportar cobranças recentes: {str(e)}")
    
    def commit_to_git(self, filepath, commit_message=None):
        """
        Faz commit do arquivo de backup no Git
        
        Args:
            filepath (str): Caminho do arquivo para commit
            commit_message (str): Mensagem do commit (opcional)
        
        Returns:
            dict: Resultado da operação
        """
        try:
            # Verificar se estamos em um repositório Git
            if not os.path.exists('.git'):
                return {
                    'success': False,
                    'error': 'Não é um repositório Git. Execute git init primeiro.'
                }
            
            # Adicionar arquivo ao Git
            subprocess.run(['git', 'add', filepath], check=True, cwd=os.path.dirname(filepath))
            
            # Mensagem padrão se não fornecida
            if not commit_message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                commit_message = f"Backup automático de cobranças - {timestamp}"
            
            # Fazer commit
            subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=os.path.dirname(filepath))
            
            return {
                'success': True,
                'message': 'Backup commitado com sucesso',
                'commit_message': commit_message
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f'Erro no Git: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro inesperado: {str(e)}'
            }
    
    def backup_and_commit(self, backup_type='full'):
        """
        Executa backup completo e commit no Git
        
        Args:
            backup_type (str): 'full' para backup completo, 'latest' para últimas 24h
        
        Returns:
            dict: Resultado da operação
        """
        try:
            # Escolher tipo de backup
            if backup_type == 'latest':
                filepath = self.export_latest_cobrancas()
                commit_msg = f"Backup incremental - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                filepath = self.export_cobrancas_to_json()
                commit_msg = f"Backup completo - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Fazer commit
            git_result = self.commit_to_git(filepath, commit_msg)
            
            return {
                'success': True,
                'backup_file': filepath,
                'git_result': git_result,
                'backup_type': backup_type
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def restore_from_json(self, filepath):
        """
        Restaura cobranças de um arquivo JSON de backup
        
        Args:
            filepath (str): Caminho do arquivo JSON
        
        Returns:
            dict: Resultado da operação
        """
        try:
            # Ler arquivo JSON
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Validar estrutura
            if 'cobrancas' not in backup_data:
                return {
                    'success': False,
                    'error': 'Arquivo de backup inválido: estrutura não reconhecida'
                }
            
            cobrancas_data = backup_data['cobrancas']
            restored_count = 0
            skipped_count = 0
            
            # Restaurar cada cobrança
            for cobranca_dict in cobrancas_data:
                # Verificar se já existe (por external_reference)
                existing = Cobranca.query.filter_by(
                    external_reference=cobranca_dict['external_reference']
                ).first()
                
                if existing:
                    skipped_count += 1
                    continue
                
                # Criar nova cobrança
                cobranca = Cobranca(
                    external_reference=cobranca_dict['external_reference'],
                    mercadopago_id=cobranca_dict.get('mercadopago_id'),
                    cliente_nome=cobranca_dict['cliente_nome'],
                    cliente_email=cobranca_dict['cliente_email'],
                    cliente_telefone=cobranca_dict.get('cliente_telefone'),
                    cliente_documento=cobranca_dict.get('cliente_documento'),
                    titulo=cobranca_dict['titulo'],
                    descricao=cobranca_dict.get('descricao'),
                    valor=cobranca_dict['valor'],
                    status=cobranca_dict['status'],
                    payment_url=cobranca_dict.get('payment_url')
                )
                
                # Definir dados do Mercado Pago se existirem
                if cobranca_dict.get('dados_mercadopago'):
                    cobranca.set_dados_mercadopago(cobranca_dict['dados_mercadopago'])
                
                db.session.add(cobranca)
                restored_count += 1
            
            # Salvar no banco
            db.session.commit()
            
            return {
                'success': True,
                'restored_count': restored_count,
                'skipped_count': skipped_count,
                'total_in_backup': len(cobrancas_data)
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_backup_files(self):
        """
        Lista todos os arquivos de backup disponíveis
        
        Returns:
            list: Lista de arquivos de backup
        """
        try:
            backup_files = []
            
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    
                    backup_files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
            
            # Ordenar por data de modificação (mais recente primeiro)
            backup_files.sort(key=lambda x: x['modified'], reverse=True)
            
            return backup_files
            
        except Exception as e:
            return []
