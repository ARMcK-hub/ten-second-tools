import requests
import csv

ids = [
    "bitcoin",
    "bitcoin-cash",
    "filecoin",
    "polkadot",
    "solana",
    "algorand",
    "cardano",
    "ethereum-classic",
    "ethereum",
    "chainlink",
    "the-graph",
    "matic-network",
    "storj",
    "aave",
    "compound-governance-token",
    "sushi",
    "bancor",
    "uniswap",
    "ethereum-name-service"
]

r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={'%2C'.join(ids)}&vs_currencies=usd")
data = r.json()

with open("crypto_price_data.csv", "w+") as file:
    writer = csv.writer(file)
    writer.writerow(["currency", "price_usd"])
    for id in ids:
        writer.writerow([id, data[id]['usd']])
