# vivino-scraper
Python command line tool to scrape data from vivino.com.
The [vivino explore API](https://www.vivino.com/api/explore/explore) at is used. 

Scraped data is saved in pickle format.
If --download_labels argument is given, all wine labels are downloaded under labels folder as well.

## Installation
`pip install -r requirements.txt`

## Usage
`python scrape.py --filter filter.json --download_labels`

usage: scrape.py [-h] [--filter_json FILTER_JSON] [--download_labels]

optional arguments:

  -h, --help                    show this help message and exit

  --filter_json FILTER_JSON     the path to filter json file

  --download_labels             downloads wine labels if specified

## Filters
The following are the valid filters for vivino's explore API:
- country_code - i.e. fr
- country_codes[] - i.e. fr can be provided multiple times
- currency_code - i.e. chf
- grape_filter - i.e. varietal
- min_rating - i.e. 4
- order_by - i.e. ratings_count
- order - i.e. ASC
- page - i.e. 1
- price_range_max - i.e. 500
- price_range_min - i.e. 20
- wine_type_ids[] - i.e. 1 can be provided multiple times
- vc_only - i.e. true
- per_page - i.e. 100
