from flask import Flask, abort, request, render_template
from gevent import pywsgi

from back_end.connection_graph import graph_data_create
from back_end.mail_process import mail_process_use_path, mail_process_use_account, login

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def main():
    return render_template("./index.html")


@app.route("/login/", methods=["POST"])  # 为什么这里用post而下面用get 因为邮箱密码不应该明文URL上传输应该用Post封装
def use_mail():
    if request.get("mail_id") is None or request.get("mail_key") is None:
        return "500 You input empty mail-id or password"
    mail_id, mail_key = request.get("mail_id"), request.get("mail_key")
    try:
        server = login()
        server.close()
    except:
        return "500 the mail and the password is not fit"

    # 这个函数用的别人的函数有点多，有可能throw exception, 反之下面就没有这个问题
    try:
        mail_extrace = mail_process_use_account(mail_id, mail_key)
    except Exception as e:
        return "500 " + e.__str__()

    return render(mail_extrace)


@app.route("/path/", methods=["GET"])
def use_path():
    if request.get("path") is None:
        return "500 You are not input any path"
    path = request.get("path")
    import os
    if os.path.isfile(path):
        mail_extrace = mail_process_use_path([path])
    elif os.path.isdir(path):
        mail_extrace = mail_process_use_path(os.listdir(path))
    else:
        mail_extrace = Exception("Path is illegal")

    if type(mail_extrace) == Exception:
        return "500" + mail_extrace.__str__()

    return render(mail_extrace)


def render(mail_extrace: list):
    return {"mail_extrace":mail_extrace, "graph_data": graph_data_create(mail_extrace)}


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
