# Config
Create a file named 'credentials.py' in this directory and insert 
```
token=YOUR_TOKEN_HERE
```
Note: The token is the secret that is generated on the discord developer portal when you create a new app/bot

# To Install
First pull code, then run the following commands:
```
poetry install
poetry shell
```

# To Run
```
python main.py
```



# To integrate with your products
Example POST request (Python):
```
notifyURL = "http://127.0.0.1:10001/price-alerts"
message = {'handle': 'implicit', 'channel': 'price-alerts', 'data': {'hxxps://product_url.html': "price_here"}}

response = requests.post(notifyURL, json=message)
```
'handle' - OPTIONAL, selects the method that will create the message to send to discord. 'implicit' simply sends the data field into the text channel with minimal formatting, 'explicit' will apply custom formatting based on the channel field. if not provided, will default to implicit.<br />
'channel' - OPTIONAL, the name of the text-channel to send the notification to. If not provided, will use the slug of the POST request (without the leading '/')<br />
'data' - REQUIRED, the fields you wish to send in a discord notification. If not provided. notification will be dropped<br />
