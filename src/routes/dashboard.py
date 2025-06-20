from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import os
import json
from datetime import datetime
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel_data(file_path):
    """Processa os dados da planilha Excel e retorna dados estruturados"""
    try:
        df = pd.read_excel(file_path)
        
        # Renomear colunas para facilitar o processamento
        column_mapping = {
            'CANC. INICIAL/VALOR DOS ITENS': 'cancelamento_inicial',
            'REVERSÃO': 'reversao',
            'CANCELAMENTO FINAL': 'cancelamento_final',
            'TOTAL DO PEDIDO': 'total_pedido',
            'REGIONAIS': 'regional',
            'PRIMEIRA ANALISE': 'status',
            'DATA': 'data'
        }
        
        # Renomear colunas que existem
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df[old_name] = df[old_name].fillna(0)
                df = df.rename(columns={old_name: new_name})
        
        # Calcular totais gerais
        total_cancelamento_inicial = df['cancelamento_inicial'].sum()
        total_reversao = df['reversao'].sum()
        total_cancelamento_final = df['cancelamento_final'].sum()
        total_venda_ifood = df['total_pedido'].sum()
        
        # Calcular percentuais
        perc_antes_reversao = (total_cancelamento_inicial / total_venda_ifood * 100) if total_venda_ifood > 0 else 0
        perc_apos_reversao = (total_cancelamento_final / total_venda_ifood * 100) if total_venda_ifood > 0 else 0
        
        # Dados por regional
        dados_regionais = df.groupby('regional').agg({
            'cancelamento_inicial': 'sum',
            'reversao': 'sum',
            'cancelamento_final': 'sum',
            'total_pedido': 'sum'
        }).reset_index()
        
        # Calcular percentuais por regional
        dados_regionais['perc_antes_reversao'] = (dados_regionais['cancelamento_inicial'] / dados_regionais['total_pedido'] * 100).fillna(0)
        dados_regionais['perc_apos_reversao'] = (dados_regionais['cancelamento_final'] / dados_regionais['total_pedido'] * 100).fillna(0)
        
        # Dados por status
        dados_status = df.groupby('status').agg({
            'cancelamento_inicial': 'sum',
            'reversao': 'sum',
            'cancelamento_final': 'sum'
        }).reset_index()
        
        return {
            'resumo_geral': {
                'total_pedidos': len(df),
                'venda_total_ifood': total_venda_ifood,
                'cancelamento_inicial': total_cancelamento_inicial,
                'reversao': total_reversao,
                'cancelamento_final': total_cancelamento_final,
                'perc_antes_reversao': round(perc_antes_reversao, 2),
                'perc_apos_reversao': round(perc_apos_reversao, 2)
            },
            'dados_regionais': dados_regionais.to_dict('records'),
            'dados_status': dados_status.to_dict('records'),
            'dados_completos': df.to_dict('records')
        }
    except Exception as e:
        raise Exception(f"Erro ao processar planilha: {str(e)}")

