# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PsychologyEvaluation(models.Model):
    _name = "psychology.evaluation"
    _inherit = [
        "psychology.evaluation",
        "mixin.single_operating_unit",
    ]
