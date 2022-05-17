import datetime
with open('message.txt', encoding='utf8') as f:
        last_time = int(datetime.datetime.now().timestamp())
        print(last_time)