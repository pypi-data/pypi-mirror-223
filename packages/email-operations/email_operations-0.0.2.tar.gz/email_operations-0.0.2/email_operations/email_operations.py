"""
@Time : 2023/8/2 10:00 
@Author : skyoceanchen
@TEL: 18916403796
@项目：email_operations
@File : email_operations.by
@PRODUCT_NAME :PyCharm
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import datetime
import configparser


class EmailOperations(object):
    # 创建一个解析器
    config = configparser.ConfigParser()

    def __init__(self, conf_path):
        self.config.read(conf_path, encoding='utf-8')

    def read_config(self):
        self.config.options('from_user')
        self.from_email = self.config.get('from_user', 'from_email')
        self.passwd = self.config.get('from_user', 'passwd')

    def start_send(self, subject, to_user):
        self.msg['Subject'] = subject
        self.msg['From'] = self.from_email
        self.msg['To'] = Header(",".join(to_user))
        self.msg['Date'] = Header(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  'utf-8')  # 时间可以这么获取：datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(self.from_email, self.passwd)
        try:
            s.sendmail(self.from_email, to_user, self.msg.as_string())
            # print(s.c)
            # print(f"{msg_from}  -> {subject} -> {msg_to}-> 发送{len(msg_to)}成功")
            #     源邮箱  -> 主题 -> 目标邮箱-> 是否发送成功
            return True
        except smtplib.SMTPException as e:
            s.quit()
            # print(f"{msg_from}  -> {subject} -> {msg_to}-> 发送失败，错误{str(e)}")
            return False
        finally:
            s.quit()

    def send_email(self, subject=None, to_user=None, send_content=None, send_html_file=None, send_html_img=None,
                   file_path=None, send_img=None):
        """
        :param subject: 主题
        :param to_user: 发送到那些人
        :param send_content: 发送内容
        :param send_html_file: 发送html内容
        :param send_html_img: 发送html内的图片，与send_html_file一起使用
        :param file_path: 发送附件
        :param send_img: 发送的图片
        :return:
        """
        self.msg = MIMEMultipart()
        if send_content:
            self.msg.attach(MIMEText(send_content))
        if send_html_file:
            f = open(send_html_file, 'rb')  # HTML文件默认和当前文件在同一路径下，若不在同一路径下，需要指定要发送的HTML文件的路径
            mail_body = f.read()
            f.close()
            if send_html_img:
                for index, tu_path in enumerate(send_html_img):
                    # 将图片显示在正文
                    with open(tu_path, 'rb') as f:
                        # 图片添加到正文
                        msgImage = MIMEImage(f.read())
                        # 定义图片ID
                        image_index = index + 1  # 可以添加9个图片，需要更多的话需要修改index,
                        """
                        这里是把图片发布到邮箱中，在进行引用，自行修改html
                        在html中引用使用方式为  src="cid:image2" 如下
                        <img  
                            src="cid:image2"
                            style="width: 601px; height: 338px;" id="img_insert_166558994361906185784892969268"  modifysize="97%" diffpixels="24px">
                        """
                    msgImage.add_header('Content-ID', f'<image{str(image_index)}>')
                    self.msg.attach(msgImage)
                    # print(f'<image{str(index + 1)}>', msgImage)
                #     <img src="cid:image1">
            text = MIMEText(mail_body, 'html', 'utf-8')
            self.msg.attach(text)
        # file_path = r'read.md'  #如果需要添加附件，就给定路径
        if file_path:  # 最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
            docFile = file_path
            docApart = MIMEApplication(open(docFile, 'rb').read())
            docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
            self.msg.attach(docApart)

        self.start_send(subject, to_user)
