from config import SENDER_EMAIL, SENDGRID_API

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailService:
    def send_email(self, to_email: str, subject: str, lines: list[str]) -> bool:
        body_html = "<br>".join(lines) if lines else "No matching items today."
        html = (
            "<html><body>"
            f"<h3 style='margin:0 0 12px 0'>{subject}</h3>"
            f"<div style='font-size:14px;line-height:1.4'>{body_html}</div>"
            "</body></html>"
        )

        # If SendGrid config is missing, print email to console
        if not SENDGRID_API or not SENDER_EMAIL:
            print(f"\n--- EMAIL (console) ---\nTo: {to_email}\nSubject: {subject}\n{html}\n--- END ---\n")
            return True

        sg = SendGridAPIClient(SENDGRID_API)
        msg = Mail(from_email=SENDER_EMAIL, to_emails=to_email, subject=subject, html_content=html)
        resp = sg.send(msg)
        return 200 <= resp.status_code < 300
