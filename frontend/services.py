from interfaces import IAuthService, IPortfolioService
from model import Portfolio, Stock
from datetime import datetime

class AuthService(IAuthService):
    def __init__(self):
        self.valid_users = {
            "admin": "password123",
            "user1": "user123"
        }
    
    def authenticate(self, username: str, password: str) -> bool:
        return (username in self.valid_users and 
                self.valid_users[username] == password)

class PortfolioService(IPortfolioService):
    def __init__(self):
        # Mock data for demonstration
        self.mock_portfolio = Portfolio(
            stocks=[
                Stock("AAPL", 10, 150.00),
                Stock("GOOGL", 5, 2800.00)
            ],
            last_updated=datetime.now()
        )

    def get_portfolio(self, user_id: str) -> Portfolio:
        return self.mock_portfolio

    def execute_buy_order(self, user_id: str, symbol: str, shares: int) -> bool:
        # Mock implementation
        return True

    def execute_sell_order(self, user_id: str, symbol: str, shares: int) -> bool:
        # Mock implementation
        return True
