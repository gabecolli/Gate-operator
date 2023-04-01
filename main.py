from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
app = Flask(__name__)

app.secret_key = 'super secret key'

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
@app.route('/protected', methods=['GET', 'POST'])
def protected():
    # check if the user is authenticated
    if not session.get('authenticated'):
        return redirect(url_for('pin'))
    else:
        print("sup homie") #replace this with the actual GPIO action you want.
        return render_template('protected.html')

if __name__ == '__main__':
    app.run(host='192.168.1.194', port=5000)