import json
import os
import urllib2

app = Celery('tasks', backend='amqp', broker='amqp://worker:worker@130.238.29.173/rabbithost')

@app.task
def calculate (adresses):
    for adress in adresses:
        print 'started'
        skip = 0
        words = {'han': 0, 'hon' : 0, 'den' : 0,'det' : 0, 'denna': 0, 'denne' : 0, 'hen' : 0}

        response = urllib2.urlopen('http://smog.uppmax.uu.se:8080/swift/v1/tweets/tweets/' + adress)


        for row in response:
            if (row == ''):
                break 
            if (row == '\n'):
                continue 

            json2 = json.loads(row)
            if ('retweeted_status'  in json2):
                skip = skip + 1
                continue
            text = json2['text']

            for word in words:
                n = text.count(word)
                amount = words.get(word)
                words[word] = n + amount


            for word in words:
                print('ordet ' + word + " antalet " + str(words[word]))  
                print('skip ' + str(skip))     
