from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged("idk", "post_install", "-at_install")
class TestSaleOrderCommissions(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create commission rules for testing, values
        # taken from the ticket's description.
        cls.commission_rules = cls.env["commission.rule"].create([{
            "commission_percentage": 0.02,
            "commission_type": "kas_fs_in",
        }, {
            "commission_percentage": 0.03,
            "commission_type": "kas_fs_out",
        }, {
            "lower_rate": 0,
            "higher_rate": 0.2499,
            "commission_percentage": 0,
            "commission_type": "kas_parts",
        }, {
            "lower_rate": 0.25,
            "higher_rate": 0.3499,
            "commission_percentage": 0.015,
            "commission_type": "kas_parts",
        }, {
            "lower_rate": 0.35,
            "higher_rate": 1,
            "commission_percentage": 0.03,
            "commission_type": "kas_parts",
        }, {
            "lower_rate": 0,
            "higher_rate": 0.2999,
            "commission_percentage": 0,
            "commission_type": "dm",
        }, {
            "lower_rate": 0.3,
            "higher_rate": 0.7,
            "commission_percentage": 0.03,
            "commission_type": "dm",
        }, {
            "lower_rate": 0.7001,
            "higher_rate": 1,
            "commission_percentage": 0,
            "commission_type": "dm",
        }, {
            "lower_rate": 0,
            "higher_rate": 0.2999,
            "commission_percentage": 0,
            "commission_type": "ts",
        }, {
            "lower_rate": 0.3,
            "higher_rate": 0.7,
            "commission_percentage": 0.02,
            "commission_type": "ts",
        }, {
            "lower_rate": 0.7001,
            "higher_rate": 1,
            "commission_percentage": 0,
            "commission_type": "ts",
        }])

        cls.partner = cls.env["res.partner"].create({
            "name": "Customer 01",
            "commission_district": "in_district",
        })

        cls.product = cls.env["product.product"].create({
            'name': 'product_01',
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'lst_price': 1000.0,
            'standard_price': 1000.0,
        })
        
        # Create sales orders so1, so2
        # with the following values
        # in the development fields:

        # so1
        # Set Commission Type FS
        # Invoice amount = 1000
        # Total cost = 680
        # Margin dollar = 320
        # Margin without freight = 32%
        # KAS FS commission = 2% of 1000 = 20
        # KAS Parts commission = 0 (Since the Commission Type is FS)
        # DM Commission = 3% of 320 = 9.6
        # TS Commission = 2% of 320 = 6.4

        # so2
        # Set Commission Type Parts
        # Invoice amount = 1000
        # Total cost = 640
        # Margin dollar = 360
        # Margin without freight = 36%
        # KAS FS commission = 0 (Since the Commission Type is Parts)
        # KAS Parts commission = 3% of 1000 = 30
        # DM Commission = 3% of 360 = 10.8 
        # TS Commission = 2% of 360 = 7.2
        cls.so1 = cls.env["sale.order"].create({
            "name": "Sale order 01",
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "order_line": [
                (0, 0, {
                    "product_id": cls.product.id, 
                    "product_uom_qty": 1, 
                    "price_unit": 1000,
                    "tax_id": False}),

            ],
            "invoiced_amount": 1000,
            "material_cost" : 300,
            "overhead_cost" : 40,
            "labor_cost" : 300,
            "parts_material_cost" : 40,
            "commission_type" : "fs",
        })

        cls.so2 = cls.env["sale.order"].create({
            "name": "Sale order 02",
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "order_line": [
                (0, 0, {
                    "product_id": cls.product.id, 
                    "product_uom_qty": 1, 
                    "price_unit": 1000,
                    "tax_id": False}),

            ],
            "invoiced_amount": 1000,
            "material_cost" : 280,
            "overhead_cost" : 40,
            "labor_cost" : 280,
            "parts_material_cost" : 40,
            "commission_type" : "parts",
        })

        # Initialize commission_district for customer
        cls.partner.write({"commission_district": "in_district"})
        
    def test_commissions_so1(self):
        self.so1.action_update_commissions()
        self.assertEqual(20, self.so1.kas_fs_commission, 
                         "KAS FS should be 20 which is 2% of 1000 (amount_untaxed, in_district customer)")
        self.assertEqual(0, self.so1.kas_parts_commission, 
                         "KAS Parts should be 0, since so1.commission_type is KAS FS")
        self.assertEqual(9.6, self.so1.dm_commission, 
                         "DM should be 9.6 which is 3% of 320 (margin_amount)")
        self.assertEqual(6.4, self.so1.ts_commission, 
                         "TS should be 6.4 which is 2% of 320 (margin_amount)")
        
    def test_commissions_so2(self):
        self.so2.action_update_commissions()
        self.assertEqual(0, self.so2.kas_fs_commission, 
                         "KAS FS should be 0, since so1.commission_type is KAS Parts")
        self.assertEqual(30, self.so2.kas_parts_commission, 
                         "KAS Parts should be 30 which is 3% of 1000 (amount_untaxed)")
        self.assertEqual(10.8, self.so2.dm_commission, 
                         "DM should be 10.8 which is 3% of 360 (margin_amount)")
        self.assertEqual(7.2, self.so2.ts_commission, 
                         "TS should be 7.2 which is 2% of 360 (margin_amount)")
    
    def test_confirmed_so_unmodified(self):
        # Only SOs in states ['draft', 'sent'] should receive commission updates
        self.so1.action_update_commissions()
        vals_before_update = {}
        vals_before_update["kas_fs_commission"] = self.so1.kas_fs_commission
        vals_before_update["kas_parts_commission"] = self.so1.kas_parts_commission
        vals_before_update["dm_commission"] = self.so1.dm_commission
        vals_before_update["ts_commission"] = self.so1.ts_commission
        self.so1.action_confirm()
        # Update a commission rule afterwards
        self.commission_rules.search([
            ("higher_rate", "=", 0.7),
            ("commission_type", "=", "dm"),
        ]).commission_percentage = 0.8
        self.so1.action_update_commissions()
        vals_after_update = {}
        vals_after_update["kas_fs_commission"] = self.so1.kas_fs_commission
        vals_after_update["kas_parts_commission"] = self.so1.kas_parts_commission
        vals_after_update["dm_commission"] = self.so1.dm_commission
        vals_after_update["ts_commission"] = self.so1.ts_commission
        self.assertEqual(vals_before_update["kas_fs_commission"], vals_after_update["kas_fs_commission"],
                         "Commission values should NOT be modified on a confirmed/cancelled SO")
        self.assertEqual(vals_before_update["kas_parts_commission"], vals_after_update["kas_parts_commission"],
                         "Commission values should NOT be modified on a confirmed/cancelled SO")
        self.assertEqual(vals_before_update["dm_commission"], vals_after_update["dm_commission"],
                         "Commission values should NOT be modified on a confirmed/cancelled SO")
        self.assertEqual(vals_before_update["ts_commission"], vals_after_update["ts_commission"],
                         "Commission values should NOT be modified on a confirmed/cancelled SO")
