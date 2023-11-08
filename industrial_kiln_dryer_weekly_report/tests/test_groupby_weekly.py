from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged 

@tagged('post_install', '-at_install')
class TestGroupbyWeekly(AccountTestInvoicingCommon):
    
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        
        cls.invoice_monday = cls.init_invoice('out_invoice', invoice_date="2023-10-30", products=cls.product_a + cls.product_b)
        cls.invoice_friday = cls.init_invoice('out_invoice', invoice_date="2023-11-03", products=cls.product_a + cls.product_b)
        cls.invoice_tuesday = cls.init_invoice('out_invoice', invoice_date="2023-11-07", products=cls.product_a + cls.product_b)
        
        cls.day_of_week = {
            'Monday': '0',
            'Tuesday': '1',
            'Wednesday': '2',
            'Thursday': '3',
            'Friday': '4',
            'Saturday': '5',
            'Sunday': '6'
        }
        
        cls.fields = ['name', 'partner_id', 'invoice_date', 'invoice_date_due',  
                  'to_check', 'payment_state', 'state', 'move_type']
        
    def test_groupby_invoices_common_functionality(self):
        '''Test to assert that original functionality is still working'''
        
        self.env['ir.config_parameter'].sudo().set_param('idk_weekly_report.start_day_of_week', self.day_of_week.get('Monday'))
        
        week_groups = self.env['account.move'].web_read_group(domain=[['move_type', '=', 'out_invoice']], fields=self.fields, groupby=['invoice_date:week'])
        self.assertTrue(len(week_groups['groups']) == 2, "Two groups should have been created")
        
        expected_ranges = ['from 2023-10-30 to 2023-11-06', 'from 2023-11-06 to 2023-11-13']
        expected_record_count_list = [2, 1]
        
        assert_groups = self.create_assert_groups(week_groups['groups'], expected_ranges, expected_record_count_list)
        
        self.assertGroupByWeekly(assert_groups)

    def test_groupby_invoices_start_friday(self):
        '''Test to assert that when start_day_of_week of ir.config_parameter is set to Friday, 
        the grouping should start at Friday when groupby='<any_date_field>:week'''
        
        self.env['ir.config_parameter'].sudo().set_param('idk_weekly_report.start_day_of_week', self.day_of_week.get('Friday'))
        
        week_groups = self.env['account.move'].web_read_group(domain=[['move_type', '=', 'out_invoice']], fields=self.fields, groupby=['invoice_date:week'])
        
        self.assertTrue(len(week_groups['groups']) == 2, "Two groups should have been created")
        
        expected_ranges = ['from 2023-10-27 to 2023-11-03', 'from 2023-11-03 to 2023-11-10']
        expected_record_count_list = [1, 2]
        
        assert_groups = self.create_assert_groups(week_groups['groups'], expected_ranges, expected_record_count_list)
        
        self.assertGroupByWeekly(assert_groups)
    
    def create_assert_groups(self, groups, expected_ranges, expected_record_count_list):
        return [
            {
                'actual_range': "from %s to %s" % (group['__range']['invoice_date']['from'], group['__range']['invoice_date']['to']),
                'actual_record_count': group['invoice_date_count'],
                'expected_range': expected_range,
                'expected_record_count': expected_record_count
            }
            for group, expected_range, expected_record_count in zip(groups, expected_ranges, expected_record_count_list)
        ]
          
    def assertGroupByWeekly(self, assert_groups):
        for group in assert_groups:
            
            self.assertEqual(group['actual_record_count'], group['expected_record_count'])
            self.assertEqual(group['actual_range'], group['expected_range'])
