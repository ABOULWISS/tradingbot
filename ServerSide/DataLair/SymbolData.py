from sqlalchemy.orm import Session
from DataLair.DatabaseManager.database import SessionLocal
from DataLair.models.Symbol import Symbol


class SymbolData:

    # ----------------------------------------------------
    # Create symbol if not exists
    # ----------------------------------------------------
    def get_or_create_symbol(self, symbol_name: str) -> Symbol:

        if not symbol_name:
            raise ValueError("Symbol name is empty")

        session: Session = SessionLocal()

        try:
            symbol = session.query(Symbol).filter_by(Name=symbol_name).first()

            if symbol:
                return symbol

            symbol = Symbol(Name=symbol_name)
            session.add(symbol)
            session.commit()
            session.refresh(symbol)

            return symbol

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    # ----------------------------------------------------
    # Get symbol by name (read only)
    # ----------------------------------------------------
    def get_symbol(self, symbol_name: str) -> Symbol | None:

        session: Session = SessionLocal()

        try:
            return session.query(Symbol).filter_by(Name=symbol_name).first()

        finally:
            session.close()

    # ----------------------------------------------------
    # Get all symbols
    # ----------------------------------------------------
    def get_all_symbols(self):

        session: Session = SessionLocal()

        try:
            return session.query(Symbol).all()

        finally:
            session.close()