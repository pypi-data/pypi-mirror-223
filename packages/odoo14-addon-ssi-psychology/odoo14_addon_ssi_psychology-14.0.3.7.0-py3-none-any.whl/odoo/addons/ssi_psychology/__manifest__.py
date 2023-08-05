# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Psychology",
    "version": "14.0.3.7.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "configuration_helper",
        "mail",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "menu.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
        "demo/res_users_demo.xml",
    ],
}
