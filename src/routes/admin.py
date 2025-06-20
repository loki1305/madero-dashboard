from flask import Blueprint, request, jsonify, session
from functools import wraps
import hashlib

admin_bp = Blueprint('admin', __name__)

# Senha simples para área administrativa (em produção, usar hash mais seguro)
ADMIN_PASSWORD = "madero2025"
ADMIN_PASSWORD_HASH = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()

def require_admin(f):
    """Decorator para proteger rotas administrativas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'Acesso negado. Login administrativo necessário.'}), 401
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Endpoint para login administrativo"""
    try:
        data = request.json
        password = data.get('password', '')
        
        # Verificar senha
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash == ADMIN_PASSWORD_HASH:
            session['admin_logged_in'] = True
            return jsonify({'message': 'Login realizado com sucesso', 'success': True})
        else:
            return jsonify({'error': 'Senha incorreta', 'success': False}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/logout', methods=['POST'])
def admin_logout():
    """Endpoint para logout administrativo"""
    session.pop('admin_logged_in', None)
    return jsonify({'message': 'Logout realizado com sucesso'})

@admin_bp.route('/status', methods=['GET'])
def admin_status():
    """Verificar status do login administrativo"""
    return jsonify({
        'logged_in': session.get('admin_logged_in', False)
    })

@admin_bp.route('/protected-upload', methods=['POST'])
@require_admin
def protected_upload():
    """Upload protegido por senha"""
    # Redirecionar para o endpoint normal de upload
    from src.routes.dashboard import upload_file
    return upload_file()

@admin_bp.route('/protected-manual', methods=['POST'])
@require_admin
def protected_manual_add():
    """Inserção manual protegida por senha"""
    # Redirecionar para o endpoint normal de inserção manual
    from src.routes.dashboard import add_manual_data
    return add_manual_data()

@admin_bp.route('/upload-history', methods=['GET'])
@require_admin
def upload_history():
    """Histórico de uploads (protegido)"""
    try:
        import os
        import json
        from datetime import datetime
        
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        history = []
        
        # Listar todos os arquivos Excel na pasta de uploads
        for filename in os.listdir(uploads_dir):
            if filename.endswith(('.xlsx', '.xls')):
                file_path = os.path.join(uploads_dir, filename)
                stat = os.stat(file_path)
                
                history.append({
                    'filename': filename,
                    'upload_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'size': stat.st_size,
                    'file_path': file_path
                })
        
        # Ordenar por data de modificação (mais recente primeiro)
        history.sort(key=lambda x: x['upload_date'], reverse=True)
        
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/change-password', methods=['POST'])
@require_admin
def change_password():
    """Alterar senha administrativa"""
    try:
        global ADMIN_PASSWORD_HASH
        
        data = request.json
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Verificar senha atual
        current_hash = hashlib.sha256(current_password.encode()).hexdigest()
        if current_hash != ADMIN_PASSWORD_HASH:
            return jsonify({'error': 'Senha atual incorreta'}), 401
        
        # Validar nova senha
        if len(new_password) < 6:
            return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400
        
        # Atualizar senha (em produção, salvar em arquivo de configuração ou banco)
        ADMIN_PASSWORD_HASH = hashlib.sha256(new_password.encode()).hexdigest()
        
        return jsonify({'message': 'Senha alterada com sucesso'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

