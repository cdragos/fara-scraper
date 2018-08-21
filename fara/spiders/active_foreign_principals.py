from scrapy import FormRequest, Request, Spider

from fara.items import ActiveForeignPrincipal
from fara.loaders import ActiveForeignPrincipalLoader


class ActiveForeignPrincipals(Spider):

    name = 'active-foreign-principals'
    allowed_domains = ['efile.fara.gov']
    start_urls = ['https://efile.fara.gov/pls/apex/f?p=185:130:0::NO:RP,130:P130_DATERANGE:N']

    _next_page = 'https://efile.fara.gov/pls/apex/wwv_flow.show'

    def parse(self, response):
        rows = response.css('#apexir_DATA_PANEL .apexir_WORKSHEET_DATA tr')
        country = None
        for row in rows:
            if row.css('.apexir_REPEAT_HEADING'):
                country = row.css('::text').extract()[1]
                continue

            columns = row.css('td')
            if len(columns) > 1:
                item = self.load_item(response, country, columns)
                request = Request(item['url'], callback=self.parse_exhibit_url,
                                  dont_filter=True)
                request.meta['item'] = item
                yield request

        next_page = response.css(
            '#apexir_DATA_PANEL .pagination img[title=Next]').xpath('..')
        if next_page:
            yield self.next_page(response, next_page)

    def load_item(self, response, country, columns):
        loader = ActiveForeignPrincipalLoader(
            ActiveForeignPrincipal(), columns)
        loader.context['response'] = response
        loader.add_css('url', '[headers*=LINK] a::attr(href)')
        loader.add_value('country', country)
        loader.add_css('state', '[headers*=STATE]::text')
        loader.add_css('reg_num', '[headers*=REG_NUMBER]::text')
        loader.add_css('address', '[headers*=ADDRESS_1]::text')
        loader.add_css('foreign_principal', '[headers*=FP_NAME]::text')
        loader.add_css(
            'foreign_principal_reg_date', '[headers*=FP_REG_DATE]::text')
        loader.add_css('registrant', '[headers*=REGISTRANT_NAME]::text')
        loader.add_css('reg_date', '[headers*=REG_DATE]::text')
        return loader.load_item()

    def parse_exhibit_url(self, response):
        item = response.meta['item']
        exhibit_url = response.css(
            '.apexir_WORKSHEET_DATA td[headers=DOCLINK] a::attr(href)'
        ).extract_first()
        item['exhibit_url'] = exhibit_url
        yield item

    def next_page(self, response, next_page):
        formdata = response.meta.get('pagination_form_data', {
            'p_request': 'APXWGT',
            'p_widget_action': 'PAGE',
            'p_widget_mod': 'ACTION',
            'p_widget_name': 'worksheet',
            'p_widget_num_return': '15',
            'p_flow_id': response.css('#pFlowId::attr(value)').extract_first(),
            'p_flow_step_id': response.css('#pFlowStepId::attr(value)').extract_first(),
            'p_instance': response.css('#pInstance::attr(value)').extract_first(),
            'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').extract_first(),
            'x02': response.css('#apexir_REPORT_ID::attr(value)').extract_first(),
        })
        href = next_page.css('::attr(href)').extract_first()
        # next page link has a javascript function
        # ex : javascript:gReport.navigate.paginate('pgR_min_row=16max_rows=15rows_fetched=15')
        formdata['p_widget_action_mod'] = href[href.find("('") + 2:href.find("')")]
        request = FormRequest(
            self._next_page, method='POST', formdata=formdata,
            callback=self.parse)
        request.meta['pagination_form_data'] = formdata
        return request
