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
{
    'name': '${object["module_name"]}',
    'version': '1.0',
    'category': '',
    "sequence": 20,
    'complexity': "easy",
    'description': """
    """,
    'author': '${company["name"]}',
    'website': '${company["website"]}',
    'images': [],
    'depends': [],
    'init_xml': [],
    'update_xml': [
    % for xml_file in object['file']:
        '${xml_file}',
    %endfor
    ],
    'demo_xml': [],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
