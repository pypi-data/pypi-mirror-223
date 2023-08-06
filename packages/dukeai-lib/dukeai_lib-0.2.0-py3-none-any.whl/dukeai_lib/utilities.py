import json
import decimal
import traceback
from dukeai_lib.globals import CUSTOMER_EMAIL_FOOTER


def send_email(
        subject: str,
        body: str,
        recipient: str,
        email_sender: str,
        footer: bool,
        email_client,
        body2="",
        body3="",
        body4="",
        body5="",
        body6="",
        body7="",
        body8=""
):
    func = send_email.__name__
    if isinstance(recipient, str):
        recipient = [recipient]

    if body2 is None:
        body2 = ""
    if body3 is None:
        body3 = ""
    if body4 is None:
        body4 = ""
    if body5 is None:
        body5 = ""
    if body6 is None:
        body6 = ""
    if body7 is None:
        body7 = ""
    if body8 is None:
        body8 = ""

    if footer:
        body_html = f"""
        <html>
        <head></head>
        <body>
        <p>{body}</p>
        <p>{body2}</p>
        <p>{body3}</p>
        <p>{body4}</p>
        <p>{body5}</p>
        <p>{body6}</p>
        <p>{body7}</p>
        <p>{body8}</p>
        {CUSTOMER_EMAIL_FOOTER}
        </body>
        </html>
        """
    else:
        body_html = f"""
        <html>
        <head></head>
        <body>
        <p>{body}</p>
        <p>{body2}</p>
        <p>{body3}</p>
        <p>{body4}</p>
        <p>{body5}</p>
        <p>{body6}</p>
        <p>{body7}</p>
        <p>{body8}</p>
        </body>
        </html>
        """
    try:
        response = email_client.send_email(
            Destination={
                'ToAddresses': recipient
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': (str(body_html)),
                    }
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=email_sender
        )
        print(f"Email sent! Message ID: {response['MessageId']}")

        return True, response, ""

    except Exception as e:
        print(f"[ERROR] {func} Error ==> {e}")
        traceback.print_exc()
        return False, {}, f"{e}"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return float(o)
        return super(DecimalEncoder, self).default(o)
