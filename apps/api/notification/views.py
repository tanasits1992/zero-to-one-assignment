import sys
import os
import uuid

from flask import request, jsonify
from flask_api import status

from apps.commons import constants
from apps.commons.connectors.sendgrid import SendGridConnector
from apps.commons.utilities.response import ResponseAPI


class NotificationViews:
    reference_id = str(uuid.uuid4())
    response_api = ResponseAPI()

    def post(self):
        try:
            print('notification API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('notification API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            to_emails = request_data.get('to')
            from_email = request_data.get('from')
            subject = request_data.get('subject') or ''
            content = request_data.get('message')
            template_id = request_data.get('templateID')
            dynamic_template_data = request_data.get('dynamicTemplateData') or dict()

            if to_emails is None:
                raise Exception('to is required')
            if from_email is None:
                raise Exception('from is required')
            if type(to_emails) is not list:
                if type(to_emails) is str:
                    to_emails = [
                        to_emails]
                else:
                    raise Exception('to is wrong frmat')

            send_grid_response = SendGridConnector(self.reference_id).send_mail(
                to_emails=to_emails,
                from_email=from_email,
                subject=subject,
                content=content,
                template_id=template_id,
                dynamic_template_data=dynamic_template_data
            )

            response = self.response_api.success('success', self.reference_id, send_grid_response)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('notification API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK
