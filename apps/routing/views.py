from flask import Blueprint
from flask import request

from apps.api.notification.views import NotificationViews
from apps.api.tax.views import TaxViews
from apps.api.contact.views import ContactViews

blah_bp = Blueprint('blah_bp', __name__, template_folder='app')


# Health Check
@blah_bp.route('/', strict_slashes=False, methods=['GET'])
def indexInitial():
    return "I'm alive"


@blah_bp.route('/api/notification', strict_slashes=False, methods=['POST'])
def notificationInitial():
    return NotificationViews().post()


@blah_bp.route('/api/calculate_tax', strict_slashes=False, methods=['POST'])
def taxInitial():
    return TaxViews().post()


@blah_bp.route('/api/group', strict_slashes=False, methods=['GET', 'POST'])
@blah_bp.route('/api/group/<group_id>', strict_slashes=False, methods=['PUT', 'DELETE'])
def groupInitial(group_id=None):
    if request.method == 'GET':
        return ContactViews().list_group()
    if request.method == 'POST':
        return ContactViews().create_group()
    if request.method == 'PUT':
        return ContactViews().update_group(group_id)
    if request.method == 'DELETE':
        return ContactViews().delete_group(group_id)


@blah_bp.route('/api/contact', strict_slashes=False, methods=['GET', 'POST'])
@blah_bp.route('/api/contact/<contact_id>', strict_slashes=False, methods=['PUT', 'DELETE'])
def contactInitial(contact_id=None):
    if request.method == 'GET':
        return ContactViews().list_contact()
    if request.method == 'POST':
        return ContactViews().create_contact()
    if request.method == 'PUT':
        return ContactViews().update_contact(contact_id)
    if request.method == 'DELETE':
        return ContactViews().delete_contact(contact_id)


@blah_bp.route('/api/list_group_detail', strict_slashes=False, methods=['GET'])
def groupDetailInitial():
    return ContactViews().list_group_detail()
    