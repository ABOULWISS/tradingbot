



from fastapi import APIRouter, HTTPException

from CoreEngineLair.MarketStructureEngine import MarketStructureService
from contextlib import asynccontextmanager
import asyncio

router = APIRouter(
    prefix="/market-structure",
    tags=["Market Structure"]
)



@router.post("/storepertimeframe")
def store_market_structure_pertimeframe(timeframe: str):
    try:  
        service = MarketStructureService()
        count = service.store_market_structure_per_timeframe(timeframe)

        return {
            "status": "ok",
            "processed_labels": count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/allPer1m")
def get_market_structure():
    service = MarketStructureService()
    return service.get_all_market_structure_data()


@router.get("/allPertimeframe")
def get_all_lables_per_time(timeframe : str): 
    service = MarketStructureService()
    return service.get_market_structure_per_timeframe(timeframe)   



async def auto_store_market_structure():
    timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]  
    while True:
        try:
            service = MarketStructureService()
            for tf in timeframes:
                count = service.store_market_structure_per_timeframe(tf)
                print(f"[MarketStructure] Stored {count} new labels for {tf}")

        except Exception as e:
            print("MarketStructure error:", e)

        await asyncio.sleep(30) 



@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(auto_store_market_structure())
    yield








