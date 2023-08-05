# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyConsultationType(models.Model):
    _name = "psychology_consultation_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Psychology Consultation Type"

    allowed_psychologist_ids = fields.Many2many(
        string="Allowed Psychologists",
        comodel_name="res.users",
        relation="rel_psy_consultation_type_2_allowed_psychologist",
        column1="type_id",
        column2="user_id",
    )
