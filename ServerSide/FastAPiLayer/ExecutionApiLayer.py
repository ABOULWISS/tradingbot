


from fastapi import FastAPI
from ExecutionLair.MT5Connector import MT5Connector

app = FastAPI()

# MT5 connector (lazy initialization)
mt5_api = None


@app.get("/")
def root():
    return {"status": "ok"}



@app.post("/buy")
def buy():

    global mt5_api

    # Initialize MT5 only once
    if mt5_api is None:
        try:
            mt5_api = MT5Connector(
                account=10008637589,
                password="-0JkXfPs",
                server="MetaQuotes-Demo"
            )
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # Trade params
    symbol = "EURUSD"
    volume = 0.1
   

    # Send order
    result = mt5_api.send_market_order(symbol, "buy", volume)

    return {
        "retcode": result.retcode,
        "comment": result.comment
    }





