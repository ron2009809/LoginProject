from flask import Flask, request

app = Flask(__name__)
comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form.get("comment", "")
        # if "<script>" in comment and "</script>" in comment:
        #     # comment = comment.replace("<script>", "").replace("</script>", "")
        #     comment = "You've done something wrong, please don't do that again)"
        comments.append(comment)

    return f"""
        <form method="POST">
            <input name="comment" placeholder="Leave a comment">
            <button type="submit">Post</button>
        </form>
        <hr>
        <h3>Comments:</h3>
        {'<br>'.join(f"<p>{c}</p>" for c in comments)}
    """

# <script> alert("This is an advertisement"); </script>
# <script>window.location.href = "https://surl.li/rqxpvc"</script>

# <style> .clickJacking {position: absolute;left: 182px;top: 8px;z-index: 1;}</style><button name="clickJacking" type="submit" class="clickJacking">Click</button>