

import asyncio
from contextlib import asynccontextmanager
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from CoreEngineLair.MarketDataEngine import MarketDataEngine

# ------------------------
# Market engine (singleton)
# ------------------------
engine = MarketDataEngine(symbol_id=1, timeframe="1m")

# ------------------------
# WebSocket connection manager
# ------------------------
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data):
        dead = []
        for ws in self.active:
            try:
                print("Broadcasting candle:", data)
                await ws.send_json(data)
            except (WebSocketDisconnect, RuntimeError):
                print("error sending to client, disconnecting")
                dead.append(ws)

        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()

# ------------------------
# Router
# ------------------------
router = APIRouter()

@router.websocket("/ws/price")
async def ws_price(ws: WebSocket):
    await manager.connect(ws)
    print("Client connected")

    try:
        await asyncio.Event().wait()
    except WebSocketDisconnect:
        print("Client disconnected")
        manager.disconnect(ws)


# ------------------------
# Broadcaster
# ------------------------
async def broadcast_prices():
    async for candle in engine.price_feed():
        print("Broadcasting candle:", candle)
        await manager.broadcast(candle)

# ------------------------
# Lifespan (EXPORTED)
# ------------------------
@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(broadcast_prices())
    yield

# ------------------------
# REST API routes
# ------------------------
@router.get("/collect")
def collect_market_data(symbol: str, timeframe: str):
    return engine.collect_market_data(symbol, timeframe)

@router.post("/store")
def store_market_data(symbol: str, timeframe: str):
    return engine.store_market_data(symbol, timeframe)

@router.get("/getall")
def get_all_market_data():
    return engine.get_all_market_dataL()


@router.get("/getbyid/{data_id}")
def get_market_data_by_id(data_id: int):
    return engine.get_market_data_by_id(data_id)




@router.get("/getallpertf")
def get_all_candles_per_tf(tf: str):
    return engine.get_all_candles_per_timeframe(tf)








