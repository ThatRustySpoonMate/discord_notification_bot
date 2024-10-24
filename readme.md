# Config
Create a file named 'credentials.py' in this directory and insert 'token=YOUR_TOKEN_HERE'

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



# To integrate 
Example POST request (Python):
```
notifyURL = "http://127.0.0.1:10001/price-alerts"
message = {'handle': 'implicit', 'channel': 'price-alerts', 'data': {'https://sydneytools.com.au/product/dewalt-dcf892p2txe-18v-50ah-xr-liion-cordless-brushless-12-detent-pin-impact-wrench-combo-kit': 699.0}}

response = requests.post(notifyURL, json=message)
```
'handle' - OPTIONAL, selects the method that will create the message to send to discord. 'implicit' simply sends the data field into the text channel without formatting, 'explicit' will apply custom formatting based on the channel field. if not provided, will default to implicit.
'channel' - OPTIONAL, the name of the text-channel to send the notification to. If not provided, will use the slug of the POST request (without the leading '/')
'data' - REQUIRED, the fields you wish to send in a discord notification. If not provided. notification will be dropped
