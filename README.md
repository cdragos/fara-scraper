# Active Foreign Principals

This is a scrapper based on Scrapy that extracts all active foreign principals from Foreign Agents Registration (FARA)

## Requirements

* Python 3.x
* Virtualenv

## Installation
(make sure you are in the project folder)

1. Create a virtualenv with python3

    ```virtualenv venv -p python3```

2. Activate the virtualenv

    ```. venv/bin/activate```

3. Install python requirements with pip

    ```pip install -r requirements.txt```


## Running the scraper

    scrapy crawl active-foreign-principals

The scraper will output the results in `fara.json` in a format that looks like this:

```json
    {
      "url": "https:\/\/efile.fara.gov\/pls\/apex\/f?p=185:200:0::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6344,Exhibit%20AB,*ST.%20MARTIN",
      "country": "ST MARTIN",
      "state": "FL",
      "reg_num": "6344",
      "address": "808 Brickell Key Drive #606",
      "foreign_principal": "Tromp, Emsley",
      "foreign_principal_reg_date": "2018-04-24T00:00:00",
      "registrant": "Livingston Group, LLC",
      "reg_date": "2018-04-24T00:00:00",
      "exhibit_url": null
    }
```

## Running the tests

    python -m unittest fara.tests.test_active_foreign_principals
