from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("https://secret-message-sender.onrender.com", methods=["POST", "GET"])
def encrypt():
    if request.method == "POST":
        input_string = request.form['Message']
        key_string = request.form['Key']

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

        encrypted_string = "https://secret-message-sender.onrender.com/decrypt/" + encrypted_string
        return render_template('index.html', result=encrypted_string)


    return render_template("index.html")


@app.route("https://secret-message-sender.onrender.com/decrypt/<data>", methods=["POST", "GET"])
def decrypt(data):
    if request.method == "POST":
        encrypted_string = request.form["Message"]
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

        return render_template('index.html', result=decrypted_string, decrypt_guide='Enter correct key to decrypt correctly')
    return render_template('index1.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
