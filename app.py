# Imports
from flask import Flask, render_template, request, flash, redirect, url_for, Markup
import json
import time
import os
from web3 import Web3

# Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRETKEY")

# Web3 
w3 = Web3(Web3.HTTPProvider('https://testnet.erachain.io'))
walletPK = os.getenv("WALLET_PUBKEY")
walletSK = os.getenv("WALLET_PRIVKEY")

# Address that already requested the ethers
session = {}

###############################################################################

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    address = None
    if "address" in request.form:
        address = request.form.get("address")
        if address == "":
            flash('Please enter an address!')
            return redirect(url_for("index"))
    else:
        flash('Please enter an address!')
        return redirect(url_for("index"))
    
    timestamp = int(time.time())
    
    if address not in session or (timestamp - session[address]) >= 60 * 60 * 24:
        txn = sendEther(address, 1)

        if txn != None:
            addTxnToSession(address, timestamp)
            flash(Markup('You will soon receive your ERA.\nA this link you can find the transaction <a href="https://testnet.erascan.io/tx/' + str(txn)+ '">here</a>.'))
        else:
            flash("There was an error sending the ERA.")
    else:
        flash('You have already requested your ERA.')
    return redirect(url_for("index"))

###############################################################################

def setup():
    global session
    with open("session/transactions.json", "r") as txnsFile:
        session = json.load(txnsFile)


def addTxnToSession(address: str, timestamp: int):
    session[address] = timestamp

    with open("session/transactions.json", "w") as txnsFile:
        json.dump(session, txnsFile, indent=4, sort_keys=True)

def sendEther(address: str, amount: float) :
    txn = None
    try:
        signed_txn = w3.eth.account.sign_transaction(dict(
                nonce=w3.eth.getTransactionCount(walletPK),
                gasPrice = w3.eth.gas_price, 
                gas = 21000,
                to=address,
                value=w3.toWei(amount,'ether')
            ),
            walletSK
        )

        txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    except Exception as e:
        print("Unable to send the transaction. " + str(e))

    return txn

###############################################################################

if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=8080)
