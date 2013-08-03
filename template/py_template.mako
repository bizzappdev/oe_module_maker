# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#/#############################################################################
#
#    ${company['name']}
#    Copyright (C) 2004-TODAY ${company['short_name']}(${company['website']}).
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
from osv import osv, fields

class ${object['name'].replace(".","_")}(osv.osv):
    _name = '${object['name']}'
    %if object['inherit']:
    _inherit = '${object['inherit']}'
    %endif
    %if object['_rec_name']:
    _rec_name = '${object['_rec_name']}'
    %endif

    _columns = {
    % for field in object['list']:
        %if field['type'] == 'char':
            '${field['field'].strip()}': fields.${field['type']}(size=${int(float(field['size'] or 256)) }, string='${field['string']}',${field['required'] and ' required=True' or ' '}, ${field['help'] and 'help="%s"'%field['help'] or ''}),
        %elif field['type'] == 'm2o':
            '${field['field'].strip()}': fields.many2one('${field['relation']}', string='${field['string']}', ${field['required'] and ' required=True' or ' '}),
        %elif field['type'] == 'o2m':
            '${field['field'].strip()}': fields.one2many('${field['relation']}', '${field['related_field']}', string='${field['string']}', ${field['required'] and ' required=True' or ' '}),
        %elif field['type'] == 'm2m':
            '${field['field'].strip()}': fields.many2many('${field['relation']}', '${field['related_field']}', '${object['name'].replace(".","_")+"_id"}', '${field['relation'].replace(".","_")+"_id"}', string='${field['string']}'),
        %elif field['type'] == 'selection':
            '${field['field'].strip()}': fields.${field['type']}(${field['option']}, string='${field['string']}', ${field['required'] and ' required=True' or ' '}),
        %else:
            '${field['field'].strip()}': fields.${field['type']}(string='${field['string']}', ${field['required'] and ' required=True' or ' '}),
        %endif
    % endfor
    }

${object['name'].replace(".","_")}()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
