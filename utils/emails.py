import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from decouple import config

SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')

class SendMail:

    @staticmethod
    def send_email(subject:str, body:str, to:str, html=False, attachment=None):
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to
        message["Subject"] = subject

        if html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        if attachment:
            try:
                with open(attachment, "rb") as attach_file:
                    attachment_part = MIMEBase("application", "octet-stream")
                    attachment_part.set_payload(attach_file.read())
                    encoders.encode_base64(attachment_part)
                    attachment_part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attachment)}"
                    )
                    message.attach(attachment_part)
            except Exception as e:
                print(f"Error attaching file: {e}")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        try:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to, message.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()

if __name__=="__main__":
    html_content = """
    <html>
        <body>
            <h1 style="color:blue;">HTML Email Example</h1>
            <p>This is a <strong>styled</strong> HTML email body.</p>
        </body>
    </html>
    """
    SendMail.send_email(
        subject="Test",
        to="utsavchatterjee71@gmail.com",
        body=html_content,
        html=True,
        attachment="/media/utsav/77f97bd8-cb4e-4891-9e00-a700efef6596/python-frameworks/flask/app/templates/index.html"
    )