# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = [
        "project.task",
    ]

    ticket_ids = fields.Many2many(
        string="Tickets",
        comodel_name="helpdesk_ticket",
        relation="rel_helpdesk_ticket_2_task",
        column1="task_id",
        column2="ticket_id",
    )
