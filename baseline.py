from datetime import datetime
import pandas as pd
import pathpy as pp
from tqdm import tqdm
from time import time
import argparse
import os
import pickle

LOGS_DIR = 'logs'
DATASET_PATH = "./reddit_hyperlink_network.tsv"


# Generate a timestamp for the log file
timestamp = datetime.now().strftime("%Y%m%d%H%M")

def load_edgelist():
    def date_to_timestamp(date_string: str):
        return int(datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp())

    reddit = pd.read_csv(DATASET_PATH, delimiter='\t')

    data = data = reddit[['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT', 'TIMESTAMP']]
    data.columns = ['source', 'target', 'timestamp']

    return [(row['source'], row['target'], date_to_timestamp(row['timestamp'])) for _, row in data.iterrows()]


def path_count(paths, k):
  count = 0
  for k in range(1, k + 1):
      count += sum([v.sum() for v in paths.paths[k].values()])
  return count

def create_models_backup_directory():
    # Create a 'models' directory if it doesn't exist
    models_directory = 'models'
    if not os.path.exists(models_directory):
        os.makedirs(models_directory)
    return models_directory

def create_run_models_directory(delta, K):
    models_dir = create_models_backup_directory()
    # Create a folder to store pickle files
    run_dir_name = f"{models_dir}/baseline_{timestamp}_delta{delta}_K{K}"
    if not os.path.exists(run_dir_name):
        os.makedirs(run_dir_name)
    return run_dir_name

def get_total_causal_paths(temporal_network, delta, K):
    run_dir = create_run_models_directory(delta, K)

    start = time()
    # Calculate the number of causal paths
    paths = pp.path_extraction.temporal_paths.paths_from_temporal_network_dag(temporal_network, delta=delta)

    output = f"Number of causal paths: {paths}\n"
    print(output)
    
    count = path_count(paths, K)
    end = time()
    runtime = end - start
    
    output += f"Total causal paths count: {count}\n"
    output += f"Runtime: {runtime} seconds\n"
    
    # Log the program output to a file with a unique name
    log_file_name = f"{LOGS_DIR}/baseline_{timestamp}_delta{delta}_K{K}.log"
    with open(log_file_name, 'w') as log_file:
        log_file.write(output)
    
    # # Save the temporal network as a pickle file
    # temporal_network_file = f"{run_dir}/temporal_network.pkl"
    # with open(temporal_network_file, 'wb') as temporal_network_pickle:
    #     pickle.dump(temporal_network, temporal_network_pickle)

    # Save the paths as a pickle file
    paths_file = f"{run_dir}/paths.pkl"
    with open(paths_file, 'wb') as paths_pickle:
        pickle.dump(paths, paths_pickle)
    
    return count, runtime

def create_temporal_network(edge_list):
    # Create a temporal network
    t = pp.TemporalNetwork()
    for edge in tqdm(edge_list):
        s, d, ts = edge
        t.add_edge(s, d, ts)
    return t

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

    edge_list = load_edgelist()
    t = create_temporal_network(edge_list)

    # Create the 'logs' directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    count, runtime = get_total_causal_paths(t, delta, args.K)