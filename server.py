from flask import Flask, Response, render_template
import sys

app = Flask(__name__)
sys.path.append('./signals')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/audio.html")
def streamwav():
    def generate():
        with open("./signals/disco_dancing.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(), mimetype="audio/x-wav")

if __name__ == "__main__":
    app.run(debug=True)



