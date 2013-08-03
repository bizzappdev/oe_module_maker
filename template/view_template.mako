<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <record id="view_${object['name'].replace('.','_')}_tree" model="ir.ui.view">
            <field name="name">${object['name']}.tree</field>
            <field name="model">${object['name']}</field>
            <field name="priority" eval="8"/>
            <field name="arch" type="xml">
            <tree string="${object['name'].replace('.',' ').title()}">
                %for field in object['list']:
                 %if field['tree']:
            	<field name="${field['field'].strip()}"/>
                 %endif
                %endfor
            </tree>
            </field>
        </record>

        <record id="view_${object['name'].replace('.','_')}_form" model="ir.ui.view">
            <field name="name">${object['name']}.form</field>
            <field name="model">${object['name']}</field>
            <field name="priority" eval="8"/>
            <field name="arch" type="xml">
            <form string="${object['name'].replace('.',' ').title()}">
            %for field in object['list']:
            %if field['form']:
              %if field['type'] in ('o2m','m2m'):
                <separator string="${field['string']}" colspan="4"/>
                <field name="${field['field'].strip()}" colspan="4" nolabel="1"/>
              %else:
                <field name="${field['field'].strip()}"/>
              %endif
             %endif
            %endfor
            </form>
            </field>
        </record>

        <record id="view_${object['name'].replace('.','_')}_search" model="ir.ui.view">
            <field name="name">${object['name']}.search</field>
            <field name="model">${object['name']}</field>
            <field name="priority" eval="8"/>
            <field name="arch" type="xml">
            <search string="${object['name'].replace('.',' ').title()}">
                %for field in object['list']:
                %if field['type'] not in ('binary','o2m') and field['search']:
                <field name="${field['field'].strip()}"/>
                %endif
                %endfor
                <newline/>
                <group expand="0" string="Group By...">
                    %for field in object['list']:
                    %if field['type'] not in ('binary','o2m') and field['filter']:
                    <filter string="${field['string']}" domain="[]" context="{'group_by':'${field['field']}'}"/>
                    %endif
                    %endfor
                </group>
            </search>
            </field>
        </record>

        <record model="ir.actions.act_window" id="act_open_${object['name'].replace('.','_')}_view">
            <field name="name">${object['name'].replace('.',' ').title()}</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">${object['name']}</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="search_view_id" ref="view_${object['name'].replace('.','_')}_search"/>
            <field name="domain">[]</field>
            <field name="context">{}</field>
        </record>

        <record model="ir.actions.act_window.view" id="act_open_${object['name'].replace('.','_')}_view_form">
            <field name="act_window_id" ref="act_open_${object['name'].replace('.','_')}_view"/>
            <field name="sequence" eval="20"/>
            <field name="view_mode">form</field>
            <field name="view_id" ref="view_${object['name'].replace('.','_')}_form"/>
        </record>

        <record model="ir.actions.act_window.view" id="act_open_${object['name'].replace('.','_')}_view_tree">
            <field name="act_window_id" ref="act_open_${object['name'].replace('.','_')}_view"/>
            <field name="sequence" eval="10"/>
            <field name="view_mode">tree</field>
            <field name="view_id" ref="view_${object['name'].replace('.','_')}_tree"/>
        </record>

    </data>
</openerp>
