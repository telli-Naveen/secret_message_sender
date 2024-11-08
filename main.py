from flask import Flask, redirect, url_for, render_template, request
import base64

app = Flask(__name__)


@app.route("/encrypt", methods=["POST", "GET"])
def encrypt():
    if request.method == "POST":
        input_string = request.form['Message']
        key_string = request.form['Key']
        input_string = input_string.replace("\n","<newline>")
        key_value = sum(ord(char) for char in key_string)
        shift_value = key_value // 100


        if shift_value == 0:
            shift_value = 56

        encrypted_string = ""
        for char in input_string:
            new_ascii = ord(char) + shift_value


            if new_ascii > 126:
                new_ascii = 32 + (new_ascii - 127) % 95

            encrypted_string += chr(new_ascii)
        encrypted_string = base64.urlsafe_b64encode(encrypted_string.encode()).decode('utf-8')
        encrypted_string = "https://secret-message-sender.onrender.com/encrypt/" + encrypted_string
        return render_template('index.html', result=encrypted_string)


    return render_template("index.html")


@app.route("/encrypt/<data>", methods=["POST", "GET"])
def decrypt(data):
    
    if request.method == "POST":
        encrypted_string = request.form["Message"]
        encrypted_string = base64.urlsafe_b64decode(encrypted_string).decode('utf-8')
        key_string = request.form['Key']

        key_value = sum(ord(char) for char in key_string)
        shift_value = key_value // 100


        if shift_value == 0:
            shift_value = 56

        
        decrypted_string = ""
        for char in encrypted_string:
            new_ascii = ord(char) - shift_value


            if new_ascii < 32:
                new_ascii = 127 - (32 - new_ascii) % 95

            decrypted_string += chr(new_ascii)
        decrypted_string = decrypted_string.replace("<newline>", "<br>")
        decrypted_string = decrypted_string.replace("l<br>","<br>")
        return render_template('index.html', result=decrypted_string, decrypt_guide='Enter correct key to decrypt correctly')
    return render_template('index1.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
