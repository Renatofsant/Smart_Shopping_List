from flask import Flask, render_template, jsonify, request
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')


def get_sheets_client():
    if not os.path.exists(creds_path):
        raise FileNotFoundError("Arquivo credentials.json não encontrado na raiz do projeto.")
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    return gspread.authorize(creds)


PLANILHA_NOME = "Lista Compras Remota"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/produtos', methods=['GET'])
def obter_produtos():
    try:
        client = get_sheets_client()
        sheet = client.open(PLANILHA_NOME).sheet1

        try:
            records = sheet.get_all_records()
        except Exception:
            records = []

        if not records:
            sheet.clear()
            headers = ["Setor", "Item", "Quantidade", "Valor_Medio", "Valor_Real_A", "Mercado_A", "Valor_Real_B",
                       "Mercado_B"]
            sheet.insert_row(headers, 1)

            itens_padrao = [
                ["Açougue & Peixaria", "Alcatra (kg)", 1, 42.00, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Coração de Frango (kg)", 1, 16.50, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Coxa de Frango (kg)", 1, 12.50, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Filé de Merluza (kg)", 1, 28.90, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Linguiça Toscana (kg)", 1, 19.90, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Patinho Moído (kg)", 1, 32.90, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Peito de Frango (kg)", 1, 18.00, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Pernil Suíno (kg)", 1, 16.90, 0.0, "", 0.0, ""],
                ["Açougue & Peixaria", "Posta de Tilápia (kg)", 1, 34.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Abacaxi (un)", 1, 7.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Alface Crespa (un)", 1, 3.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Alho (kg)", 1, 28.00, 0.0, "", 0.0, ""],
                ["Hortifruti", "Banana Prata (kg)", 1, 6.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Batata Inglesa (kg)", 1, 5.20, 0.0, "", 0.0, ""],
                ["Hortifruti", "Cebola (kg)", 1, 4.80, 0.0, "", 0.0, ""],
                ["Hortifruti", "Cenoura (kg)", 1, 5.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Limão Taiti (kg)", 1, 4.90, 0.0, "", 0.0, ""],
                ["Hortifruti", "Maçã Gala (kg)", 1, 9.80, 0.0, "", 0.0, ""],
                ["Hortifruti", "Ovos Brancos (dz)", 1, 10.50, 0.0, "", 0.0, ""],
                ["Hortifruti", "Tomate Italiano (kg)", 1, 7.90, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Iogurte Natural (un)", 1, 3.20, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Leite Integral (L)", 1, 4.50, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Manteiga com Sal (un)", 1, 9.90, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Mortadela Fatiada (kg)", 1, 18.90, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Mussarela Fatiada (kg)", 1, 45.00, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Presunto Cozido (kg)", 1, 32.00, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Queijo Minas (un)", 1, 22.50, 0.0, "", 0.0, ""],
                ["Laticínios & Frios", "Requeijão Cremoso (un)", 1, 7.80, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Água Sanitária (L)", 1, 4.50, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Amaciante de Roupa (L)", 1, 14.90, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Creme Dental (un)", 1, 3.80, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Desinfetante (L)", 1, 8.50, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Detergente Líquido (un)", 1, 2.30, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Esponja de Aço (un)", 1, 2.90, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Papel Higiênico (cx)", 1, 15.90, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Papel Toalha (un)", 1, 5.50, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Sabonete (un)", 1, 2.50, 0.0, "", 0.0, ""],
                ["Limpeza & Higiene", "Shampoo (un)", 1, 14.00, 0.0, "", 0.0, ""],
                ["Padaria & Biscoitos", "Biscoito Cream Cracker", 1, 4.20, 0.0, "", 0.0, ""],
                ["Padaria & Biscoitos", "Biscoito Recheado", 1, 3.20, 0.0, "", 0.0, ""],
                ["Padaria & Biscoitos", "Pão de Forma", 1, 7.50, 0.0, "", 0.0, ""],
                ["Padaria & Biscoitos", "Pão Francês (kg)", 1, 14.00, 0.0, "", 0.0, ""],
                ["Padaria & Biscoitos", "Torrada Integral", 1, 6.20, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Açúcar Refinado (1kg)", 1, 4.30, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Arroz Agulhinha (5kg)", 1, 26.90, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Azeite de Oliva (un)", 1, 38.00, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Café Torrado (un)", 1, 16.90, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Creme de Leite (un)", 1, 3.50, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Extrato de Tomate (un)", 1, 3.80, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Feijão Preto (1kg)", 1, 8.50, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Leite condensado (un)", 1, 5.90, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Macarrão Espaguete", 1, 4.50, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Maionese (un)", 1, 6.80, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Óleo de Soja (un)", 1, 6.20, 0.0, "", 0.0, ""],
                ["Mercearia & Despensa", "Sal Refinado (1kg)", 1, 2.90, 0.0, "", 0.0, ""]
            ]
            sheet.insert_rows(itens_padrao, 2)
            records = sheet.get_all_records()

        return jsonify({"status": "success", "data": records})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/atualizar_celula', methods=['POST'])
def atualizar_celula():
    try:
        dados = request.json
        item_nome = dados['item']
        campo = dados['campo']
        valor = dados['valor']

        client = get_sheets_client()
        sheet = client.open(PLANILHA_NOME).sheet1

        cell = sheet.find(item_nome)
        if not cell:
            return jsonify({"status": "error", "message": "Item não encontrado"}), 404

        linha = cell.row
        colunas = {
            "Quantidade": 3, "Valor_Real_A": 5, "Mercado_A": 6, "Valor_Real_B": 7, "Mercado_B": 8
        }

        coluna = colunas.get(campo)
        if coluna:
            sheet.update_cell(linha, coluna, valor)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/adicionar_item', methods=['POST'])
def adicionar_item():
    try:
        item = request.json
        client = get_sheets_client()
        sheet = client.open(PLANILHA_NOME).sheet1
        sheet.append_row([item['Setor'], item['Item'], 1, 0.0, 0.0, item['Mercado_A'], 0.0, ""])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)