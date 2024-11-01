import smtplib, os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 

W_HOST: str = "smtp.gmail.com"    
W_PORT: int = 587
w_MAIL_FROM: str = "noreply@noreply.com"    

class EmailUtility:    
    
    def __init__(self) -> None:
        self.email_to : list  = []
        self.email_cc : str  = ""
        self.email_bcc: str = ""
        self.subject  : str   = ""
        self.message  : str   = ""         
    
    def send_email(self,
                   p_email_to: list,
                   p_subject: str, 
                   p_message: str,
                   p_email_cc: str = "",
                   p_email_bcc: str = "") -> None:
        self.email_to  = p_email_to
        self.email_cc  = p_email_cc
        self.email_bcc = p_email_bcc
        self.subject   = p_subject
        self.mail_message   = p_message   
                
        w_USER    : str = os.environ.get("EMAIL_USERNAME")
        W_PASS_KEY: str = os.environ.get("EMAIL_PASSWORD")            

        if not w_USER or not W_PASS_KEY:
            print("Incomplete email setup.")            
            return

        w_num_emails = len(self.email_to)
        if w_num_emails == 0 :
            print("Email address not provided.")
            return

        with smtplib.SMTP(host=W_HOST, port=W_PORT) as connection:
            connection.starttls()
            connection.login(user=w_USER, password=W_PASS_KEY)

            if p_email_cc:
                self.email_cc =  p_email_cc             
            elif w_num_emails > 1:
                self.email_cc = self.email_to[1]    

            if p_email_bcc:
                self.email_bcc =  p_email_bcc             
            elif w_num_emails > 2:
                self.email_bcc = self.email_to[2]   

            w_msg: EmailMessage = MIMEMultipart()            
            w_msg["From"]    = w_MAIL_FROM
            w_msg["To"]      = self.email_to[0]                            
            w_msg["Cc"]      = self.email_cc        
            w_msg["Bcc"]     = self.email_bcc
            w_msg["Subject"] = self.subject                        
                        

            # attach the body with the msg instance 
            w_msg.attach(MIMEText(self.mail_message, 'plain')) 

            # Converts the Multipart msg into a string 
            w_msg_text = w_msg.as_string() 
    
            if self.email_cc:                
                self.email_to.append(self.email_cc)
            if self.email_bcc:
                self.email_to.append(self.email_cc)

            # sending the mail 
            # connection.send_message(w_msg_text)        
                    
            connection.sendmail(from_addr = w_MAIL_FROM, 
                                to_addrs  = self.email_to, 
                                msg       = w_msg_text) 
            
            # terminating the session 
            connection.quit()

            print(f"Email sent successfully\nTo: {self.email_to}\nCc:{self.email_cc}\nBcc{self.email_bcc}")
            # print(f"Email sent successfully.")