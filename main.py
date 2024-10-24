from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import discord
import uvicorn
import asyncio
from threading import Thread
from credentials import *

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@app.post("/price-alert")
async def price_alert(request: Request):
    data = await request.json()  # Get the JSON data from the request
    print("Received data:", data)  # Print the received data
    return JSONResponse(content={"message": "Price alert received!"}, status_code=200)  # Respond with a success message

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

def start_discord_bot():
    client.run(token)

if __name__ == '__main__':
    # Start the Discord bot in a separate thread
    discord_thread = Thread(target=start_discord_bot)
    discord_thread.start()

    # Start the FastAPI server
    uvicorn.run(app, host='0.0.0.0', port=42069)
