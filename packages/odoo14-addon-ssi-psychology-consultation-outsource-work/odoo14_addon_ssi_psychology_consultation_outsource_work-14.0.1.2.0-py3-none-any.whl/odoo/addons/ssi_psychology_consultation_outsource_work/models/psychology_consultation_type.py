# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PsychologyConsultationType(models.Model):
    _name = "psychology_consultation_type"
    _inherit = [
        "psychology_consultation_type",
    ]
    _description = "Psychology Consultation Type"

    outsource_work_type_id = fields.Many2one(
        string="Outsource Work Type",
        comodel_name="outsource_work_type",
    )
