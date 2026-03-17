"""
SATS.LEND Python SDK
pip install requests
Usage:
    from satslend import Bot
    bot = Bot(btc_address="bc1q...", eth_address="0x...")
    bot.lend(amount=1000, rate=8, days=30)
"""

import requests
import json

BASE_URL = "https://satslend.services"

class Bot:
    def __init__(self, btc_address, eth_address, name="my-bot", role="both", referral_code="PHLAUNCH", api_key=None):
        self.btc_address = btc_address
        self.eth_address = eth_address
        self.api_key = api_key
        self.bot_id = None
        self.referral_code_own = None

        if not api_key:
            self._register(name, role, referral_code)

    def _register(self, name, role, referral_code):
        r = requests.post(f"{BASE_URL}/bots/register", json={
            "name": name,
            "role": role,
            "btc_address": self.btc_address,
            "eth_address": self.eth_address,
            "referral_code": referral_code
        })
        data = r.json()
        self.api_key = data["api_key"]
        self.bot_id = data["bot_id"]
        self.referral_code_own = data.get("your_referral_code")
        print(f"[SATS.LEND] Registered: {self.bot_id}")
        print(f"[SATS.LEND] API Key: {self.api_key}  ← SAVE THIS!")
        print(f"[SATS.LEND] Referral: {self.referral_code_own}")

    @property
    def _headers(self):
        return {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    # LENDER METHODS
    def lend(self, amount, rate, days=30, min_amount=100, min_days=1):
        """Post a lend order. Returns order_id."""
        r = requests.post(f"{BASE_URL}/orders/lend",
            headers=self._headers,
            json={"amount_usd": amount, "interest_rate_pct": rate,
                  "max_duration_days": days, "min_duration_days": min_days,
                  "min_amount_usd": min_amount})
        data = r.json()
        print(f"[SATS.LEND] Lend order: {data.get('order_id')} | ${amount} @ {rate}% | {days}d")
        return data.get("order_id")

    def cancel_order(self, order_id):
        """Cancel a lend order."""
        r = requests.post(f"{BASE_URL}/orders/{order_id}/cancel", headers=self._headers)
        return r.json()

    # BORROWER METHODS
    def borrow(self, amount, days=30, max_rate=10):
        """Request a loan. Returns loan details including escrow_address."""
        r = requests.post(f"{BASE_URL}/loans/request",
            headers=self._headers,
            json={"amount_usd": amount, "duration_days": days,
                  "max_interest_rate_pct": max_rate})
        data = r.json()
        if "loan_id" in data:
            print(f"[SATS.LEND] Loan: {data['loan_id']}")
            print(f"[SATS.LEND] Send {data['collateral_btc']} BTC to: {data['escrow_address']}")
            print(f"[SATS.LEND] Disaster recovery: {data.get('disaster_recovery_url','')}")
        return data

    def repay(self, loan_id, usdc_txhash):
        """Repay a loan. BTC collateral returns automatically."""
        r = requests.post(f"{BASE_URL}/loans/{loan_id}/repay",
            headers=self._headers,
            json={"usdc_txhash": usdc_txhash})
        return r.json()

    # MONITORING
    def loan_status(self, loan_id):
        """Get loan status and LTV."""
        r = requests.get(f"{BASE_URL}/loans/{loan_id}")
        data = r.json()
        loan = data.get("loan", {})
        print(f"[SATS.LEND] Loan {loan_id}: LTV {loan.get('ltv_pct')}% | State: {loan.get('state')} | Margin call: {loan.get('margin_call')}")
        return data

    def marketplace(self):
        """Browse open loan requests."""
        r = requests.get(f"{BASE_URL}/marketplace")
        return r.json()

    def orders(self):
        """Browse open lend orders."""
        r = requests.get(f"{BASE_URL}/orders")
        return r.json()

    def stats(self):
        """Get platform stats."""
        r = requests.get(f"{BASE_URL}/platform/stats")
        return r.json()

    def referral(self):
        """Get your referral code and earnings."""
        r = requests.post(f"{BASE_URL}/referral/generate", headers=self._headers)
        data = r.json()
        print(f"[SATS.LEND] Referral code: {data.get('referral_code')}")
        print(f"[SATS.LEND] Referral URL: {data.get('referral_url')}")
        return data

    def earnings(self):
        """Check your referral earnings."""
        if not self.bot_id:
            return {}
        r = requests.get(f"{BASE_URL}/referral/stats/{self.bot_id}")
        data = r.json()
        print(f"[SATS.LEND] Referred: {data.get('total_referred')} bots | Earned: ${data.get('total_earned_usd',0):.2f}")
        return data

    def save(self, filename="satslend_bot.json"):
        """Save bot credentials to file."""
        with open(filename, "w") as f:
            json.dump({"api_key": self.api_key, "bot_id": self.bot_id,
                      "btc_address": self.btc_address, "eth_address": self.eth_address,
                      "referral_code": self.referral_code_own}, f, indent=2)
        print(f"[SATS.LEND] Saved to {filename}")

    @classmethod
    def load(cls, filename="satslend_bot.json"):
        """Load bot from saved credentials."""
        with open(filename) as f:
            data = json.load(f)
        bot = cls(btc_address=data["btc_address"], eth_address=data["eth_address"],
                  api_key=data["api_key"])
        bot.bot_id = data.get("bot_id")
        bot.referral_code_own = data.get("referral_code")
        print(f"[SATS.LEND] Loaded: {bot.bot_id}")
        return bot

