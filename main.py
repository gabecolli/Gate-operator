from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import time
app = Flask(__name__)

app.secret_key = 'super secret key'

import RPi.GPIO as GPIO


# Set the GPIO mode to BCM numbering



# define the PIN
PIN = '172a7c9e0e37e5ff6503fc1fa323aa9d24d598db44775742c65b3489df53a2ce'  #will hardcode hash



# define a route for the PIN form
@app.route('/', methods=['GET', 'POST'])
def pin():
    if request.method == 'POST':
        pin_entered = request.form['pin']
        #hash pin_entered
        hashed_pin_entered = hashlib.sha256(str(int(pin_entered)).encode()).hexdigest()
        print(hashed_pin_entered)
        if hashed_pin_entered == PIN:
            # set a session variable to indicate that the user is authenticated
            session['authenticated'] = True
            return redirect(url_for('protected'))
        else:
            return 'Invalid PIN'
    else:
        return render_template('pin.html')
    



# define a route for the protected page
@app.route('/protected', methods=['GET','POST'])
def protected():
    gate_status = "Stationary"
    # check if the user is authenticated
    if not session.get('authenticated'):
        return redirect(url_for('pin'))
    else:
        if request.method == 'POST':
            gate_status = "in motion"
            #GPIO.setmode(GPIO.BCM)

# Set the GPIO pin to use for the relay
            #relay_pin = 17

            # Set the pin as an output pin
            #GPIO.setup(relay_pin, GPIO.OUT)

            # Turn on the relay for 5 seconds
            #GPIO.output(relay_pin, GPIO.HIGH)
            GPIO.output(7, GPIO.LOW)
            time.sleep(1)
            GPIO.output(7,GPIO.HIGH)
            time.sleep(5)
            GPIO.output(7,GPIO.LOW)
            #GPIO.output(relay_pin, GPIO.LOW)

            # Cleanup the GPIO
            #GPIO.cleanup()
            print("gate is in motion") #replace this with the actual GPIO action you want.
            time.sleep(60)
            session['authenticated'] = False
            return redirect(url_for('protected'))
        else:
            return render_template('protected.html', gate_status=gate_status)

#Below is the code for the relay. I am not sure how to integrate it into the above code. 
'''
import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin to use for the relay
relay_pin = 17

# Set the pin as an output pin
GPIO.setup(relay_pin, GPIO.OUT)

# Turn on the relay for 5 seconds
GPIO.output(relay_pin, GPIO.HIGH)
time.sleep(5)
GPIO.output(relay_pin, GPIO.LOW)

# Cleanup the GPIO
GPIO.cleanup()



'''

#TODO will need to change the IP address to the one of the Pi
if __name__ == '__main__':
    app.run(host='192.168.1.194', port=5000,debug=True)
