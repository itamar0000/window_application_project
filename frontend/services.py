# services.py
from api_client import ApiClient
from model import Portfolio
from interfaces import IAuthService, IPortfolioService


class AuthService(IAuthService):
    def __init__(self):
        self.api_client = ApiClient("https://your-api-url")
    
    def authenticate(self, username: str, password: str) -> bool:
        return self.api_client.login(username, password)

class PortfolioService(IPortfolioService):
    def __init__(self):
        self.api_client = ApiClient("https://your-api-url")

    def get_portfolio(self, user_id: str) -> Portfolio:
        return self.api_client.get_portfolio(user_id)

    def execute_buy_order(self, user_id: str, symbol: str, shares: int) -> bool:
        return self.api_client.execute_buy_order(user_id, symbol, shares)

    def execute_sell_order(self, user_id: str, symbol: str, shares: int) -> bool:
        return self.api_client.execute_sell_order(user_id, symbol, shares)