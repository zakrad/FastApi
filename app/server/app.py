from fastapi import FastAPI
import pytz
import math
import decimal
from web3 import Web3
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_balance,
    retrieve_balances,
)
from server.models.balance import (
    ResponseModel,
)

cg = CoinGeckoAPI()
app = FastAPI(docs_url="/", redoc_url=None)
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
crvId = 'curve-dao-token'

price = cg.get_price(ids=crvId, vs_currencies='usd')

crvToken = w3.eth.contract(address="0xD533a949740bb3306d119CC777fa900bA034cd52", abi=[{"name": "balanceOf", "outputs": [
    {"type": "uint256", "name": ""}], "inputs": [{"type": "address", "name": "arg0"}], "stateMutability": "view", "type": "function", "gas": 1905}])


@app.get("/{address}", response_description="Wallet data added into the database", tags=["Wallet"])
async def add_balance_data(address):
    checksumed = Web3.to_checksum_address(address)
    balance = Web3.from_wei(
        crvToken.functions.balanceOf(checksumed).call(), 'ether')
    value = math.ceil(decimal.Decimal(
        price[crvId]['usd']) * balance * 100) / 100

    timestamp = w3.eth.get_block('latest').timestamp
    date = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    data = {
        'address': checksumed,
        'balance': balance,
        'value': value,
        'timestamp': timestamp,
        'date': date
    }
    balance = jsonable_encoder(data)
    await add_balance(balance)
    return {"token balance": data["balance"], "token usd balance": data["value"]}


@app.get("/history/{address}", tags=["Wallet"])
async def read_balance_history(address):
    checksumed = Web3.to_checksum_address(address)
    balances = await retrieve_balances(checksumed)
    if balances:
        return ResponseModel(balances, "Users balances retrieved successfully")
    return ResponseModel(balances, "Empty list returned")
