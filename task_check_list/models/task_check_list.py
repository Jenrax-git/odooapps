# Copyright © Jenrax SRL - www.jenrax.com
from odoo import api, fields, models


class TaskChecklist(models.Model):
    _name = "task.checklist"
    _description = "Checklist for Task"

    name = fields.Char(required=True)
    description = fields.Char()


class ProjectTask(models.Model):
    _inherit = "project.task"

    task_checklist = fields.Many2many("task.checklist", string="Check List")
    checklist_progress = fields.Float(
        compute="_compute_checklist_progress",
        string="Progress",
        store=True,
    )

    @api.depends("task_checklist")
    def _compute_checklist_progress(self):
        total = self.env["task.checklist"].search_count([])
        for task in self:
            task.checklist_progress = (
                len(task.task_checklist) * 100.0 / total if total else 0.0
            )
