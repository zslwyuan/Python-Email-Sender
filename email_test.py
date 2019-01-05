# -*- coding: utf-8 -*-
# Python 3.6


import smtplib
from email.mime.multipart import MIMEMultipart # import MIMEMultipart
from email.mime.text import MIMEText # import MIMEText
from email.mime.base import MIMEBase # import MIMEBase
import os.path
import mimetypes
import email

def send_email_via_python(From,To,Title, Content,file_name):
    server = smtplib.SMTP_SSL("xxx.xxx.xxx", 994)   #SMTP server setting
    server.login("xxxx@xxx","xxxx")   # account and password to login  仅smtp服务器需要验证时,第一个是账号，第二个是密码

    # construct MIMEMultipart as root container 构造MIMEMultipart对象做为根容器
    main_msg = MIMEMultipart()
    # construct MIMEText objext to display content of email 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = MIMEText(Content,_charset="utf-8")
    main_msg.attach(text_msg)
 
    # construct MIMEBase objext to attach files to email 构造MIMEBase对象做为文件附件内容并附加到根容器
 
    ## read the attached file and formatdate it 读入文件内容并格式化 
    data = open(file_name, 'rb')
    ctype,encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype,subtype = ctype.split('/',1)
    file_msg = MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    email.encoders.encode_base64(file_msg)# encode the attachment 把附件编码

    ## set the header of attachment 设置附件头
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition','attachment', filename = basename) # set the header of email 修改邮件头
    main_msg.attach(file_msg)
 
    # configure the properties of root container 设置根容器属性
    main_msg['From'] = From
    main_msg['To'] = To
    main_msg['Subject'] = Title # Title for the email 标题
    main_msg['Date'] = email.utils.formatdate( )
 
    # obtain the complete text 得到格式化后的完整文本
    fullText = main_msg.as_string( )   
 
    # send the email via SMTP 用smtp发送邮件
    try:
        server.sendmail(From, To, fullText)
        
    finally:
        server.quit()
    print('send done')


##################  Above shows the details of send a email via Python                               ##########################
##################  Usually, user can only care about the things below, send emails according to the lists ##########################



Froms = ["xxx@xxx"]  # Sender list 发送邮箱列表
Tos = ["xxx@xxx"]  # Receiver list 接收邮箱列表
Titles = ["xxx"] #  Title list 标题列表
Contents = ["您好，\n    我是xxx, 这个邮件附件是个测试文件，请查收！谢谢\n\n此致\n----------------\n xxxx"] # Content list 内容列表
Attached_file_names = ["./test.jpg"] # Attachment list 附件名列表（带路径）

for From,To,Title, Content,file_name in zip(Froms, Tos, Titles, Contents,Attached_file_names):
    send_email_via_python(From,To,Title, Content,file_name) # send emails according to the lists
 

