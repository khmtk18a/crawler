from tasks import dfs_crawler
from celery.result import AsyncResult
import argparse

parser = argparse.ArgumentParser('Inject url to tasks')
parser.add_argument('url', type=str)
parser.add_argument('depth', type=int, default=1)

args = parser.parse_args()
r: AsyncResult = dfs_crawler.apply_async((args.url, args.depth))
print(r.task_id)
