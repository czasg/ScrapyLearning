import pymysql
import time
import logging

from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP

logger = logging.getLogger(__name__)

threshold_value = 60 * 10  # 报警阈值

to_email = ['chenziangsg@163.com']


def send_email(SMTP_host, from_account, from_passwd, to_account, subject, content, html=False):
    if isinstance(to_account, str):
        to_account = [to_account]
    email_client = SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    if html:
        msg = MIMEText(content, 'html', 'utf-8')  # 必须是plain
    else:
        msg = MIMEText(content, 'plain', 'utf-8')  # 必须是plain
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_account
    msg['To'] = ""
    email_client.sendmail(from_account, to_account, msg.as_string())
    email_client.quit()


def main():
    db = pymysql.connect("localhost", "root", "cza19950917", "cza")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from heartbeat")
    machines_list = cursor.fetchall()

    for machine in machines_list:
        assert machine and len(machine) == 5, '未查询到监控机器/监控机器存储数据异常'
        now = time.time()
        time_diff = float(now) - float(machine['created_at'])
        if threshold_value < time_diff:
            email_count = machine['email_count']
            if email_count < 3:
                logger.error(
                    '机器 %s 异常，时差 %s min，发送报警邮件！ 警告次数 %d' % (machine['id'], int(time_diff) // 60, email_count + 1))
                try:
                    cursor.execute(
                        "update heartbeat set state=0,email_count=%d where `id`='%s'" % (
                            email_count + 1, machine['id']))
                    db.commit()
                    for email in to_email:
                        send_email('smtp.qq.com', '1970268719@qq.com', 'hzfrmpqvuhafbfdf', email, '报警邮件',
                                   '机器 %s 异常，心跳时差 %s min，发送报警邮件！ 警告次数 %d' % (
                                       machine['id'], int(time_diff) // 60, email_count + 1))
                except:
                    db.rollback()
            else:
                pass
        else:
            logger.info('机器 %s 正常，上次访问时间 %s，时差 %s min' % (
                machine['id'], datetime.fromtimestamp(int(machine['created_at'])), int(time_diff) // 60))
    db.close()


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    hdr = TimedRotatingFileHandler("supervisor.log", when="d", backupCount=3)
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)
    main()
