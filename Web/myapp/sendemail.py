import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'zunoc123@gmail.com'
	mypassword = '0805465856'
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin Web'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเว็บไซต์'
newmember_name = 'Test'
content = ''' กรุณายืนยันอีเมล์ '''
msg = 'สวัสดี {}\n\n {}'.format(newmember_name,content)

sendthai('zunoc123@gmail.com',subject,msg) 