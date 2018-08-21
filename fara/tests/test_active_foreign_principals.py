from urllib.parse import parse_qs
import unittest

from fara.spiders import ActiveForeignPrincipals
from fara.items import ActiveForeignPrincipal
from fara.tests import fake_response


class ActiveForeignPrincipalsTests(unittest.TestCase):

    START_URL = 'https://efile.fara.gov/pls/apex/'

    def setUp(self):
        self.spider = ActiveForeignPrincipals()

    def test_parse(self):
        resp = fake_response(
            'responses/active_foreign_principals_first_page.html',
            self.START_URL)
        results = list(self.spider.parse(resp))
        # 15 records and a next page request
        self.assertEqual(len(results), 16)

        records, next_page_req = results[:15], results[15:]
        self.assertEqual(
            records[0].url,
            'https://efile.fara.gov/pls/apex/f?p=185:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6344,Exhibit%20AB,*ST.%20MARTIN')
        self.assertEqual(
            records[1].url,
            'https://efile.fara.gov/pls/apex/f?p=185:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6065,Exhibit%20AB,AFGHANISTAN')

        self.assertEqual(next_page_req[0].url, self.spider._next_page)
        self.assertEqual(parse_qs(next_page_req[0].body), {
            b'p_request': [b'APXWGT'],
            b'p_widget_action': [b'PAGE'],
            b'p_widget_mod': [b'ACTION'],
            b'p_widget_name': [b'worksheet'],
            b'p_widget_num_return': [b'15'],
            b'p_flow_id': [b'185'],
            b'p_flow_step_id': [b'130'],
            b'p_instance': [b'30861316723764'],
            b'x01': [b'555215554758934859'],
            b'x02': [b'555216849652934863'],
            b'p_widget_action_mod': [b'pgR_min_row=16max_rows=15rows_fetched=15']
        })

    def test_parse_last_page(self):
        resp = fake_response(
            'responses/active_foreign_principals_last_page.html',
            self.START_URL)
        results = list(self.spider.parse(resp))
        self.assertEqual(len(results), 3)
        self.assertEqual(
            results[-1].url,
            'https://efile.fara.gov/pls/apex/f?p=185:200:30861316723764::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6552,Exhibit%20AB,YEMEN')

    def test_parse_with_exhibit_url(self):
        resp = fake_response(
            'responses/active_foreign_principals_first_page.html',
            self.START_URL)
        results = list(self.spider.parse(resp))
        # 15 records and a next page request
        self.assertEqual(len(results), 16)

        exhibit_resp = fake_response(
            'responses/exhibit_url.html', self.START_URL, meta=results[0].meta)
        exhibit_url_results = list(self.spider.parse_exhibit_url(exhibit_resp))
        self.assertEqual(len(exhibit_url_results), 1)
        self.assertEqual(exhibit_url_results[0], {
            'address': '808 Brickell Key Drive #606',
            'country': 'ST MARTIN',
            'exhibit_url': 'http://www.fara.gov/docs/2987-Exhibit-AB-19781201-D0EE2403.pdf',
            'foreign_principal': 'Tromp, Emsley',
            'foreign_principal_reg_date': '2018-04-24T00:00:00',
            'reg_date': '2018-04-24T00:00:00',
            'reg_num': '6344',
            'registrant': 'Livingston Group, LLC',
            'state': 'FL',
            'url': 'https://efile.fara.gov/pls/apex/f?p=185:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6344,Exhibit%20AB,*ST.%20MARTIN'
        })


if __name__ == '__main__':
    unittest.main()
