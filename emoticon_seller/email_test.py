import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    from_email = "dayofchoonsik@gmail.com"
    password = "udjadjgyrtojftgv"

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # SMTP 서버 주소에 오타 수정 및 초기화 추가
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()  # 서버와의 연결 초기화
            server.starttls()  # TLS 사용 시작
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 사용 예시
send_email("Test Subject", "This is the body of the email", "6_6ho@kakao.com")
