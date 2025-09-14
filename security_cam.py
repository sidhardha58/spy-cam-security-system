from gpiozero import MotionSensor
from picamera import PiCamera
import time
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Initialize PIR motion sensor and PiCamera
pir = MotionSensor(4)
camera = PiCamera()
camera.resolution = (1024, 768)
camera.rotation = 180  # Adjust based on your camera orientation

# Email configuration
from_email_addr = 'FROM_EMAIL'
from_email_password = 'FROM_EMAIL_PASSWORD'
to_email_addr = 'TO_EMAIL'
subject = 'Security Alert!'

while True:
    if pir.motion_detected:
        print("Motion detected!")
        
        # Give camera time to adjust
        time.sleep(2)
        
        # Capture image with timestamp
        picname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
        camera.capture(picname)
        print(f"Image captured: {picname}")
        
        # Prepare email with the image
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        
        with open(picname, 'rb') as fp:
            img = MIMEImage(fp.read())
            msg.attach(img)

        # Send the email via Gmail SMTP server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(user=from_email_addr, password=from_email_password)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
        
        # Wait before detecting again (adjust as needed)
        time.sleep(5)
    else:
        print("No motion.")
