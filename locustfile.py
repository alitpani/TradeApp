from locust import HttpUser, task, between
import json
import random

class StockTradesUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    token = None

    def on_start(self):
        """Get JWT token before starting tests"""
        # Login to get token
        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpass123"
        })
        if response.status_code == 200:
            self.token = response.json()["access"]
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task(3)
    def get_trades(self):
        """Test GET /trades/ endpoint"""
        self.client.get("/trades/")

    @task(2)
    def get_filtered_trades(self):
        """Test GET /trades/ with filters"""
        params = {
            "type": random.choice(["buy", "sell"]),
            "user_id": random.randint(1, 10)
        }
        self.client.get("/trades/", params=params)

    @task(1)
    def create_trade(self):
        """Test POST /trades/ endpoint"""
        trade_data = {
            "type": random.choice(["buy", "sell"]),
            "symbol": f"STOCK{random.randint(1, 100)}",
            "shares": random.randint(1, 100),
            "price": round(random.uniform(10.0, 1000.0), 2)
        }
        self.client.post("/trades/", json=trade_data)

    @task(1)
    def get_single_trade(self):
        """Test GET /trades/{id}/ endpoint"""
        trade_id = random.randint(1, 100)  # Assuming we have trades with IDs 1-100
        self.client.get(f"/trades/{trade_id}/") 