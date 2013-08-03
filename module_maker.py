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
from template import OpenERPTemplate
from openerp.osv import osv
from openerp.osv import fields
import types
import os
import inspect
import tempfile
import zipfile
import base64

from openerp import addons

replace_list = [' ', ',', '.', '-']


def get_name(name):
    for ch in replace_list:
        name = name.replace(ch, "_")
    return name


def zipdir(path, zip_file, temp_dir):
    rootlen = len(path) + 1
    for base, dirs, files in os.walk(path):
        for file_path in files:
            fn = os.path.join(base, file_path)
            zip_file.write(fn, fn[rootlen:])


def _get_fields_type(self, cr, uid, context=None):
    # Avoid too many nested `if`s below, as RedHat's Python 2.6
    # break on it. See bug 939653.
    return sorted([(k, k) for k, v in fields.__dict__.iteritems()
                   if isinstance(type(v), types.TypeType) and
                   inspect.isclass(v) and
                   issubclass(v, fields._column) and
                   v != fields._column and
                   not v._deprecated and
                   not issubclass(v, fields.function)])


class module_module(osv.osv):
    _name = 'module.module'
    _description = 'Module '

    def _get_file_name(self, cr, uid, ids, name, arg, context={}):
        res = {}
        for self_obj in self.browse(cr, uid, ids, context=context):
            res[self_obj.id] = self_obj.name + '.zip'

        return res

    _columns = {
        'name': fields.char('Module Name', size=64, required=True),
        'template_path': fields.char("Tempalte Path", size=256, required=True),
        'object_ids': fields.one2many('module.object', 'module_id',
                                      'Module object'),
        'module_file': fields.binary('Module File'),
        'file_name': fields.function(_get_file_name,
                                     method=True,
                                     string='File Name',
                                     type='char',
                                     store=False, ),
    }

    def _get_tempalte_path(self, cr, uid, context={}):
        return os.path.join(addons.__path__[0], "oe_module_maker",
                            "template")

    _defaults = {
        'template_path': _get_tempalte_path,
    }

    def get_comnpany_data(self, cr, uid, context={}):
        company_pool = self.pool.get('res.company')
        company_obj = company_pool.browse(
            cr, uid, company_pool._company_default_get(
                cr, uid, self._name, context=context), context=context)
        return {'name': company_obj.name, 'short_name': company_obj.name,
                'website': company_obj.website}

    def genrate_module(self, cr, uid, ids, context={}):

        for self_obj in self.browse(cr, uid, ids, context=context):
            sub_folder = []
            basic_file = []
            xml_file = []
            objs = []
            openerp_data = {
                'sub_folder': sub_folder,
                'basic_file': basic_file,
                'xml_file_list': xml_file,
                'object_datas': []}
            for obj in self_obj.object_ids:
                sub_folder.append(get_name(obj.name))
                objs.append(get_name(obj.name))
                xml_file.append(os.path.join(get_name(obj.name), '%s_view.%s' %
                                             (get_name(obj.name), 'xml')))

                temp_dict = {
                    'list': [],
                    '_rec_name': '',
                    'inherit': '',
                    'name': obj.name,
                    'sub_folder': get_name(obj.name)}
                for field_obj in obj.field_ids:
                    temp_dict['list'].append({
                        'field': field_obj.name,
                        'filter': field_obj.filter,
                        'form': field_obj.form,
                        'help': field_obj.help,
                        'option': field_obj.selection,
                        'readonly': field_obj.readonly,
                        'related_field': field_obj.relation_field,
                        'relation': field_obj.relation,
                        'required': field_obj.required,
                        'search': field_obj.select_level,
                        'size': field_obj.size or '256',
                        'string': (field_obj.field_caption or
                                   field_obj.name.capitalize()),
                        'tree': field_obj.tree,
                        'type': field_obj.type})
                openerp_data['object_datas'].append(temp_dict)
            openerp_data['objs'] = objs
            xml_file.append("security/ir.model.access.csv")
            oe = OpenERPTemplate(self_obj.name, openerp_data,
                                 self.get_comnpany_data(cr, uid, context),
                                 self_obj.template_path)
            temp_dir = tempfile.gettempdir()
            module_path = oe.create_module(temp_dir)
            zip_file_name = os.path.join(
                temp_dir,
                get_name(self_obj.name) + '.zip')
            zip_file = zipfile.ZipFile(zip_file_name, 'w',
                                       zipfile.ZIP_DEFLATED)
            zipdir(module_path, zip_file, temp_dir)
            zip_file.close()

            file_obj = open(zip_file_name, "r")
            file_data = file_obj.read()
            file_data = base64.encodestring(file_data)
            self.write(cr, uid, ids,
                       {'module_file': file_data})

        return True

module_module()


class module_object(osv.osv):
    _name = 'module.object'
    _description = 'Module Object'

    _columns = {
        'name': fields.char('Object Name', size=64, required=True),
        'description': fields.char('Object Description', size=64,
                                   required=True),
        'field_ids': fields.one2many('module.object.field', 'object_id',
                                     'Object Fields'),
        'module_id': fields.many2one('module.module', 'Module', required=True),
    }

module_object()


class module_object_field(osv.osv):
    _name = 'module.object.field'
    _description = 'Object Field'

    _columns = {
        'name': fields.char('Field', size=64, required=True),
        'type': fields.selection(_get_fields_type, 'Field Type',
                                 required=True),
        'relation_field': fields.char('Relation Field', size=64, ),
        'relation': fields.many2one('module.object', 'Relation Object'),
        'field_caption': fields.char('Field Label', size=64),
        'selection': fields.char('Selection Options', size=128, ),
        'required': fields.boolean('Required'),
        'readonly': fields.boolean('Read-only'),
        'select_level': fields.selection(
            [('0', 'Not Searchable'), ('1', 'Always Searchable')],
            'Searchable'),
        'translate': fields.boolean('Translatable', ),
        'size': fields.integer('Size'),
        'on_delete': fields.selection(
            [('cascade', 'Cascade'), ('set null', 'Set NULL')],
            'On Delete', ),
        'domain': fields.char('Domain', size=256, ),
        'object_id': fields.many2one('module.object', 'Object'),
        'help': fields.char('Help', size=256),
        'filter': fields.boolean('Filter'),
        'form': fields.boolean('Form'),
        'tree': fields.boolean('tree'),
    }
    _defaults = {
        'filter': lambda *a: True,
        'form': lambda *a: True,
        'tree': lambda *a: True,
    }

module_object_field()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
