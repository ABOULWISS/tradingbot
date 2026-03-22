


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from DataLair.DatabaseManager.database import engine, Base



from FastAPiLayer.MarketData import (
    router as market_data_router,
    lifespan as marketdata_lifespan,
)

from FastAPiLayer.MarketStructureAPI import (
    router as market_structure_router,
    lifespan as marketstructure_lifespan,
)






# 🔥 Lifespan موحد يشغل الاثنين
@asynccontextmanager
async def main_lifespan(app: FastAPI):
    async with marketdata_lifespan(app):
        async with marketstructure_lifespan(app):
            yield

app = FastAPI(lifespan=main_lifespan)


'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
       "http://localhost:3000",
       "http://127.0.0.1:3000",
       "http://127.0.0.1:5173",
       "http://localhost:5173",
       "http://localhost:8000",
       "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 TEMP FIX
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_data_router)
app.include_router(market_structure_router)