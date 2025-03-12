import torch
import torchvision
import pyarrow.parquet
import pandas
import scraper
import converter

# Acces table from parquet file
table = pyarrow.parquet.read_table('logos.snappy.parquet')

data = table.to_pandas()
for domain in data['domain']:
    favicon_url = scraper.retrieve_icon(domain)

converter.convert_to_png('./data')
converter.resize_images('./data')

