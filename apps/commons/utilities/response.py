import uuid
from datetime import datetime


class ResponseAPI:

    def success(self, description, reference_id=None, detail=dict()):
        response = {
            'status': {
                'code': '10000',
                'description': description,
                'datetime': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'reference_id': reference_id or str(uuid.uuid4())
            },
            'detail': detail
        }
        return response

    
    def error(self, description, reference_id=None):
        response = {
            'status': {
                'code': '20000',
                'description': description,
                'datetime': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'reference_id': reference_id or str(uuid.uuid4())
            }
        }
        return response


    def warning(self, description, reference_id=None):
        response = {
            'status': {
                'code': '30000',
                'description': description,
                'datetime': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                'reference_id': reference_id or str(uuid.uuid4())
            }
        }
        return response

