#!/usr/bin/python
#
# Copyright (C) 2013 Connectify
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import gdata.docs
import gdata.docs.client
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import gdata.sample_util
import atom
import getopt
import re
import sys
import string
import socket
import datetime


class AppConfig(object):
    APP_NAME = 'ConnectifyTestingSpreadsheetReporter'
    DEBUG = False

class SpreadsheetReporter:

    def __init__(self, email, password):
        self.gd_service = gdata.spreadsheet.service.SpreadsheetsService()
        self.gd_service.email = email
        self.gd_service.password = password
        self.gd_service.source = AppConfig.APP_NAME
        self.gd_service.ProgrammaticLogin()
        self.gd_client = self.CreateClient(email, password)
        self.curr_wksht_id = ''
        self.list_feed = None

        self.doc_name = socket.gethostname() + " " + \
                        str(datetime.datetime.now())
        self.CreateSpreadsheet(self.doc_name)
        self.curr_key = self.document.resource_id.text.split(':')[1]

        print 'Getting worksheets for key ' + self.curr_key
        feed = self.gd_service.GetWorksheetsFeed(self.curr_key)
        id_parts = feed.entry[0].id.text.split('/')
        self.curr_wksht_id = id_parts[len(id_parts) - 1]

        self.folder_name = 'AutomatedTesting'
        COLLECTION_QUERY_URI     = '/feeds/default/private/full/-/folder'
        target_collection = None
        for resource in self.gd_client.GetAllResources(uri=COLLECTION_QUERY_URI):
          if resource.title.text == self.folder_name:
            self.folder = resource
            self.gd_client.MoveResource(self.document,self.folder)
            return

    def CreateClient(self, email, password):
        """Create a Documents List Client."""
        client = gdata.docs.client.DocsClient(source=AppConfig.APP_NAME)
        client.http_client.debug = AppConfig.DEBUG
        # Authenticate the user with CLientLogin, OAuth, or AuthSub.
        try:
            client.client_login(email, password, AppConfig.APP_NAME)
        except gdata.client.BadAuthentication:
            exit('Invalid user credentials given.')
        except gdata.client.Error:
            exit('Login Error')
        return client

    def CreateSpreadsheet(self, title):
        """Create an empty resource of type document."""
        document = gdata.docs.data.Resource(type='spreadsheet', title=title)
        self.document = self.gd_client.CreateResource(document)
        print 'Created:', self.document.title.text, self.document.resource_id.text
        print 'Visit at https://docs.google.com/spreadsheet/ccc?key=' + \
              self.document.resource_id.text.split(':')[1]

    def _StringToDictionary(self, row_data):
        dict = {}
        for param in row_data.split(' '):
          temp = param.split('=')
          dict[temp[0]] = temp[1]
        return dict

    def AppendHeading(self, row_data):
        print('Appending \"'+row_data+'\"')
        row = 1
        col = 1
        for heading in row_data.split(','):
            entry = self.gd_service.UpdateCell(row=row, col=col, inputValue=heading,
                                               key=self.curr_key, wksht_id=self.curr_wksht_id)
            #if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
            #    print 'Updated!'
            col = col + 1

    def AppendHeadingRow(self, rowDict):
        print('Appending \"'+str(rowDict)+'\"')
        col = 1
        for elem in rowDict:
            entry = self.gd_service.UpdateCell(row=1, col=col, inputValue=str(elem),
                                               key=self.curr_key, wksht_id=self.curr_wksht_id)
            #if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
            #    print 'Updated!'
            col = col + 1

    def AppendRow(self, rowDict, row):
        if row <= 1:
            print("Can't write to row " + str(row))
            return

        print('Appending \"'+str(rowDict)+'\"')
        col = 1
        for elem in rowDict.values():
            entry = self.gd_service.UpdateCell(row=row, col=col, inputValue=str(elem),
                                               key=self.curr_key, wksht_id=self.curr_wksht_id)
            #if isinstance(entry, gdata.spreadsheet.SpreadsheetsCell):
            #    print 'Updated!'
            col = col + 1

    def AppendResultRow(self, row_data):
        print('Appending \"'+row_data+'\"')
        entry = self.gd_service.InsertRow(self._StringToDictionary(row_data),
                                         self.curr_key, self.curr_wksht_id)
        #if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        #    print 'Inserted!'

    def SanitizeHeaderString(self, str):
        sanitized_str = re.sub('[_]', '-', str)
        sanitized_str = string.lower(sanitized_str)
        return sanitized_str

    def SanitizeHeader(self, header):
        out_header = []
        for i in range(len(header)):
            out_header.append(self.SanitizeHeaderString(header[i]))
        return out_header
