# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Psychologycase(models.Model):
    _name = "psychology.case"
    _inherit = [
        "psychology.case",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
