import os
import random
from flask_cors import CORS

import psycopg2
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

DB_NAME = "loginprojectdatabase_px4j"
DB_USER = "loginprojectdatabase_px4j_user"
DB_PASS = "C3YNL7aadsJALWHte1uJkSQ6L7havJe4"
DB_HOST = "dpg-d0g200k9c44c73d5jb70-a"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connected successfully")
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM user_table;
    """)
    # Fetch all rows from the executed query
    rows = cur.fetchall()
    # print(rows)
    for row in rows:
        print(row)
    # conn.commit()
except psycopg2.Error as e:
    print("Databse not connected successfully")
    print("Error details:", e)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "roncui2009809@gmail.com"
app.config['MAIL_PASSWORD'] = "qozwszhlehkpmjfv"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

verification_code_sent_by_email = str(random.randint(100000, 999999))

@app.route("/send_email")
def index():
    mail_message = Message(
        'Verification Code For Changing Password',
        sender = 'roncui2009809@gmail.com',
        recipients = ['roncui2009809@gmail.com'])
    mail_message.body = verification_code_sent_by_email
    mail.send(mail_message)
    print(verification_code_sent_by_email)
    return render_template('verificationcodeconfirm.html')

@app.route("/verify_verification_code")
def verify_verification_code():
    verification_code = request.args.get('confirming_verification_code_for_python')
    if verification_code == verification_code_sent_by_email:
        return render_template('codeverifiedsuccessfully.html')
    else:
        return render_template('codeverifiedunsuccessfully.html')

@app.route("/New_password_created_sucessfully")
def New_password_created_sucessfully():
    NewPassword = request.args.get('new_password_for_python')
    NewPasswordConfirm = request.args.get('new_password_confirm_for_python')
    if NewPassword == NewPasswordConfirm:
        return render_template('newpasswordcreatedsuccessfully.html')
    else:
        return render_template('failedtoconfirmpassword.html')

@app.route("/code_verified_unsuccessfully")
def code_verified_unsuccessfully():
    return render_template('verificationcodeconfirm.html')
# //
@app.route("/verify_password_unsuccessfully")
def verify_password_unsuccessfully():
    return render_template('codeverifiedsuccessfully.html')
# //
@app.route('/', methods=['POST'])
def loginPage():
    loginRequest = request.get_json()
    print(loginRequest)
    return loginRequest

@app.route('/checkUsernameExistOrNot')
def checkUsernameExistOrNot():
    checkUserNameExistence = request.get_json()
    # username = request.args.get('username_for_python')
    # password = request.args.get('password_for_python')
    username = checkUserNameExistence.get('username_for_python')
    password = checkUserNameExistence.get('password_for_python')
    action = checkUserNameExistence.get('forgot_password_action')

    # action = request.args.get('forgot_password_action')

    # if request.method == 'GET':
    #     if request.method == 'POST':
    #         query = request.form['query']
    #         response = MyService.retrieve_response(query)
    #         return render_template("index.html", value=response)
    if action == 'Forgot_Password?':
        # return render_template('forgotpassword.html')
        return jsonify({"status": "forgot_password_request"})
    cur.execute("SELECT * FROM user_table WHERE user_name = %s", (username,))
    result = cur.fetchall()
    conn.commit()
    if len(result) > 0:
        cur.execute("SELECT password FROM user_table WHERE user_name = %s", (username,))
        database_password = cur.fetchone()
        if password == database_password[0]:
            cur.execute("SELECT * FROM upload_post")
            posts_info = cur.fetchall()
            cur.execute("SELECT ip_address FROM user_table WHERE user_name = %s", (username,))
            ip_address = cur.fetchone()
            # return render_template('HorizonSuccessfullyLoginPage.html', posts = posts_info, ip_address = ip_address)
            return jsonify({"status": "success", "posts": posts_info, "ip_address": ip_address}), 200
        else:
            # return render_template('reenterpasswordloginpage.html')
            return jsonify({"status": "error", "message": "Wrong Password!"}), 401
    else:
        # return render_template('checkUsernameExistOrNot.html')
        return jsonify({"status": "error", "message": "Username does not exist"}), 404

@app.route('/signUp')
def signUp():
    signUpRequest = request.get_json()
    action = signUpRequest.get('user_action')
    if action == 'tryAgain':
        # return render_template('loginpage.html')
        return jsonify({"status": "fail", "message": "Try Again"})
    else:
        # return render_template('signuppage.html')
        return jsonify({"status": "success", "message": "Sign Up Success"})

@app.route('/PasswordConfirm')
def PasswordConfirm():
    PasswordConfirmRequest = request.get_json()
    username = PasswordConfirmRequest.get('signUp_username_for_python')
    cur.execute("SELECT user_name from user_table")
    database_usernames = cur.fetchall()
    print(database_usernames)
    for string in database_usernames:
        t = "".join(string)
        print(username)
        print(database_usernames)
        print(t)
        if username == t:
            return render_template('usernamecheckforsignup.html')
    password1 = request.args.get('signUp_password1_for_python')
    password2 = request.args.get('signUp_password2_for_python')
    email = request.args.get('signUp_email_for_python')
    ip_address = request.remote_addr
    # action = request.args.get('CreateAccount')
    if password1 == password2:
        cur.execute("INSERT into user_table (user_name, password, email, ip_address) values (%s, %s, %s, %s)", (username, password2, email, ip_address))
        conn.commit()
        cur.execute("SELECT * FROM user_table")
        cur.fetchall()
        return render_template('accountcreatedsuccessfully.html')
    else:
        return "Failed To Confirm The Password, Please Enter The Password Again"

@app.route('/UploadPost')
def UploadPost():
    action = request.args.get('UploadPost_action')
    if action == 'UploadPost':
        return render_template('UploadPostPage.html')

@app.route('/SearchPost')
def SearchPost():
    action = request.args.get('SearchPost_action')
    if action == 'SearchPost':
        return render_template('SearchPostPage.html')

@app.route('/PostUploadSuccessfully')
def PostUploadSuccessfully():
    table = request.args.get('Upload_post_info_for_python')
    action = request.args.get('Uploadpost_action')
    post_title = request.args.get('post_title_for_python')
    post_information = request.args.get('post_info_for_python')
    post_tag = request.args.get('post_tag_for_python')
    upload_date = request.args.get('post_date_for_python')
    if action == 'Uploadpost':
        cur.execute("INSERT into upload_post (post_title, post_information, post_tag, upload_date) values (%s, %s, %s, %s)", (post_title, post_information, post_tag, upload_date))
        conn.commit()
        cur.execute("SELECT * FROM upload_post")
        result = cur.fetchall()
        return render_template('HorizonSuccessfullyLoginPage.html', posts = result)
    return table

# @app.route('/SearchPostInfo')
# def SearchPostInfo():
#     post_title_search = request.args.get('post_title_for_search_for_python')
#     post_tag_search = request.args.get('post_tag_for_search_for_python')
#     if action == 'Searchpost':
#         cur.execute("SELECT * FROM upload_post WHERE post_title = %s", (post_title_search,))
#         result = cur.fetchall()
#         conn.commit()

@app.route('/whatsMyIP')
def whatsMyIP():
    # if action == 'login':
    if action == request.args.get('login_action'):
        cur.execute("INSERT into user_table (user_name, password, email, ip_address) values (%s, %s, %s, %s)", (user_name, password, email, ip_address))
        conn.commit()
        cur.execute("SELECT * FROM user_table")
        result = cur.fetchall()
        return result
    print(request.remote_addr)
    return request.remote_addr

# @app.route('/hello', methods=['GET'])
# def say_hello():
#     return render_template('HorizonHomePage.html')
@app.route('/hello', methods=['GET'])
def say_hello():
    dic = {"name": "Ron"}
    return jsonify(dic)

@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({"greeting": f"Hello, {name}!"})

@app.route('/items', methods=['GET'])
def items():
    return jsonify({"items": ["apple", "banana", "cherry"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port = port)