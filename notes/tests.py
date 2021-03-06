"""
******************************************************************************
* Purpose: purpose is to define the tests for the APIs defined for the app using
           pytest
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import json
import os
from django.contrib.auth.models import User
from notes.models import Label, Note, EmailTemplate
from fundoonote.settings import note_create_url, label_create_url, note_url, label_url, \
    archive_notes_url, trash_notes_url, reminder_url, send_mail_url
from rest_framework.test import APITestCase

with open(os.path.dirname(__file__).split('/notes')[0] + '/templates' + str('/testing_note.json'), 'r') as f:
    DATA = json.load(f)
    header = {
        'HTTP_AUTHORIZATION':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxMzMyOTkwLCJqdGkiOiIwYWZhZmZjNmI5N2M0M2U5YmI4YzM4NzliZmM3OWU2NyIsInVzZXJfaWQiOjF9.mKgTiqlatPBQFz3qtVdnyH7-R1Tz7Bx9Wm20CqWk-D0'
    }
    token = os.getenv('token')


    class LabelModelTest(APITestCase):

        def test_string_representation(self):
            label_entry = Label(label="notimportant")
            self.assertEqual(str(label_entry), label_entry.label)

        def test_string_representation1(self):
            label_entry = Label(label="very urgent")
            self.assertEqual(str(label_entry), label_entry.label)


    class NoteModelTest(APITestCase):

        def test_string_representation(self):
            note_entry = Note(title="shifting to city")
            self.assertEqual(str(note_entry), note_entry.title)

        def test_string_representation1(self):
            note_entry = Note(title="buying a pet dog")
            self.assertEqual(str(note_entry), note_entry.title)


    class NoteCreate(APITestCase):
        fixtures = ['project_database.json']

        def test_note_create_view1(self):
            response = self.client.post(path=note_create_url, data=DATA[0]['note1'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 201)

        def test_note_create_view2(self):
            response = self.client.post(path=note_create_url, data=DATA[0]['note2'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 400)

        def test_note_create_view3(self):
            response = self.client.post(path=note_create_url, data=DATA[0]['note3'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 400)


    class LabelCreate(APITestCase):
        fixtures = ['project_database.json']

        def test_label_create_view1(self):
            response = self.client.post(path=label_create_url, data=DATA[1]['label1'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 201)

        def test_label_create_view2(self):
            response = self.client.post(path=label_create_url, data=DATA[1]['label2'], **header)
            self.assertEqual(response.status_code, 400)

        def test_label_create_view3(self):
            response = self.client.post(path=label_create_url, data=DATA[1]['label3'], **header)
            self.assertEqual(response.status_code, 400)


    class NoteUpdate(APITestCase):
        fixtures = ['project_database.json']

        def test_note_update_view1(self):
            response = self.client.put(path=note_url, data=DATA[2]['note1'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)

        def test_note_update_view2(self):
            response = self.client.put(path=note_url, data=DATA[2]['note2'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 400)


    class NoteCrud(APITestCase):
        fixtures = ['project_database.json']

        def test_note_get_view(self):
            response = self.client.get(path=note_url, **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)

        def test_note_delete_view(self):
            response = self.client.delete(path=note_url, **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)


    class LabelCrud(APITestCase):
        fixtures = ['project_database.json']

        def test_label_update_view(self):
            response = self.client.put(path=label_url, data=DATA[3]['label1'], **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)

        def test_label_get_view(self):
            response = self.client.get(path=label_url, **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)

        def test_label_delete_view(self):
            response = self.client.delete(path=label_url, **header)
            print(response.content)
            self.assertEqual(response.status_code, 200)


    class ReminderArchiveTrash(APITestCase):
        fixtures = ['project_database.json']

        def test_reminder_view(self):
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' + token,
            )
            response = self.client.get(path=reminder_url)
            print(response.content)
            self.assertEqual(response.status_code, 200)

        def test_archived_view(self):
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' + token,
            )
            response = self.client.get(path=archive_notes_url)
            print(response.content)
            self.assertEqual(response.status_code, 200)


    def test_trash_view(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + token,
        )
        response = self.client.get(path=trash_notes_url)
        print(response.content)
        self.assertEqual(response.status_code, 200)


class SendEmail(APITestCase):
    fixtures = ['project_database.json']

    def test_send_email_view(self):
        response = self.client.post(path=send_mail_url, data=DATA[4]['email1'])
        print(response.content)
        self.assertEqual(response.status_code, 200)


class TitleContentFieldValidation(APITestCase):
    fixtures = ['project_database.json']

    def test_note_view1(self):
        response = self.client.post(path=note_create_url, data=DATA[5]['note1'], **header)
        print(response.content)
        self.assertLessEqual(len(DATA[5]['note1']['title']), 50)
        self.assertLessEqual(len(DATA[5]['note1']['content']), 200)

    def test_note_view2(self):
        response = self.client.post(path=note_create_url, data=DATA[5]['note2'], **header)
        print(response.content)
        self.assertLessEqual(len(DATA[5]['note2']['title']), 50)
        self.assertLessEqual(len(DATA[5]['note2']['content']), 200)

    def test_note_view3(self):
        response = self.client.post(path=note_create_url, data=DATA[5]['note3'], **header)
        print(response.content)
        self.assertGreaterEqual(len(DATA[5]['note3']['title']), 50)
        self.assertLessEqual(len(DATA[5]['note3']['content']), 200)


class UserCollaboratorLabelTypeFieldValidation(APITestCase):
    fixtures = ['project_database.json']

    def test_note_view1(self):
        response = self.client.post(path=note_create_url, data=DATA[6]['note1'], **header)
        print(response.content)
        user = User.objects.get(id=DATA[6]['note1']['user'])
        self.assertNotEqual(type(DATA[6]['note1']['user']), type(user.id))

    def test_note_view2(self):
        response = self.client.post(path=note_create_url, data=DATA[6]['note2'], **header)
        print(response.content)
        user = User.objects.get(id=DATA[6]['note2']['user'])
        self.assertEqual(type(DATA[6]['note1']['user']), type(str(user.id)))


class EmailTemplateFieldValidation(APITestCase):
    fixtures = ['project_database.json']

    def test_email_view1(self):
        response = self.client.post(path=note_create_url, data=DATA[7]['email1'], **header)
        print(response.content)
        self.assertEqual(len(DATA[7]['email1']['subject']), 255)

    def test_email_view2(self):
        response = self.client.post(path=note_create_url, data=DATA[7]['email2'], **header)
        print(response.content)
        self.assertEqual(len(DATA[7]['email2']['to_email']), 255)

    def test_email_view3(self):
        response = self.client.post(path=note_create_url, data=DATA[7]['email3'], **header)
        print(response.content)
        self.assertEqual(len(DATA[7]['email3']['from_email']), 255)

