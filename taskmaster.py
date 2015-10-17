#!flask/bin/python

from celery import Celery
from celery import group
from work import calculate
from flask import Flask, jsonify
import subprocess
import sys
import os
#import swiftclient.client
import json
import time
import urllib2
from collections import Counter

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def task():
        print "started"
        tweets = []
        req = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets")
        response = urllib2.urlopen(req)
        tweetsObject = response.read().split()
        for t in tweetsObject:
                tweets.append(t)

        A = tweets[:1]
        B = tweets[:1]
        C = tweets[:1]
        D = tweets[:1]
        E = tweets[:1]
        
        job = group(calculate.s(A), 
                calculate.s(B), 
                calculate.s(C),
                calculate.s(D),
                calculate.s(E))

        tweetTask = job.apply_async()


        print "Celery is working..."
        counter = 0
        while (tweetTask.ready() == False):
                print "... %i s" %(counter)
                counter += 5
                time.sleep(5)

                
        print "The task is done!"

        #get values
        results = tweetTask.get()

        #summ
        c = Counter()
        for result in results:
                c.update(result)
        
        print c
        print jsonify(c)
        return jsonify(c)
        #return  jsonify(dict(c))

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

