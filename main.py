from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import discord
import uvicorn
import asyncio
from credentials import *

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

notificationQueue = []


""" Channel Definitions"""
PRICE_ALERTS = "price-alerts"

@app.post("/" + PRICE_ALERTS)
async def price_alert(request: Request):
    data = await request.json()  # Get the JSON data from the request
    #print("Received data:", data)  # Print the received data

    # Check if a channel has been specified, if not, default to this route's channel
    if("channel" not in data):
        data['channel'] = PRICE_ALERTS
    
    # Queue the notification to be handled in separate task
    notificationQueue.append(data)

    return JSONResponse(content={"message": "Price alert received!"}, status_code=200)  # Respond with a success message

@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')


async def send_message(message: str, channel: str):
    await discord_client.wait_until_ready()

    # Fetch the channel by name
    channel = discord.utils.get(discord_client.get_all_channels(), name=channel)
    if channel and isinstance(channel, discord.TextChannel):
        await channel.send(message)  # Send message to the channel
    else:
        print("Channel 'price-alerts' not found or is not a text channel.")


async def start_fastapi():
    # Run the FastAPI server
    config = uvicorn.Config(app, host='0.0.0.0', port=42069)
    server = uvicorn.Server(config)
    await server.serve()


async def serve_notification_queue():
    while True:  # Continuously handle notifications
        if notificationQueue:
            notification = notificationQueue.pop(0)  # Get the first notification

            if("data" not in notification):
                print(f"Received notification without data! Dropping notification:\n{notification}")
                continue

            if("handle" not in notification):
                print(f"Incoming notification does not have handle set. Defaulting to implicit handling:\n{notification}")
                notification['handle'] = "implicit"
            
            
            if(notification['handle'] == "implicit"):
                await handle_notification_implicit(notification['data'], notification['channel'])
            elif(notification['handle'] == "explicit"):
                await handle_notification_explicit(notification['data'], notification['channel'])
            else:
                await handle_notification_implicit(notification['data'], notification['channel'])
        
        

        await asyncio.sleep(1)  # Sleep for a bit to avoid busy-waiting

# Target is text channel
# Implicit doesn't know anything about the format of the data so it just sends the key/val pairs 
async def handle_notification_implicit(notif_data: dict, target: str):
    outStr_list = []

    for key,val in notif_data.items():
        outStr_list.append(f"{key}: {val}")  # Append formatted strings to the list

    outMsg = "\n".join(outStr_list)  # Join the list into a single string

    asyncio.create_task(send_message(outMsg, target))

    return

# Target is text channel
# You can add to the if statement to handle the data better with known formatting here
async def handle_notification_explicit(notif_data: dict, target: str):
    outMsg = ""

    if(target == PRICE_ALERTS):
        # Handle price alert messages here
        outMsg = outMsg + "\nNEW PRICE ALERT\n"
        outMsg = outMsg + "-" * 20 + "\n"
        for key,val in notif_data.items():
            outMsg = outMsg + "URL: " + key + "\n"
            outMsg = outMsg + "Price: " + val + "\n \n"
        outMsg = outMsg + "-" * 20 + "\n"


    asyncio.create_task(send_message(outMsg, target))

    return


async def main():
    # Start both the Discord bot and FastAPI server
    discord_task = asyncio.create_task(discord_client.start(token))
    fastapi_task = asyncio.create_task(start_fastapi())
    notification_task = asyncio.create_task(serve_notification_queue())  
    
    await discord_task
    await fastapi_task
    await notification_task  


if __name__ == '__main__':
    asyncio.run(main())
