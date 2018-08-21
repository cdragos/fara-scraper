from scrapy import Field, Item


class ActiveForeignPrincipal(Item):

    url = Field()
    country = Field()
    state = Field()
    reg_num = Field()
    address = Field()
    foreign_principal = Field()
    foreign_principal_reg_date = Field()
    registrant = Field()
    reg_date = Field()
    exhibit_url = Field()
