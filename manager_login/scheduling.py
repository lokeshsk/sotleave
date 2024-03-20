import schedule
import time
from twilio.rest import Client

import mysql.connector

def db_connect():
    conn =mysql.connector.connect(host="localhost",
    user="root", 
    password="", 
    db="leaves")
    return conn

mydb = db_connect()
mycursor = mydb.cursor()
def fetch_db():
    qry = "select count(ID) from leave_records where status=%s"
    val = ('pending',)
    mycursor.execute(qry, val)
    res = mycursor.fetchall()
    return res
def job():
    #print("I'm working...")
    pending_cnt = fetch_db()
    pending_cnt_final = pending_cnt[0][0]
    account_sid = 'SID here'
    auth_token = 'AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+15622964479',
    body='Dear Manager, You have '+ str(pending_cnt_final) + ' pending leave requests. Kindly, do the needful using given link: https://sotmanager.tunnelto.dev',
    to='+91XXXXXXXXXXX'
    )
    print(message.sid)


schedule.every().monday.at("18:00").do(job)
#schedule.every().tuesday.at("11:35").do(job)
schedule.every().wednesday.at("18:06").do(job)
schedule.every().friday.at("17:30").do(job)
# schedule.every().tuesday.at("15:41").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
