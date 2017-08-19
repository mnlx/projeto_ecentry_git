import poplib
import logging
import os
import csv
import smtplib
import email.mime.multipart as MIMEMultipart
import email.mime.text as MIMEText
import email.mime.base as MIMEBase
from email import encoders

class log():
    def __init__(self):
        SERVER = "pop.gmail.com"
        USER = "analiseecentry@gmail.com"
        PASSWORD = ""
        logging.debug('connecting to ' + SERVER)
        self.server = poplib.POP3_SSL(SERVER)
        logging.debug('logging in')
        self.server.user(USER)
        self.server.pass_(PASSWORD)

        # list items on server
        logging.debug('listing emails')
        resp, items, octets = self.server.list()
        self.total_emails = [int(str(x).split(' ')[0].split("'")[1]) for x in items][-1]
        self.loglist = []
        with open(os.path.join(os.path.dirname(__file__), 'logs/log1.csv'), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.loglist.append(row)

        self.total_analisadas = spamreader.line_num

    def emailget(self):
        diff = self.total_emails - self.total_analisadas
        self.client_list =[]
        for i in range(diff):
            resp, text, octets = self.server.retr(self.total_analisadas + i +1)
            textstr = [str(x) for x in text]
            textind = [str(x)[0:10] for x in text]

            if "b'Cliente:" in textind:
                index = textind.index("b'Cliente:")
                cliente = textstr[index].split(': ')[1].split("'")[0]

            else:
                # print(textind)
                cliente = 'Not a cliente'

            self.client_list.append(cliente)
        if diff == 0:
            self.client_list = 'Nothing to be analysed'

    def loger(self, log_list):
        for x in range(len(log_list)):
            log_list[x]= [x+self.total_analisadas+1] + log_list[x]
        with open(os.path.join(os.path.dirname(__file__), 'logs/log1.csv'), 'a') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerows(log_list)
        csvfile.close()

    def emailsend(self,send_list):


        fromaddr = "analiseecentry@gmail.com"
        toaddr = "analiseecentry@gmail.com"
        msg = MIMEMultipart.MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr

        for x in send_list:
            save_location, dominio, campanha = x
            msg['Subject'] = "[Analises Completadas]"+' dominio:' + dominio +'-' + campanha[0:15]

            body = "Análise da base {0}".format(dominio)

            msg.attach(MIMEText.MIMEText(body, 'plain'))

            filename = "{0}.txt".format(dominio+ '-' +campanha[0:15] )
            attachment = open(save_location, "rb")

            part = MIMEBase.MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)

            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
