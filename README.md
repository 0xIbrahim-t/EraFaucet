# EthereumFaucet
 A basic Ethereum Faucet on the Ropsten network.
 
## How it works
Insert your wallet address, click on the button and you'll magically receive 0.02 ETH on the Ropsten network. At the moment you can only make this request once a day per address.

## Installation
To run EthereumFaucet you need Python3 and a wallet with some ETH inside.
The first step is to install the dependencies:

```sh
pip3 install -r requirements.txt
```

Then you must set these four environment variables
```sh
export FLASK_SECRETKEY="Your secret key for flask"
export INFURA_ID="Your Infura project id"
export WALLET_PUBKEY="Your wallet public key (i.e. the address)"
export WALLET_PRIVKEY="Your wallet private key"
```

Now you can run your own version. 

## Running the faucet
At the moment it runs on port 8080 and accepts connections from every IP address.

To start the server you just to execute
```sh
python3 app.py
```
