from .DatabaseManager.database import engine, Base

from .models.Symbol import Symbol
from .models.MarketDataModel import MarketData
from .models.Account import Account
from .models.Fibonachi import Fibonacci
from .models.Liquidity import Liquidity
from .models.MarketStructure import MarketStructure
from .models.Order import Order
from .models.Person import Person
from .models.OrderBlock import OrderBlock
from .models.User import User
from .models.Position import Position
from .models.Strategy import Strategy

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    create_tables()