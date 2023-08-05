# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Psychology Evaluation - Operating Unit Integration",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "ssi_psychology_evaluation",
        "ssi_psychology_operating_unit",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir_rule_data.xml",
        "views/psychology_evaluation_views.xml",
        "views/psychology_evaluation_batch_views.xml",
    ],
}
