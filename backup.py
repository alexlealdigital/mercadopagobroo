from flask import Blueprint, request, jsonify, send_file
from src.services.backup_service import BackupService
import os

backup_bp = Blueprint('backup', __name__)

# Instanciar serviço de backup
backup_service = BackupService()

@backup_bp.route('/backup/export', methods=['POST'])
def export_backup():
    """
    Exporta cobranças para JSON
    
    Body JSON (opcional):
    {
        "type": "full" | "latest"
    }
    """
    try:
        data = request.get_json() or {}
        backup_type = data.get('type', 'full')
        
        if backup_type == 'latest':
            filepath = backup_service.export_latest_cobrancas()
        else:
            filepath = backup_service.export_cobrancas_to_json()
        
        return jsonify({
            'success': True,
            'message': 'Backup exportado com sucesso',
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'backup_type': backup_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@backup_bp.route('/backup/commit', methods=['POST'])
def commit_backup():
    """
    Executa backup e commit no Git
    
    Body JSON (opcional):
    {
        "type": "full" | "latest",
        "message": "Mensagem personalizada do commit"
    }
    """
    try:
        data = request.get_json() or {}
        backup_type = data.get('type', 'full')
        
        result = backup_service.backup_and_commit(backup_type)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Backup criado e commitado com sucesso',
                'backup_file': result['backup_file'],
                'git_result': result['git_result'],
                'backup_type': result['backup_type']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@backup_bp.route('/backup/restore', methods=['POST'])
def restore_backup():
    """
    Restaura cobranças de um arquivo JSON
    
    Body JSON:
    {
        "filename": "nome_do_arquivo.json"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('filename'):
            return jsonify({
                'success': False,
                'error': 'Nome do arquivo é obrigatório'
            }), 400
        
        filename = data['filename']
        filepath = os.path.join(backup_service.backup_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Arquivo de backup não encontrado'
            }), 404
        
        result = backup_service.restore_from_json(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Backup restaurado com sucesso',
                'restored_count': result['restored_count'],
                'skipped_count': result['skipped_count'],
                'total_in_backup': result['total_in_backup']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@backup_bp.route('/backup/list', methods=['GET'])
def list_backups():
    """
    Lista todos os arquivos de backup disponíveis
    """
    try:
        backup_files = backup_service.list_backup_files()
        
        return jsonify({
            'success': True,
            'backup_files': backup_files,
            'total_files': len(backup_files)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@backup_bp.route('/backup/download/<filename>', methods=['GET'])
def download_backup(filename):
    """
    Faz download de um arquivo de backup específico
    """
    try:
        filepath = os.path.join(backup_service.backup_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Arquivo não encontrado'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@backup_bp.route('/backup/status', methods=['GET'])
def backup_status():
    """
    Retorna informações sobre o status do sistema de backup
    """
    try:
        # Verificar se é repositório Git
        is_git_repo = os.path.exists('.git')
        
        # Listar arquivos de backup
        backup_files = backup_service.list_backup_files()
        
        # Informações do diretório de backup
        backup_dir_exists = os.path.exists(backup_service.backup_dir)
        
        return jsonify({
            'success': True,
            'status': {
                'git_repository': is_git_repo,
                'backup_directory': backup_service.backup_dir,
                'backup_directory_exists': backup_dir_exists,
                'total_backup_files': len(backup_files),
                'latest_backup': backup_files[0] if backup_files else None
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
