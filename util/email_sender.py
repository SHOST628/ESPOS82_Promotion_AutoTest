from util.mylogger import logger


class EmailSender:
    """
    construct email and send email
    """
    def __init__(self):
        pass

    def email(self):
        pass

    def send(self):
        pass


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import smtplib
import socks

# 设置smtplib所需的参数
# 下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.tech-trans.com'
username = 'ttsz'
password = '24945000'
sender = 'sincave.zhang@tech-trans.com'
# 收件人为多个收件人
receiver = ['599531369@qq.com']
subject = 'Python email test'
# 构造邮件对象MIMEMultipart对象
# 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = sender
# 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
msg['To'] = ",".join(receiver)
# 构造文字内容
text = "Hi!"
text_plain = MIMEText(text, 'plain', 'utf-8')
msg.attach(text_plain)
# # 构造附件
# sendfile = open(r'D:\pythontest\1111.txt', 'rb').read()
# text_att = MIMEText(sendfile, 'base64', 'utf-8')
# text_att["Content-Type"] = 'application/octet-stream'
# # 以下附件可以重命名成aaa.txt
# # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
# # 另一种实现方式
# text_att.add_header('Content-Disposition', 'attachment', filename='aaa.txt')
# # 以下中文测试不ok
# # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
# msg.attach(text_att)

# 发送邮件
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '172.31.0.3', 8080)
socks.wrapmodule(smtplib)
smtp = smtplib.SMTP()
smtp.set_debuglevel(True)
smtp.connect(smtpserver, 25)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()


# class Mail(object):
#     def __init__(self, host, user, passwd):
#         self._user = user
#         try:
#             server = smtplib.SMTP()
#             server.connect(host,25)
#             server.login(user, passwd)
#             self._server = server
#         except Exception as e:
#             logger.error("登陆邮件服务器失败")
#             logger.exception(e)
#
#     def send_mail(self, to_addrs, sub, content, attach_path='', attach_type='', subtype ='plain'):
#         """
#         it can send a text or html email with an attachment or many of attachments
#         :param to_addrs: the address from receiver
#         :param sub: subject name
#         :param content: email message
#         :param attach_path: attachment path
#         eg: D:\javawork\PyTest\src\main.py  or  D:\javawork\PyTest\src\main.py,D:\javawork\PyTest\src\test.jpg
#         :param attach_type: image,noimage  decide  if the file is an image or an other attachment
#         :param subtype: html file : html   ;   text file: plain
#         :return:
#         """
#         if attach_path == '':
#             msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
#         else:
#             msg = MIMEMultipart()
#             f_path_list = attach_path.split(',')
#             for f_path in f_path_list:
#                 try:
#                     if '\\' in f_path:
#                         index = f_path.rindex('\\')
#                     else:
#                         index = f_path.rindex('/')
#                     file_name = f_path[index + 1:]
#                     if attach_type == 'image':
#                         att = MIMEImage(open(attach_path, 'rb').read())
#                         att['Content-Disposition'] = 'attachment; filename="%s"' % file_name
#                         msg.attach(att)
#
#                     else:
#                         att = MIMEText(open(attach_path, 'rb').read(), 'base64', 'utf-8')
#                         att['Content-Type'] = 'application/octet-stream'
#                         att['Content-Disposition'] = 'attachment; filename="%s"' % file_name
#                         msg.attach(att)
#                         # add email message
#                         msg.attach(MIMEText(content, _subtype=subtype, _charset='utf-8'))
#                 except Exception as e:
#                     logger.exception(e)
#
#         msg['Subject'] = sub
#         msg['From'] = self._user
#         msg['To'] = to_addrs
#         to_addr_list = to_addrs.split(',')
#
#         try:
#             self._server.sendmail(self._user, to_addr_list, msg.as_string())
#             logger.info("发送了一封主题为 《%s》 的邮件给 %s , 邮件明细: %s " % (sub, to_addr_list,content))
#         except Exception as e:
#             logger.error('邮件发送失败')
#             logger.exception(e)
#
#     def __del__(self):
#         self._server.quit()
#         self._server.close()
#
#
# mail = Mail('smtp.tech-trans.com', 'ttsz', '24945000')
# mail.send_mail('599531369@qq.com', 'test', 'hello')

