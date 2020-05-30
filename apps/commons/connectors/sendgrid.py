
import os
import sendgrid

from apps.commons import constants

class SendGridConnector:

    def __init__(self, ref):
        self.reference_id = ref


    def send_mail(self, to_emails, from_email, subject, content=str(), template_id=str(), dynamic_template_data=dict()):
        try:
            to_emails = list(map(lambda t: { 'email': t }, to_emails))

            request_body = {
                'personalizations': [{
                    'to': to_emails,
                    'subject': subject
                }],
                'from': {
                    'email': from_email
                }
            }

            if template_id:
                request_body['personalizations'][0]['dynamic_template_data'] = dynamic_template_data
                request_body['template_id'] = template_id
            
            else:
                request_body['content'] = [{
                    'type': 'text/plain',
                    'value': content
                }]

            print('sendgrid connector [reference id = {}] request body - {}'.format(self.reference_id, request_body))
            
            try:
                sg = sendgrid.SendGridAPIClient(api_key=constants.SENDGRID_API_KEY)
                response = sg.client.mail.send.post(request_body=request_body)
            
            except Exception as sge:
                raise Exception(sge.body)

            print('sendgrid connector [reference id = {}] success'.format(self.reference_id))

        except Exception as e:
            print('sendgrid connector [reference id = {}] exception - {}'.format(self.reference_id, str(e)))
            raise e
