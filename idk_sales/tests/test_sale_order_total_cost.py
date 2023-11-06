from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestSaleOrderTotalCost(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.so = cls.env['sale.order'].create({
            'name': 'Sale order',
            'partner_id': 3,
            'partner_invoice_id': 3,
            'order_line': [
                (0, 0, {'product_id': 1, 'product_uom_qty': 1, 'price_unit': 100,}),

            ],
            'material_cost' : 10,
            'overhead_cost' : 10,
            'labor_cost' : 10,
            'parts_material_cost' : 50,
            'freight_out' : 10,
            'freight_in' : 10,
            'invoiced_amount' : 150,
        })
        cls.so.action_confirm()
        cls.env['ir.config_parameter'].sudo().set_param('sale.freight_profit_margin', 0.5)
        
    def test_total_cost(self):
        self.assertEqual(80, self.so.total_cost, 
                         "In this case, the total should be 80 which is a sum of the other costs")
    def test_parts_margin(self):
        self.assertEqual(0.625, self.so.parts_margin, 
                         "In this case, the part margin should be 0.645 because is the parts_material_cost/total_cost")
    def test_freight(self):
        self.assertEqual(40, self.so.freight, 
                         "In this case, the reult should be 40 as a result of (freight_in + freight_out) / freight_profit_margin")
    def test_margin_with_freight(self):
        self.assertEqual(0.2, self.so.margin_with_freight, 
                         "In this case, the part margin should be 0.2 as a result of ((invoiced_amount - (total_cost + freight)) / invoiced_amount)")
    def test_margin_without_freight(self):
        self.assertEqual(0.4666666666666667, self.so.margin_without_freight, 
                         "In this case, the part margin should be 0.467 as a result of ((invoiced_amount - total_cost) / invoiced_amount)")
