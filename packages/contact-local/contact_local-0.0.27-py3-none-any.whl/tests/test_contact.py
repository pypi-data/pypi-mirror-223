import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from datetime import datetime
from dotenv import load_dotenv
import pytest
from Contact.contact_api import contact
from db import contactView



load_dotenv()
logzio_token = os.getenv("LOGZIO_TOKEN")
print(logzio_token)


updated_contact_data = {
'id': 99, 
'person_id': 71117,
'name_prefix': 'Dr.',
'first_name': 'John',
'additional_name': 'M.',
'job_title': 'Software Engineer'
}



@pytest.mark.test
def test_insert_select():
    contact.insert_contact(1,"test3",2, 'Mr.','shnizel','','Software Engineer')
    contactRes = contactView.get_contact_by_account_name('test3')
    contactRes is not None

@pytest.mark.test
def test_update():
    contact.update_contact_data_by_id(updated_contact_data)
    contactRes = contactView.get_contact_by_id(99)
    assert contactRes['person_id']== 71117
    assert contactRes['name_prefix']=='Dr.'
    assert contactRes['first_name']== 'John'
    assert contactRes['additional_name']== 'M.'
    assert contactRes['job_title']== 'Software Engineer'

@pytest.mark.test
def test_select_valid():
    contactRes = contactView.get_contact_by_id(99)
    contactRes is not None


@pytest.mark.test
def test_select_valid():
    contactRes = contactView.get_contact_by_id(12121231765)
    contactRes is None
