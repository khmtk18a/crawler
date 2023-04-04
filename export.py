from tasks import app
from celery.result import AsyncResult
import argparse
import csv

def export(r: AsyncResult, writer: csv.DictWriter):
    if r.successful():
        writer.writerow(r.result)
    child: AsyncResult
    for child in r.children or []:
        export(child, writer)

parser = argparse.ArgumentParser('Export result to CSV')
parser.add_argument('id', type=str)

args = parser.parse_args()
r: AsyncResult = app.AsyncResult(args.id)

with open('./music.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['id', 'name', 'artist', 'url'])
    writer.writeheader()
    export(r, writer)
