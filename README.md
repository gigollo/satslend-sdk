# satslend — Python SDK

Bitcoin-collateralized lending for AI agents and trading bots.

## Install
pip install requests
python satslend.py

## Lender Bot (3 lines)
from satslend import Bot
bot = Bot(btc_address="bc1q...", eth_address="0x...", name="my-lender", role="lender")
bot.lend(amount=1000, rate=8, days=30)

## Borrower Bot (3 lines)
from satslend import Bot
bot = Bot(btc_address="bc1q...", eth_address="0x...", name="my-borrower", role="borrower")
loan = bot.borrow(amount=500, days=30, max_rate=10)

## Save/Load credentials
bot.save()  # saves to satslend_bot.json
bot = Bot.load()  # loads saved bot

## Docs
https://satslend.services
https://github.com/gigollo/satslend-api
