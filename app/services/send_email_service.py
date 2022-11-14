import os
import smtplib
import email.message

class SendEmailService:
    def send_email(encrypted_email, user_email):
        route = "/users/validation/"
        email_body = f"""
                  <p><a href={"http://"+os.getenv('PC2I_PUBLIC_IP_ADDRESS') +":"+ os.getenv("PORT") + route + encrypted_email}>Clique aqui para fazer a confirmação </a></p>    
                   """
        msg = email.message.Message()
        msg['Subject'] = "PC2I - Validação de cadastro"
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = f"{user_email}"

        password = os.getenv('PASSWORD')
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_body)
        smtp = smtplib.SMTP('smtp.gmail.com: 587')
        smtp.starttls()
        smtp.login(msg['From'], password)
        smtp.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

