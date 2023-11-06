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
                (0, 0, {'product_id': 1, 'product_uom_qty': 1, 'price_unit': 1,}),
                (0, 0, {'product_id': 2, 'product_uom_qty': 1, 'price_unit': 1,}),

            ],
            'material_cost' : 10,
            'overhead_cost' : 10,
            'labor_cost' : 10,
            'parts_material_cost' : 10,
        })
        cls.so.action_confirm()
  
    def test_total_cost(self):
        self.assertEqual(40, self.so.total_cost, 
                         "In this case, the total should be 40 which is a sum of the other costs")
