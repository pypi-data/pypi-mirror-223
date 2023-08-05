# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class PsychologyConsultation(models.Model):
    _name = "psychology_consultation"
    _inherit = [
        "psychology_consultation",
        "mixin.outsource_work_object",
    ]
    _outsource_work_create_page = True
    _work_log_page_xpath = "//page[@name='note']"
    _work_log_template_position = "before"

    @api.depends(
        "outsource_work_ids",
        "outsource_work_ids.type_id",
        "type_id",
    )
    def _compute_outsource_work_id(self):
        for record in self:
            result = False
            if (
                record.type_id
                and record.type_id.outsource_work_type_id
                and record.outsource_work_ids
            ):
                ttype = record.type_id
                works = record.outsource_work_ids.filtered(
                    lambda r: r.type_id.id == ttype.outsource_work_type_id.id
                )
                if len(works) > 0:
                    result = works[0].id
                record.outsource_work_id = result

    outsource_work_id = fields.Many2one(
        string="# Outsource Work",
        comodel_name="outsource_work",
        compute="_compute_outsource_work_id",
        store=True,
    )

    @ssi_decorator.post_done_action()
    def _create_outsource_work(self):
        self.ensure_one()
        if self.outsource_work_id:
            return True
        OutsourceWork = self.env["outsource_work"]
        ctx = {"outsource_work_model": self._name}
        temp_record = OutsourceWork.with_context(ctx).new(
            self._prepare_create_outsource_work()
        )

        temp_record = self._compute_outsource_work_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        OutsourceWork.create(values)

    @ssi_decorator.post_cancel_action()
    def _delete_outsource_work(self):
        if not self.outsource_work_id:
            return True

        self.outsource_work_id.unlink()

    def _get_outsource_work_model_id(self):
        self.ensure_one()
        Model = self.env["ir.model"]
        criteria = [("model", "=", self._name)]
        return Model.search(criteria)[0].id

    def _compute_outsource_work_onchange(self, temp_record):
        temp_record.onchange_usage_id()
        temp_record.onchange_pricelist_id()
        temp_record.onchange_account_id()
        temp_record.onchange_uom_id()
        temp_record.onchange_pricelist_id()
        temp_record.onchange_price_unit()

        return temp_record

    def _get_partner(self):
        self.ensure_one()
        result = False
        # TODO: Raise exception when False
        if self.psychologist_id.partner_id.contact_id:
            result = self.psychologist_id.partner_id.contact_id
        return result

    def _prepare_create_outsource_work(self):
        return {
            "partner_id": self._get_partner().id,
            "date": fields.Date.today(),
            "model_id": self._get_outsource_work_model_id(),
            "type_id": self.type_id.outsource_work_type_id.id,
            "product_id": self.type_id.outsource_work_type_id.product_id.id,
            "analytic_account_id": self.case_id.analytic_account_id.id,
            "work_object_id": self.id,
        }
