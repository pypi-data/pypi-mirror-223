# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
        "abstract.config.settings",
    ]

    module_ssi_psychology_evaluation = fields.Boolean(
        string="Evaluation",
    )
    module_ssi_psychology_assessment = fields.Boolean(
        string="Assessment",
    )
    module_ssi_psychology_intervention = fields.Boolean(
        string="Intervention",
    )
    module_ssi_psychology_operating_unit = fields.Boolean(
        string="Psychology Evaluation Integration With Operating Unit",
    )
    module_ssi_psychology_evaluation_related_attachment = fields.Boolean(
        string="Psychology Evaluation Integration With Related Attachment",
    )
