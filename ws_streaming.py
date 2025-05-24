import asyncio
import json
import logging
import signal
import os

from websockets import connect
from dotenv import load_dotenv


print("🟢 Script iniciou")


load_dotenv()
SYMBOLS = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")
print("Símbolos =", SYMBOLS)


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class BinanceWSClient:
    def __init__(self, symbols):
        self.symbols = [s.lower() for s in symbols]
        self.base_url = "wss://stream.binance.com:9443/ws"
        self.ws = None
        self.connected = False
        self.keep_running = True

    def _build_stream_url(self) -> str:
        streams = "/".join(f"{sym}@trade" for sym in self.symbols)
        return f"{self.base_url}/{streams}"

    async def connect(self):
        url = self._build_stream_url()
        logging.info(f"Tentando conectar em {url}")
        try:
            self.ws = await connect(url)
            self.connected = True
            logging.info("Conectado com sucesso!")
        except Exception as e:
            logging.error(f"Falha ao conectar: {e}")
            self.connected = False

    async def _handle_message(self, message: str):
        data = json.loads(message)
        symbol = data.get("s")
        price  = float(data.get("p", 0))
        qty    = float(data.get("q", 0))
        ts     = data.get("T")
        logging.info(f"[{symbol}] Price={price}, Qty={qty}, Timestamp={ts}")
        

    async def run(self):
        while self.keep_running:
            if not self.connected:
                await self.connect()
                if not self.connected:
                    await asyncio.sleep(5)
            try:
                async for msg in self.ws:
                    await self._handle_message(msg)
            except (asyncio.CancelledError, Exception) as e:
                logging.warning(f"Conexão encerrada ou erro: {e}")
                self.connected = False

    def stop(self):
        logging.info("Parando cliente...")
        self.keep_running = False
        if self.ws:
            asyncio.create_task(self.ws.close())

if __name__ == "__main__":
    client = BinanceWSClient(symbols=SYMBOLS)
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: client.stop())
    asyncio.run(client.run())
