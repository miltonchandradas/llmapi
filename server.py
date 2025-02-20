from flask import Flask

# Creates Flask serving engine
app = Flask(__name__)

@app.route("/v1/greeting", methods=["GET"])
def greeting():
    return "Hello...  Welcome to the world of Python..."

if __name__ == "__main__":
    print("Serving Initializing")
    print("Serving Started")

    app.run(host="0.0.0.0", port=5000, debug=True)