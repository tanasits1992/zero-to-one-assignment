import uuid
import os
import ast

from tempfile import mkstemp
from shutil import move, copymode
from flask import request, jsonify
from flask_api import status

from apps.commons.utilities.response import ResponseAPI


class ContactViews:
    reference_id = str(uuid.uuid4())
    response_api = ResponseAPI()
    current_path = os.path.dirname(os.path.abspath(__file__))

    def list_group(self):
        try:
            print('list group API [reference id = {}] start'.format(self.reference_id))

            result = list()

            # Read groups file
            groups = open(os.path.join(self.current_path, 'tmp', 'groups'), 'r')
            lines = groups.readlines()
            groups.close()

            for line in lines:
                # Skip comment
                if line[0] == '#':
                    continue

                # Strip new line
                line = line.rstrip('\r\n')

                group = line.split('|')
                result.append({
                    'id': group[0], 
                    'name': group[1]
                })

            response = self.response_api.success('success', self.reference_id, result)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('list group API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK

    def create_group(self):
        try:
            print('create group API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('create group API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            id = uuid.uuid4()
            name = request_data.get('name')
            if name is None:
                raise Exception('name is required')

            data = '|'.join([str(id), str(name)])
            print('create group API [reference id = {}] data - {}'.format(self.reference_id, data))

            with open(os.path.join(self.current_path, 'tmp', 'groups'), 'a') as (group):
                group.write('\n' + data)

            response = self.response_api.success('success', self.reference_id, data)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)
                
        finally:
            print('create group API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK

    def update_group(self, id):
        try:
            print('update group API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('create group API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            name = request_data.get('name')

            if id is None:
                raise Exception('id is required')
            if name is None:
                raise Exception('name is required')

            data = '|'.join([str(id), str(name)])
            print('update group API [reference id = {}] data - {}'.format(self.reference_id, data))

            found = False
            group_database_file = os.path.join(self.current_path, 'tmp', 'groups')

            # Create temp file for update file
            fh, abs_path = mkstemp()

            with os.fdopen(fh, 'w') as groups_new_file:
                with open(group_database_file) as groups_old_file:
                    for line in groups_old_file:
                        line = line.rstrip('\r\n')

                        # Skip comment
                        if line[0] == '#':
                            groups_new_file.write(line)
                            continue

                        group = line.split('|')
                        if group[0] != id:
                            groups_new_file.write('\n' + line)

                        else:
                            groups_new_file.write('\n' + data)
                            found = True

            # Copy permission file 
            copymode(group_database_file, abs_path)
            os.remove(group_database_file)
            move(abs_path, group_database_file)

            if found == False:
                raise Exception('id is invalid')

            response = self.response_api.success('success', self.reference_id, data)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('update group API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK

    def delete_group(self, id):
        try:
            print('delete group API [reference id = {}] start'.format(self.reference_id))

            if id is None:
                raise Exception('id is required')

            found = False
            group_database_file = os.path.join(self.current_path, 'tmp', 'groups')

            # Create temp file for update file
            fh, abs_path = mkstemp()

            with os.fdopen(fh, 'w') as groups_new_file:
                with open(group_database_file) as groups_old_file:
                    for line in groups_old_file:
                        line = line.rstrip('\r\n')

                        # Skip comment
                        if line[0] == '#':
                            groups_new_file.write(line)
                            continue

                        group = line.split('|')
                        if group[0] != id:
                            groups_new_file.write('\n' + line)

                        else:
                            print('delete group API [reference id = {}] delete group line - {}'.format(self.reference_id, line))
                            found = True

            copymode(group_database_file, abs_path)
            os.remove(group_database_file)
            move(abs_path, group_database_file)

            if found == False:
                raise Exception('id is invalid')

            # Delete contacts records which link groups
            contact_database_file = os.path.join(self.current_path, 'tmp', 'contacts')

            # Create temp file for update file
            fh, abs_path = mkstemp()

            with os.fdopen(fh, 'w') as contacts_new_file:
                with open(contact_database_file) as contacts_old_file:
                    for line in contacts_old_file:
                        line = line.rstrip('\r\n')

                        # Skip comment
                        if line[0] == '#':
                            contacts_new_file.write(line)
                            continue

                        contact = line.split('|')
                        if contact[7] != id:
                            contacts_new_file.write('\n' + line)

                        else:
                            print('delete group API [reference id = {}] delete contact line - {}'.format(self.reference_id, line))
                            found = True

            copymode(contact_database_file, abs_path)
            os.remove(contact_database_file)
            move(abs_path, contact_database_file)

            response = self.response_api.success('success', self.reference_id)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('delete group API [reference id = {}] response - {}'.format(self.reference_id, response))
            return jsonify(response), status.HTTP_200_OK

    def list_contact(self):
        try:
            print('list contact API [reference id = {}] start'.format(self.reference_id))

            group_id = request.args.get('group_id')
            if group_id is None:
                raise Exception('group id is required')

            # Read contacts file
            result = list()
            contacts = open(os.path.join(self.current_path, 'tmp', 'contacts'), 'r')
            lines = contacts.readlines()
            contacts.close()

            for line in lines:

                # Skip comment
                if line[0] == '#':
                    continue

                line = line.rstrip('\r\n')
                contact = line.split('|')

                if contact[7] == group_id:
                    result.append({
                        'id': contact[0], 
                        'first_name': contact[1], 
                        'last_name': contact[2], 
                        'birth_date': contact[3], 
                        'phone_numbers': ast.literal_eval(contact[4]), # convert list of string to list
                        'emails': ast.literal_eval(contact[5]), # convert list of string to list
                        'urls': ast.literal_eval(contact[6]) # convert list of string to list
                    })

            response = self.response_api.success('success', self.reference_id, result)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('list contact API [reference id = {}] response - {}'.format(self.reference_id, response))
            return (jsonify(response), status.HTTP_200_OK)

    def create_contact(self):
        try:
            print('create contact API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('create contact API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            id = uuid.uuid4()
            first_name = request_data.get('first_name')
            last_name = request_data.get('last_name')
            birth_date = request_data.get('birth_date')
            phone_numbers = request_data.get('phone_numbers') or list()
            emails = request_data.get('emails') or list()
            urls = request_data.get('urls') or list()
            group_id = request_data.get('group_id')

            if first_name is None:
                raise Exception('first name is required')
            if group_id is None:
                raise Exception('group id is required')

            data = '|'.join([str(id), str(first_name), str(last_name), str(birth_date), str(phone_numbers), str(emails), str(urls), str(group_id)])
            print('create contact API [reference id = {}] data - {}'.format(self.reference_id, data))
            
            with open(os.path.join(self.current_path, 'tmp', 'contacts'), 'a') as (contact_file):
                contact_file.write('\n' + data)

            response = self.response_api.success('success', self.reference_id, data)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('create contact API [reference id = {}] response - {}'.format(self.reference_id, response))
            return (jsonify(response), status.HTTP_200_OK)

    def update_contact(self, id):
        try:
            print('update contact API [reference id = {}] start'.format(self.reference_id))

            request_data = request.json or dict()
            if request_data is None:
                raise Exception('request is wrong format')

            print('create contact API [reference id = {}] request data - {}'.format(self.reference_id, request_data))

            first_name = request_data.get('first_name')
            last_name = request_data.get('last_name')
            birth_date = request_data.get('birth_date')
            phone_numbers = request_data.get('phone_numbers') or list()
            emails = request_data.get('emails') or list()
            urls = request_data.get('urls') or list()
            group_id = request_data.get('group_id')

            if id is None:
                raise Exception('id is required')
            if first_name is None:
                raise Exception('first name is required')
            if group_id is None:
                raise Exception('group id is required')

            data = '|'.join([str(id), str(first_name), str(last_name), str(birth_date), str(phone_numbers), str(emails), str(urls), str(group_id)])
            print('update contact API [reference id = {}] data - {}'.format(self.reference_id, data))

            found = False
            contact_database_file = os.path.join(self.current_path, 'tmp', 'contacts')

            # Create temp file
            fh, abs_path = mkstemp()

            with os.fdopen(fh, 'w') as contacts_new_file:
                with open(contact_database_file) as contacts_old_file:
                    for line in contacts_old_file:
                        line = line.rstrip('\r\n')

                        # Skip comment
                        if line[0] == '#':
                            contacts_new_file.write(line)
                            continue

                        contact = line.split('|')
                        if contact[0] != id:
                            contacts_new_file.write('\n' + line)

                        else:
                            contacts_new_file.write('\n' + data)
                            found = True

            # Copy permission file
            copymode(contact_database_file, abs_path)
            os.remove(contact_database_file)
            move(abs_path, contact_database_file)

            if found == False:
                raise Exception('id is invalid')

            response = self.response_api.success('success', self.reference_id, data)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('update contact API [reference id = {}] response - {}'.format(self.reference_id, response))
            return (jsonify(response), status.HTTP_200_OK)

    def delete_contact(self, id):
        try:
            print('delete contact API [reference id = {}] start'.format(self.reference_id))

            if id is None:
                raise Exception('id is required')

            found = False
            contact_database_file = os.path.join(self.current_path, 'tmp', 'contacts')

            # Create temp file
            fh, abs_path = mkstemp()

            with os.fdopen(fh, 'w') as contacts_new_file:
                with open(contact_database_file) as contacts_old_file:
                    for line in contacts_old_file:
                        line = line.rstrip('\r\n')

                        # Skip comment
                        if line[0] == '#':
                            contacts_new_file.write(line)
                            continue

                        contact = line.split('|')
                        if contact[0] != id:
                            contacts_new_file.write('\n' + line)

                        else:
                            print('delete contact API [reference id = {}] delete conntact line - {}'.format(self.reference_id, line))
                            found = True

            copymode(contact_database_file, abs_path)
            os.remove(contact_database_file)
            move(abs_path, contact_database_file)
            if found == False:
                raise Exception('id is invalid')
            response = self.response_api.success('success', self.reference_id)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('delete contact API [reference id = {}] response - {}'.format(self.reference_id, response))
            return (jsonify(response), status.HTTP_200_OK)

    def list_group_detail(self):
        try:
            print('list group detail API [reference id = {}] start'.format(self.reference_id))

            # Read contacts file
            contact_result = dict()
            contacts = open(os.path.join(self.current_path, 'tmp', 'contacts'), 'r')
            lines = contacts.readlines()
            contacts.close()

            for line in lines:
                # Skip comment
                if line[0] == '#':
                    continue

                line = line.rstrip('\r\n')
                contact = line.split('|')

                if contact[7] not in contact_result:
                    contact_result[contact[7]] = list()
                    
                contact_result[contact[7]].append({
                    'id': contact[0], 
                    'first_name': contact[1], 
                    'last_name': contact[2], 
                    'birth_date': contact[3], 
                    'phone_numbers': ast.literal_eval(contact[4]), # convert list of string to list
                    'emails': ast.literal_eval(contact[5]), # convert list of string to list
                    'urls': ast.literal_eval(contact[6]) # convert list of string to list
                })

            # Read groups file
            result = list()
            groups = open(os.path.join(self.current_path, 'tmp', 'groups'), 'r')
            lines = groups.readlines()
            groups.close()

            for line in lines:

                # Skip comment
                if line[0] == '#':
                    continue

                line = line.rstrip('\r\n')
                group = line.split('|')

                result.append({
                    'id': group[0], 
                    'name': group[1], 
                    'contacts': contact_result.get(group[0]) or list()
                })

            response = self.response_api.success('success', self.reference_id, result)

        except Exception as e:
            response = self.response_api.error(str(e), self.reference_id)

        finally:
            print('list group detail API [reference id = {}] response - {}'.format(self.reference_id, response))
            return (jsonify(response), status.HTTP_200_OK)
