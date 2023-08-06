# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class OdooImplementation(models.Model):
    _name = "odoo_implementation"
    _inherit = [
        "odoo_implementation",
    ]

    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_project_id(self):
        self.project_id = False
