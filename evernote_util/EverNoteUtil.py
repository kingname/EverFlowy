"""
EverNoteUtil.py
~~~~~~~~~~~~~~~

This module is used to generate the enml format content and then sync it to evernote.

As every item in workflowy is in the format like:
{
    'nm': 'title',
    'ch': [{'nm': '2.1'},
           {'nm': '2.2',
            'ch': [{
                'nm': '2.2.1',
                'ch': [{'nm': '2.2.1.1'}]
            },
                {'nm': '2.2.2'}]},
           {'nm': '2.3'}]
}

this module will convert it to the `enml` format so that evernote could parse:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
    <ul>
        <li>2.1</li>
        <li>
            2.2
            <ul>
                <li>
                    2.2.1
                    <ul>
                        <li>2.2.1.1</li>
                    </ul>
                </li>
                <li>2.2.2</li>
            </ul>
        </li>
        <li>2.3</li>
    </ul>
</en-note>

Moreover, the `title` will be the title of a note in evernote.
"""
import json
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString
from evernote.api.client import EvernoteClient
from evernote.edam.type import ttypes as Types


class EverNoteUtil(object):
    def __init__(self, dev_token, template):
        self.dev_token = dev_token
        self.template = template

    def construct_body(self, project_list):
        """

        :param project_list:
        :return: {"title": xxx,
                  "body": xxx,
                  "id": xxx,
                  "detail_json": xxx}
        """
        item_list = []
        for project in project_list:
            title = project['nm']
            detail = project.get('ch', [])
            _id = project['id']
            item_list.append({'title': title,
                              'body': self.generate_body(detail),
                              'id': _id,
                              'detail_json': json.dumps(detail)})
        return item_list

    def generate_body(self, detail):
        ul = ET.Element('ul')
        for item in detail:
            name = item['nm']
            ch = item.get('ch', [])
            li = ET.Element('li')
            li.text = name
            if ch:
                li.append(self.generate_body(ch))
            ul.append(li)
        return ul

    def write_to_evernote(self, item_list):
        client = EvernoteClient(token=self.dev_token)
        # client.get_access_token()
        note_store = client.get_note_store()
        for item in item_list:
            body = ET.tostring(item['body']).decode()
            pretty_body = parseString(body).toprettyxml(indent='    ')
            note = Types.Note()
            note.title = item['title']
            note.content = self.template.format(body='\n'.join(pretty_body.split('\n')[1:]))
            received_note = note_store.createNote(note)
            print(item['title'])
            item['evernote_id'] = received_note.Guid