@dashboard_bp.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload de planilha"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        try:
            # Processar dados
            dados = process_excel_data(file_path)
            
            # Salvar dados no banco de dados (opcional)
            # Aqui você pode implementar a lógica para salvar no SQLite
            
            # Salvar metadados do upload
            metadata = {
                'filename': filename,
                'upload_date': datetime.now().isoformat(),
                'file_path': file_path
            }
            
            # Salvar metadados em arquivo JSON
            metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)
            
            return jsonify({
                'message': 'Arquivo enviado e processado com sucesso',
                'data': dados,
                'metadata': metadata
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

@dashboard_bp.route('/data', methods=['GET'])
def get_data():
    """Endpoint para obter dados processados"""
    try:
        # Verificar se existe upload recente
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        if not os.path.exists(metadata_path):
            return jsonify({'error': 'Nenhum dado disponível. Faça upload de uma planilha primeiro.'}), 404
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo de dados não encontrado'}), 404
        
        # Processar dados novamente (ou implementar cache)
        dados = process_excel_data(file_path)
        
        return jsonify({
            'data': dados,
            'metadata': metadata
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/data/filter', methods=['POST'])
def filter_data():
    """Endpoint para filtrar dados por data, semana ou mês"""
    try:
        filters = request.json
        
        # Obter dados atuais
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        if not os.path.exists(metadata_path):
            return jsonify({'error': 'Nenhum dado disponível'}), 404
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        df = pd.read_excel(file_path)
        
        # Aplicar filtros
        if 'data_inicio' in filters and 'data_fim' in filters:
            df['DATA'] = pd.to_datetime(df['DATA'])
            data_inicio = pd.to_datetime(filters['data_inicio'])
            data_fim = pd.to_datetime(filters['data_fim'])
            df = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
        
        # Processar dados filtrados
        # Salvar temporariamente e processar
        temp_path = os.path.join(UPLOAD_FOLDER, 'temp_filtered.xlsx')
        df.to_excel(temp_path, index=False)
        
        dados_filtrados = process_excel_data(temp_path)
        
        # Limpar arquivo temporário
        os.remove(temp_path)
        
        return jsonify({'data': dados_filtrados})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/export', methods=['POST'])
def export_data():
    """Endpoint para exportar dados filtrados"""
    try:
        filters = request.json
        
        # Obter e filtrar dados (similar ao endpoint de filtro)
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        if not os.path.exists(metadata_path):
            return jsonify({'error': 'Nenhum dado disponível'}), 404
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        df = pd.read_excel(file_path)
        
        # Aplicar filtros se fornecidos
        if filters and 'data_inicio' in filters and 'data_fim' in filters:
            df['DATA'] = pd.to_datetime(df['DATA'])
            data_inicio = pd.to_datetime(filters['data_inicio'])
            data_fim = pd.to_datetime(filters['data_fim'])
            df = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
        
        # Criar arquivo de exportação
        export_filename = f"dados_exportados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        export_path = os.path.join(UPLOAD_FOLDER, export_filename)
        df.to_excel(export_path, index=False)
        
        return jsonify({
            'message': 'Dados exportados com sucesso',
            'download_url': f'/api/dashboard/download/{export_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/download/<filename>')
def download_file(filename):
    """Endpoint para download de arquivos"""
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@dashboard_bp.route('/manual/add', methods=['POST'])
def add_manual_data():
    """Endpoint para inserção manual de dados"""
    try:
        data = request.json
        
        # Validar dados obrigatórios
        required_fields = ['regional', 'cancelamento_inicial', 'reversao', 'cancelamento_final', 'total_pedido']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Carregar dados atuais
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            file_path = metadata['file_path']
            df = pd.read_excel(file_path)
        else:
            # Criar novo DataFrame se não existir dados
            df = pd.DataFrame()
        
        # Adicionar nova linha
        new_row = {
            'N° PEDIDO': data.get('numero_pedido', ''),
            'DATA': data.get('data', datetime.now()),
            'RESTAURANTE': data.get('restaurante', ''),
            'ORIGEM DO CANCELAMENTO': data.get('origem_cancelamento', ''),
            'MOTIVO DO CANCELAMENTO': data.get('motivo_cancelamento', ''),
            'TOTAL DO PEDIDO': data['total_pedido'],
            'CANC. INICIAL/VALOR DOS ITENS': data['cancelamento_inicial'],
            'REVERSÃO': data['reversao'],
            'CANCELAMENTO FINAL': data['cancelamento_final'],
            'PRIMEIRA ANALISE': data.get('status', ''),
            'REGIONAIS': data['regional'],
            'CANAL DE VENDA': data.get('canal_venda', 'iFood')
        }
        
        # Adicionar ao DataFrame
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Salvar arquivo atualizado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_manual_update.xlsx"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(file_path, index=False)
        
        # Atualizar metadados
        metadata = {
            'filename': filename,
            'upload_date': datetime.now().isoformat(),
            'file_path': file_path,
            'type': 'manual_update'
        }
        
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Processar dados atualizados
        dados = process_excel_data(file_path)
        
        return jsonify({
            'message': 'Dados adicionados com sucesso',
            'data': dados
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/manual/update/<int:row_id>', methods=['PUT'])
def update_manual_data(row_id):
    """Endpoint para atualizar dados específicos"""
    try:
        data = request.json
        
        # Carregar dados atuais
        metadata_path = os.path.join(UPLOAD_FOLDER, 'latest_upload.json')
        if not os.path.exists(metadata_path):
            return jsonify({'error': 'Nenhum dado disponível'}), 404
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        file_path = metadata['file_path']
        df = pd.read_excel(file_path)
        
        # Verificar se o índice existe
        if row_id >= len(df):
            return jsonify({'error': 'Registro não encontrado'}), 404
        
        # Atualizar campos fornecidos
        for key, value in data.items():
            if key in df.columns:
                df.loc[row_id, key] = value
        
        # Salvar arquivo atualizado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_manual_update.xlsx"
        new_file_path = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(new_file_path, index=False)
        
        # Atualizar metadados
        metadata = {
            'filename': filename,
            'upload_date': datetime.now().isoformat(),
            'file_path': new_file_path,
            'type': 'manual_update'
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        # Processar dados atualizados
        dados = process_excel_data(new_file_path)
        
        return jsonify({
            'message': 'Dados atualizados com sucesso',
            'data': dados
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

