import torch
import torchvision
import pyarrow.parquet
import pandas
import scraper as scraper

# Acces table from parquet file
table = pyarrow.parquet.read_table('logos.snappy.parquet')

data = table.to_pandas()
for domain in data['domain'].head(10):
    favicon_url = scraper.retrieve_icon(domain)
