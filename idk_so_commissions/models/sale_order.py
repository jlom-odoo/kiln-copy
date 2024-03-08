from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    commission_type = fields.Selection([
        ("parts", "Parts"),
        ("fs", "FS"),
    ], required=True, 
       default="parts")
    margin_amount = fields.Monetary(compute="_compute_margin_amount")
    kas_parts_commission = fields.Monetary(string="KAS Parts Commission")
    kas_fs_commission = fields.Monetary(string="KAS FS Commission")
    dm_commission = fields.Monetary(string="DM Commission")
    ts_commission = fields.Monetary(string="TS Commission")
    
    kas_parts_percentage = fields.Float(digits=[4,4])
    kas_fs_in_percentage = fields.Float(digits=[4,4])
    kas_fs_out_percentage = fields.Float(digits=[4,4])
    dm_percentage = fields.Float(digits=[4,4])
    ts_percentage = fields.Float(digits=[4,4])

    @api.depends("amount_untaxed", "total_cost")
    def _compute_margin_amount(self):
        for so in self:
            so.margin_amount = so.amount_untaxed - so.total_cost
    
    def action_update_commissions(self):
        self.ensure_one()
        if self.state in ["draft", "sent"]:
            grouped_rules = self.env["commission.rule"].read_group(
                [
                    "|", "&", 
                    ("lower_rate", "<=", self.margin_without_freight),
                    ("higher_rate", ">=", self.margin_without_freight),
                    ("commission_type", "in", ["kas_fs_in", "kas_fs_out"]),
                ], 
                ["commission_percentage:min"], ["commission_type"],
            )
            commission_percentages = {c["commission_type"]: c["commission_percentage"] for c in grouped_rules}

            self.kas_parts_percentage = commission_percentages.get("kas_parts", 0.0)
            self.kas_fs_in_percentage = commission_percentages.get("kas_fs_in", 0.0)
            self.kas_fs_out_percentage = commission_percentages.get("kas_fs_out", 0.0)
            self.dm_percentage = commission_percentages.get("dm", 0.0)
            self.ts_percentage = commission_percentages.get("ts", 0.0)
        
        self.dm_commission = (self.dm_percentage or 0.0) * self.margin_amount
        self.ts_commission = (self.ts_percentage or 0.0) * self.margin_amount
        
        if self.commission_type == "parts":
            self.kas_fs_commission = 0.0
            self.kas_parts_commission = (self.kas_parts_percentage or 0.0) * self.amount_untaxed
        else:
            self.kas_parts_commission = 0.0
            kas_fs_percentage = self.kas_fs_in_percentage \
                if self.partner_id.commission_district == "in_district" else self.kas_fs_out_percentage
            self.kas_fs_commission = (kas_fs_percentage or 0.0) * self.amount_untaxed
