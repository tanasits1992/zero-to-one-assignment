import sys 
import os
import uuid

from flask import request, jsonify
from flask_api import status

from apps.commons import constants
from apps.commons.utilities.response import ResponseAPI


class TaxViews:
    reference_id = str(uuid.uuid4())
    response_api = ResponseAPI()

    def post(self):
        try:
            print('tax API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('tax API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            net_income = request_data.get('net_income')
            if net_income is None:
                raise Exception('net income is required')

            net_income = float(net_income)
            pit = self.calculate_tax(net_income)

            result = {
                'pit': pit
            }

            response = self.response_api.success('success', self.reference_id, result)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)
            
        finally:
            print('tax API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK

    def calculate_tax(self, net_income):
        try:
            tax_rates = constants.TAX_RATES
            # Sorted reverse
            tax_rates = sorted(tax_rates, key=(lambda tr: tr.get('upper_bound') or sys.maxsize), reverse=True)

            pit = 0.0
            remain = net_income

            for tax_rate in tax_rates:
                lower_bound = tax_rate.get('lower_bound') or 0
                rate = tax_rate.get('rate') or 0
                
                if remain >= lower_bound:
                    pit += (remain - (lower_bound - 1)) * rate / 100
                    remain = lower_bound - 1

            return pit

        except Exception as e:
            raise e