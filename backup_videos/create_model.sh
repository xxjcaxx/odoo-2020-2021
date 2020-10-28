#!/bin/bash

module=$1
name=$2
parent=$3

echo -e "\nclass $name(models.Model):\n    _name = '${module}.$name'\n    name = fields.Char()  " >> ./$module/models/models.py
echo -e '<odoo><data>\n<record model="ir.actions.act_window" id="'$module'.action_'$name'_window">
         <field name="name">'$module' '$name' window</field>
         <field name="res_model">'${module}'.'$name'</field>
         <field name="view_mode">tree,form</field>
</record>
    <menuitem name="'$name'" id="'$module'.menu_'$name'" parent="'$module'.'$parent'"
              action="'$module'.action_'$name'_window"/>
\n</data></odoo>' >> ./$module/views/$name.xml

echo -e "\naccess_${module}_${name},${module}.${name},model_${module}_${name},base.group_user,1,1,1,1" >> ./$module/security/ir.model.access.csv