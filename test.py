from pageschecker import PagesChecker
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendNotification(content, title):
    # set up the SMTP server
    s = smtplib.SMTP(host='mail.appcom.xyz', port=587)
    s.starttls()
    s.login("theoguidoux@appcom.xyz", "8a8aa3acd17e")

    # For each contact, send the email:
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = title

    # Prints out the message body for our sake

    # setup the parameters of the message
    msg['From']="theoguidoux@appcom.xyz"
    msg['To']="theoguidoux@appcom.xyz"
    msg['Subject']=content

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()

def onPageChangeEvent(url):
	print("onPageChangeEvent("+str(url)+")")
	sendNotification("Coronavirus Update !", "Go : https://www.worldometers.info/coronavirus/")


#call onPageChangeEvent each time a webpage has changed
urls = ["https://www.worldometers.info/coronavirus/"]

pc = PagesChecker(urls, onchange=onPageChangeEvent)
pc.run()
