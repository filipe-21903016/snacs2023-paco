import pandas as pd
from datetime import datetime
from paco import TimeStampedLinkList, paco
import argparse
import time


def load_edgelist():
    def date_to_timestamp(date_string: str):
        return int(datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp())

    reddit = pd.read_csv('reddit_hyperlink_network.tsv', delimiter='\t')
    # reddit = pd.read_csv('edges.tsv', delimiter='\t')

    data = data = reddit[['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT', 'TIMESTAMP']]
    data.columns = ['source', 'target', 'timestamp']

    return [(row['source'], row['target'], date_to_timestamp(row['timestamp'])) for _, row in data.iterrows()]
    # return [(row['source'], row['target'], row['timestamp']) for _, row in data.iterrows()]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Process command line arguments.")
    parser.add_argument(
        "-d", type=int, help="Maximum time difference", required=True)
    parser.add_argument(
        "--hour",dest='h' , help="Set time difference to hours", action='store_true')
    parser.add_argument(
        "--minute",dest='m',  help="Set time difference to minutes", action='store_true')
    parser.add_argument(
        "-K", type=int, help="Maximum path length", required=True)
    args = parser.parse_args()

    delta = args.d * (60 if args.m is True or args.h is True else 1) * (60 if args.h is True else 1) 

    print('Pre-processing data...')
    s = time.time()
    edge_list = load_edgelist()
    data = TimeStampedLinkList.from_edgelist(edge_list)

    e = time.time()
    load_time = e - s
    print(f'Processed data. ({round(load_time, 2)}s)')
    print('Counting causal paths...\n')
    s = time.time()
    C = paco(data, delta, args.K)
    e = time.time()
    runtime = e - s

    print(f'PaCo found {sum(C.values())} causal paths. ({round(runtime, 2)}s)')