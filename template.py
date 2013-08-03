#!/usr/bin/env python
# -*- coding: utf-8 -*-
#/#############################################################################
#
#    BizzAppDev
#    Copyright (C) 2004-TODAY bizzappdev(<http://www.bizzappdev.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################
import os
from mako.template import Template


def get_next_name(module_name):
    next_number = 1
    while True:
        if not os.path.exists('%s_%s' % (module_name, next_number)):
            break
        next_number += 1
    return '%s_%s' % (module_name, next_number)


def write_file(file_name, data):
    file_obj = open(file_name, "w")
    file_obj.write(data)
    file_obj.close()


class OpenERPTemplate(object):

    def __init__(self, module_name, OpenERPData, company_data, template_path):
        self.OpenERPData = OpenERPData
        self.module_name = module_name
        self.company_data = company_data
        self.template_path = template_path

    def create_module(self, addons_location):

        if not os.path.exists(addons_location):
            raise OSError("Provided addons path not found: %s" %
                          addons_location)

        module_path = os.path.join(addons_location, self.module_name)

        if os.path.exists(module_path):
            module_path_new = get_next_name(module_path)
            os.rename(module_path, module_path_new)

        os.mkdir(module_path)

        list_sub_folder = self.OpenERPData['sub_folder']

        for sub_folder in list_sub_folder:
            os.mkdir(os.path.join(module_path, sub_folder))
        os.mkdir(os.path.join(module_path, "security"))
        init_data = list_sub_folder + [x.replace('.py', "") for x in
                                       self.OpenERPData.get('basic_file', [])]
        self.init_file(module_path, init_data)
        openerp_data = {
            'file': self.OpenERPData.get('xml_file_list', []),
            'module_name': self.module_name,
        }
        self.openerp_file(module_path, openerp_data)

        for object_data in self.OpenERPData['object_datas']:
            self.py_file(module_path, object_data)
            self.xml_file(module_path, object_data)
        self.security_file(module_path, self.OpenERPData)
        return module_path
    def security_file(self, module_path, object_list):
        security_temp = Template(filename=os.path.join(
            self.template_path, 'security.mako'))
        file_path = 'ir.model.access.csv'
        file_path = os.path.join(module_path, 'security',
                                 file_path)
        sec_data = security_temp.render(object=object_list)
        write_file(file_path, sec_data)
                  
    def xml_file(self, module_path, object_data):
        view_temp = Template(filename=os.path.join(
            self.template_path, 'view_template.mako'))
        file_path = '%s_view.%s' % (object_data['name'].replace(".", "_"),
                                    "xml")
        file_path = os.path.join(module_path, object_data['sub_folder'],
                                 file_path)
        view_data = view_temp.render(object=object_data,
                                     company=self.company_data)
                                     
        write_file(file_path, view_data)

    def py_file(self, module_path, object_data):
        py_temp = Template(filename=os.path.join(self.template_path,
                                                 "py_template.mako"))
        file_path = '%s.%s' % (object_data['name'].replace(".", "_"), "py")
        file_path = os.path.join(module_path, object_data['sub_folder'],
                                 file_path)
        py_data = py_temp.render(object=object_data, company=self.company_data)
        write_file(file_path, py_data)

    def openerp_file(self, module_path, openerp_data):
        oper_temp = Template(
            filename=os.path.join(self.template_path,
                                  'module_openerp_template.mako'))
        oper_data = oper_temp.render(object=openerp_data,
                                     company=self.company_data)

        write_file(os.path.join(module_path,
                                '__openerp__.py'), oper_data)

    def init_file(self, module_path, init_data):
        file_name = os.path.join(
            self.template_path, 'init_template.mako')
        init_temp = Template(filename=file_name)

        init_data = init_temp.render(object=init_data,
                                     company=self.company_data)

        write_file(os.path.join(module_path, '__init__.py'), init_data)


if __name__ == '__main__':
    object_datas = [
        {'_rec_name': '',
         'inherit': '',
         'list': [{'field': 'name',
                   'filter': 0,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Name',
                   'tree': 1,
                   'type': 'char'},
                  {'field': 'number',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Number',
                   'tree': 1,
                   'type': 'integer'},
                  {'field': 'gender',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': [('male', 'Male'), ('female', 'Female')],
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Gender',
                   'tree': 1,
                   'type': 'selection'}],
         'sub_folder': '',
         'name': 'test.test'},
        {'_rec_name': '',
         'inherit': '',
         'list': [{'field': 'name',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Name',
                   'tree': 1,
                   'type': 'char'},
                  {'field': 'number',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Number',
                   'tree': 1,
                   'type': 'integer'},
                  {'field': 'gender',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': [('male', 'Male'), ('female', 'Female')],
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 0,
                   'search': 1,
                   'size': '256',
                   'string': 'Gender',
                   'tree': 1,
                   'type': 'selection'}],
         'sub_folder': 'sale',
         'name': 'new.test'},
        {'_rec_name': '',
         'inherit': '',
         'list': [{'field': 'name',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Name',
                   'tree': 1,
                   'type': 'char'},
                  {'field': 'number',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': '',
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Number',
                   'tree': 1,
                   'type': 'integer'},
                  {'field': 'gender',
                   'filter': 1,
                   'form': 1,
                   'help': 'test field',
                   'option': [('male', 'Male'), ('female', 'Female')],
                   'readonly': '',
                   'related_field': '',
                   'relation': '',
                   'required': 1,
                   'search': 1,
                   'size': '256',
                   'string': 'Gender',
                   'tree': 1,
                   'type': 'selection'}],
         'sub_folder': 'sale',
         'name': 'old.test'}]

    oerp = OpenERPTemplate("test_module",
                           {'sub_folder': ['sale', 'product'],
                            'basic_file': ['test.py'],
                            'object_datas': object_datas},
                           {'name': 'Ruchir Shukla', 'short_name': 'Ruchir',
                            'website': 'http://ruchir-shukla.blogspot.in/'})

    oerp.create_module("/home/ruchir/")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
