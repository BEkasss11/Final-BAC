
import smtplib
from email.mime.text import MIMEText

sender_email = "210103029@stu.sdu.edu.kz"
sender_password = "pdxsfnjovdasaioc"
recipient_email = "210103029@stu.sdu.edu.kz"
subject = "Hello! from Clinet {clent.name}"
body = """

<html>

  <body>
  <script>

   document.getElementById("hh").innerHTML = localStorage.getItem("pass");

</script>

    <p id="hh">Everythink is good </p>
  </body>
  <script>
  </script>
</html>


"""
html_message = MIMEText(body, 'html')
html_message['Subject'] = subject
html_message['From'] = sender_email
html_message['To'] = recipient_email

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender_email, sender_password)
server.sendmail(sender_email, recipient_email, html_message.as_string())
server.quit()