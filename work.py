import json
import os


skip = 0
words = {'han': 0, 'hon' : 0, 'den' : 0,'det' : 0, 'denna': 0, 'denne' : 0, 'hen' : 0}

#config = {'tenant_name':os.environ['ACC-Course'],
#          'authurl':os.environ['http://smog.uppmax.uu.se:5000/v2.0']}


import urllib2
response = urllib2.urlopen('http://smog.uppmax.uu.se:8080/swift/v1/tweets/tweets_0.txt')
html = response.read()

with open(html) as f:
    for row in f:
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
