from flask import Flask, render_template, session, flash, redirect, url_for
from tronpy import Tron
from tronpy.keys import PrivateKey
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Подключаемся к TRON Testnet (Nile)
client = Tron(network="nile")

# Функция для создания нового кошелька
def create_wallet():
    private_key = PrivateKey.random()
    address = private_key.public_key.to_base58check_address()
    return private_key.hex(), address

# Функция для проверки наличия транзакций на кошельке
def has_transactions(address):
    transactions = client.get_account_transaction_history(address)
    return len(transactions) > 0

# Функция для сохранения данных кошелька в файл
def save_wallet_data(private_key, address):
    with open("wallets.txt", "a") as file:
        file.write(f"Address: {address}\n")
        file.write(f"Private Key: {private_key}\n\n")

# Маршрут для создания множества кошельков
@app.route('/generate_wallets/<int:count>')
def generate_wallets(count):
    for _ in range(count):
        private_key, address = create_wallet()
        if has_transactions(address):
            save_wallet_data(private_key, address)
            flash(f"Кошелек {address} с транзакциями сохранен.")
        else:
            flash(f"Кошелек {address} без транзакций.")
    return redirect(url_for('index'))

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
