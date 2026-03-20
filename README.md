# satslend — Bitcoin Lending SDK for AI Agents

Bitcoin-collateralized M2M lending for AI agents and trading bots.
Live API: https://satslend.services | No KYC | Pure API

## Install

pip install git+https://github.com/gigollo/satslend-sdk.git

or download directly:
pip install https://github.com/gigollo/satslend-sdk/releases/download/v1.0.0/satslend-1.0.0.tar.gz

## Lender Bot (3 lines)

from satslend import Bot
bot = Bot(btc_address="bc1q...", eth_address="0x...", role="lender")
bot.lend(amount=1000, rate=8, days=30)

## Borrower Bot (3 lines)

from satslend import Bot
bot = Bot(btc_address="bc1q...", eth_address="0x...", role="borrower")
loan = bot.borrow(amount=500, days=30, max_rate=10)

## Testnet — Free Testing

bot = Bot(btc_address="tb1q...", eth_address="0x...", testnet=True)
loan = bot.borrow(amount=100, days=7)
# Loan auto-funded within 15 seconds — no real money needed!

## Save and Load credentials

bot.save()
bot = Bot.load()

## Links

API: https://satslend.services
Docs: https://satslend.services/docs/
Testnet: https://satslend.services/testnet/health
GitHub: https://github.com/gigollo/satslend-sdk
