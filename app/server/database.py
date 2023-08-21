import motor.motor_asyncio
from decouple import config


MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.balances

balance_collection = database.get_collection("balances_collection")


def balance_helper(balance) -> dict:
    return {
        "id": str(balance["_id"]),
        "address": balance["address"],
        "balance": balance["balance"],
        "value": balance["value"],
        "timestamp": balance["timestamp"],
        "date": balance["date"]
    }

# Retrieve all user balances present in the database


async def retrieve_balances(address: str):
    balances = []
    async for balance in balance_collection.find({"address": address}).sort("timestamp", -1):
        balances.append(balance_helper(balance))
    return balances


# Add a new user balance into to the database
async def add_balance(balance_data: dict) -> dict:
    balance = await balance_collection.insert_one(balance_data)
    new_balance = await balance_collection.find_one({"_id": balance.inserted_id})
    return balance_helper(new_balance)
