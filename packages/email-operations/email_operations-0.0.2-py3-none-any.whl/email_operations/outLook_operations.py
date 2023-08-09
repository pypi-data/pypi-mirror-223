# @Time : 2021/11/21 17:18
# @Author : skyoceanchen
# @File : out.py
# @Software: PyCharm
# @PRODUCT_NAME: PyCharm
# @MONTH_NAME_SHORT:11月

import win32com.client as win32


def send_mail():
    outlook = win32.Dispatch('Outlook.Application')

    mail_item = outlook.CreateItem(0)  # 0: olMailItem

    mail_item.Recipients.Add('2331568246@qq.com')
    mail_item.Subject = 'Mail Test'

    mail_item.BodyFormat = 2  # 2: Html format
    mail_item.HTMLBody = '''
        <H2>Hello, This is a test mail.</H2>
        Hello Guys.
        '''
    mail_item.Attachments.Add(r'F:\pythonstudyother\automaticoffice\002common\邮箱\发送邮箱.py')
    mail_item.Send()


if __name__ == '__main__':
    send_mail()
