# - IMPORT ------------------------------------------ #
import pandas as pd
import io

from utils.loggers import Logger

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import smtplib, ssl

from config.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_FROM, EMAIL_PASSWORD, EMAIL_RECEIVERS
# --------------------------------------------------- #
class ExportCSV:
    @staticmethod
    def get_csv(data):
        try:
            columns_data = ["Data svuotamento", "Tag contribuente", "Codice tipo categoria di rifiuto", "Numero svuotamenti", "Kg pesatura", "Nota libera svuotamento"]

            df = pd.DataFrame(data=data, columns=columns_data)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

        except Exception as exc:
            Logger.log_error(f"utils.export_csv.ExportCSV - get_csv - Exception: {str(exc)}")
            csv_buffer = io.StringIO()
        finally:
            return csv_buffer

    @staticmethod
    def send_mail_csv(data):
        try:
            csv_buffer = ExportCSV.get_csv(data)

            # Creazione dell'email con allegato
            email_message = MIMEMultipart()
            email_message["From"] = EMAIL_FROM
            email_message["To"] = ", ".join(EMAIL_RECEIVERS)
            email_message["Subject"] = "Export Conferimenti"

            email_message.attach(MIMEText("In allegato il file CSV richiesto.", "plain"))

            csv_attachment = MIMEBase("application", "octet-stream")
            csv_attachment.set_payload(csv_buffer.getvalue()) #.encode("utf-8")
            encoders.encode_base64(csv_attachment)
            csv_attachment.add_header("Content-Disposition", "attachment", filename="conferimenti.csv")

            email_message.attach(csv_attachment)

            #context = ssl.create_default_context()
            context = ssl._create_unverified_context()
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.sendmail(EMAIL_FROM, EMAIL_RECEIVERS, email_message.as_string())

            #csv_buffer.getvalue()
        except Exception as exc:
            Logger.log_error(f"utils.export_csv.ExportCSV - send_csv - Exception: {str(exc)}")
        finally:
            csv_buffer.close()