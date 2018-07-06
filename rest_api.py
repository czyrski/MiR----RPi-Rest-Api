import requests
import json
import time
from gpiozero import Button
import pifacerelayplus

# inicjowanie zmiennych
button=Button(2) #przycisk
pfr=pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY) #pi face relay plus

#initial
print "Skrypt OK"

url='http://mir.com/api/v2.0.0/registers/2'
headers= {'Content-Type': 'application/json', 'Accept-Language':'en_US', 'Host':'mir.com:8080', 'Authorization':'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='}
data={"value": 0,"label": "Piface relay 0"}
r=requests.put(url, data=json.dumps(data), headers=headers, )


while True:

    time.sleep(0.05)

    #sprawdzenie czy trwa przerwa na produkcji
    hour=time.strftime("%-H") #format 24h decimal bez zera na przodzie
    hour=int(hour)
    minute=time.strftime("%-M") #decimal bez zera na przodzie
    minute=int(minute)


    if (hour==9 and 45<minute<59) or (hour==17 and 45<minute<59) or (hour==1 and 45<minute<59):
        url='http://mir.com/api/v2.0.0/registers/3'
        headers= {'Content-Type': 'application/json', 'Accept-Language':'en_US', 'Host':'mir.com:8080', 'Authorization':'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='}
        data={"value": 1,"label": "Break indicator"}

        r=requests.put(url, data=json.dumps(data), headers=headers, )
    else:
        url='http://mir.com/api/v2.0.0/registers/3'
        headers= {'Content-Type': 'application/json', 'Accept-Language':'en_US', 'Host':'mir.com:8080', 'Authorization':'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='}
        data={"value": 0,"label": "Break indicator"}

        r=requests.put(url, data=json.dumps(data), headers=headers, )
        
    #obsluga rejestru i piface relay 0
    url='http://mir.com/api/v2.0.0/registers/2'
    headers= {'Content-Type': 'application/json', 'Accept-Language':'en_US', 'Host':'mir.com:8080', 'Authorization':'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='}
    
    r=requests.get(url, headers=headers, )
    if r.text[-6:-3] == "1.0" and pfr.relays[0].value == 0:
        print r.text[-6:-3]
        pfr.relays[0].set_high()
       
    
    # obsluga przycisku
    if button.is_pressed:
        url='http://mir.com/api/v2.0.0/registers/1'
        headers= {'Content-Type': 'application/json', 'Accept-Language':'en_US', 'Host':'mir.com:8080', 'Authorization':'Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=='}
        data={"value": 1,"label": "Raspberry button"}

        r=requests.put(url, data=json.dumps(data), headers=headers, )
    
    #zerowanie przekaznika 
    if r.text[-6:-3]=="0.0" and pfr.relays[0].value == 1:
        pfr.relays[0].set_low()
            
    
