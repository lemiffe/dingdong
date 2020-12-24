#!/usr/bin/env python3
import requests, json, sys
import numpy as np
import sounddevice as sd
import time as t
from config import CONFIG

time_since_last_webhook = t.time() - 30

def check_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    #print ("|" * int(volume_norm))
    if int(volume_norm) >= CONFIG['threshold']:
        global time_since_last_webhook
        current_time = t.time()
        diff_time = current_time - time_since_last_webhook
        print(" * vol: " + str(volume_norm) + " (timer: " + str(diff_time) + "s) *")
        if (diff_time > 120):
            print("[SEND!] Volume: " + str(volume_norm) + ". " + str(diff_time) + " secs after last trigger.")
            for webhook in CONFIG['webhooks']:
                print(" -> Webhook: " + webhook['url'])
                if CONFIG['debug'] == False:
                    result = requests.post(webhook['url'], data=json.dumps(webhook['data']), headers=webhook['headers'])
                    try:
                        result.raise_for_status()
                    except requests.exceptions.HTTPError as err:
                        print(err)
            time_since_last_webhook = t.time()

try:
    while True:
        print ("Listening (for 60s)... (" + str(t.time()) + ")")
        with sd.Stream(callback=check_sound):
            sd.sleep(60000)
except KeyboardInterrupt:
    print('Ending program (keyboard interrupt)!')
