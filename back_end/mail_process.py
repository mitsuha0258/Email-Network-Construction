import os

import poplib
from email.parser import BytesParser, Parser
from email.policy import default
import re

regex = re.compile(r'<[^>]+>')


def remove_html(string):
    return regex.sub('', string)


def login(mail_id, mail_key):
    pop_server = poplib.POP3("pop.qq.com")
    pop_server.user(mail_id)
    pop_server.pass_(mail_key)
    return pop_server


def get_mail():
    pop_server = login()
    mail_num = len(pop_server.list()[1])
    mail_list = []
    for m in range(mail_num, mail_num - 1, -1):  # 第二个元素应该是0
        pop_server.close()
        pop_server = login()
        resp, data, octets = pop_server.retr(m)
        msg_data = b'\r\n'.join(data)
        msg = BytesParser(policy=default).parsebytes(msg_data)
        print(type(msg))
        print('发件人:' + msg['from'])
        print('收件人:' + msg['to'])
        print('主题:' + msg['subject'])
        print('第一个收件人名字:' + msg['to'].addresses[0].username)
        print('第一个发件人名字:' + msg['from'].addresses[0].username)
        mail_text = ""
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
                # 如果maintype是text，说明是邮件正文部分
            elif part.get_content_maintype() == 'text':
                mail_text += str(part.get_content())
        mail_list.append(mail_handle(mail_text))
    return mail_list


def mail_process_use_path(path: list):
    mail_list = read_mail(path)
    return extrace_mail(mail_list)


def mail_process_use_account(mail_id, mail_key):
    mail_list = get_mail(mail_id, mail_key)
    return extrace_mail(mail_list)


def mail_handle(mail_text: str):
    mail_text = remove_html(mail_text).split("\n")
    mail_final_text = ""
    for line in mail_text:
        line_copy = line
        line_copy = line_copy.replace(" ", "").replace("\r", "").replace("\t", "").replace("&nbsp;", "")
        if line_copy != '':
            line = line.replace("&nbsp;", "").strip(" ")
            mail_final_text += line
            mail_final_text += "\n"
    return mail_final_text


def read_mail(path: list):
    mail_result = []
    for p in path:
        if not os.path.isfile(p):
            return Exception("The File in the path is illegal")
        with open(p, "r", encoding="utf8") as reader:
            mail_text = reader.read()
        mail_result.append(mail_handle(mail_text))
    return mail_result


def extrace_mail(mail_list):
    pass
    return None  # return 处理后的data
