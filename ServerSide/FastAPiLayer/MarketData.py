
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
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




"""






import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, Query
from CoreEngineLair.MarketDataEngine import MarketDataEngine


# ------------------------
# WebSocket connection manager
# Per-timeframe: each tf has its own set of subscribers
# ------------------------
class ConnectionManager:
    def __init__(self):
        # { "1m": [ws1, ws2], "5m": [ws3] }
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, ws: WebSocket, tf: str):
        await ws.accept()
        self.active.setdefault(tf, []).append(ws)
        print(f"Client connected for tf={tf}")

    def disconnect(self, ws: WebSocket, tf: str):
        if tf in self.active and ws in self.active[tf]:
            self.active[tf].remove(ws)
            print(f"Client disconnected from tf={tf}")

    async def broadcast(self, data: dict, tf: str):
        clients = self.active.get(tf, [])
        dead = []
        for ws in clients:
            try:
                await ws.send_json(data)
            except (WebSocketDisconnect, RuntimeError):
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, tf)


manager = ConnectionManager()

# ------------------------
# Per-timeframe engines
# Lazily created on first connection
# ------------------------
engines: dict[str, MarketDataEngine] = {}
broadcaster_tasks: dict[str, asyncio.Task] = {}


def get_or_create_engine(tf: str) -> MarketDataEngine:
    if tf not in engines:
        engines[tf] = MarketDataEngine(symbol_id=1, timeframe=tf)
        print(f"Created new engine for tf={tf}")
    return engines[tf]


async def broadcast_prices_for_tf(tf: str):
    
    engine = get_or_create_engine(tf)
    try:
        async for candle in engine.price_feed():
            print(f"[{tf}] Broadcasting candle: {candle}")
            await manager.broadcast(candle, tf)
    except Exception as e:
        print(f"[{tf}] Broadcaster error: {e}")
    finally:
        # Clean up so it can be restarted on next connection
        broadcaster_tasks.pop(tf, None)
        print(f"[{tf}] Broadcaster stopped")


def ensure_broadcaster(tf: str):
    
    if tf not in broadcaster_tasks or broadcaster_tasks[tf].done():
        task = asyncio.create_task(broadcast_prices_for_tf(tf))
        broadcaster_tasks[tf] = task
        print(f"[{tf}] Broadcaster started")


# ------------------------
# Router
# ------------------------
router = APIRouter()


@router.websocket("/ws/price")
async def ws_price(
    ws: WebSocket,
    tf: str = Query(default="1m"),   # ← reads ?tf= from query string
):
    await manager.connect(ws, tf)
    ensure_broadcaster(tf)            # ← start broadcaster if needed

    try:
        # Keep connection alive by actively reading.
        # This is the CORRECT way to detect disconnection.
        while True:
            await ws.receive_text()   # blocks until client sends or disconnects
    except WebSocketDisconnect:
        print(f"Client disconnected cleanly from tf={tf}")
    except Exception as e:
        print(f"WS error on tf={tf}: {e}")
    finally:
        manager.disconnect(ws, tf)


# ------------------------
# Lifespan
# ------------------------
@asynccontextmanager
async def lifespan(app):
    yield
    # Cancel all broadcaster tasks on shutdown
    for tf, task in broadcaster_tasks.items():
        task.cancel()
        print(f"[{tf}] Broadcaster cancelled on shutdown")


# ------------------------
# REST API routes
# ------------------------
@router.get("/collect")
def collect_market_data(symbol: str, timeframe: str):
    engine = get_or_create_engine(timeframe)
    return engine.collect_market_data(symbol, timeframe)


@router.get("/getall")
def get_all_market_data():
    engine = get_or_create_engine("1m")
    return engine.get_all_market_dataL()


@router.get("/getbyid/{data_id}")
def get_market_data_by_id(data_id: int):
    engine = get_or_create_engine("1m")
    return engine.get_market_data_by_id(data_id)


@router.get("/getallpertf")
def get_all_candles_per_tf(tf: str):
    engine = get_or_create_engine(tf)
    return engine.get_all_candles_per_timeframe(tf)
