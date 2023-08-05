# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PsychologyEvaluationBatch(models.Model):
    _name = "psychology.evaluation_batch"
    _inherit = [
        "psychology.evaluation_batch",
        "mixin.related_attachment",
    ]
    _related_attachment_create_page = True
