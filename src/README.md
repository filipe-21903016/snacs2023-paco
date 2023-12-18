# README.md

## Running the Causal Paths Script and PaCo Algorithm

This repository contains two scripts: `baseline.py` for calculating causal paths using pathpy and `main.py` for executing the PaCo algorithm. Follow the instructions below to run the PaCo algorithm.

1. Run the PaCo algorithm with the following command:

```bash
python main.py -d <max_time_difference> [--hour/--minute] -K <max_path_length>
```

#### Parameters

- `-d` or `--delta`: Maximum time difference between consecutive interactions. Must be specified.
- `--hour`: If present, the time difference will be interpreted in hours.
- `--minute`: If present, the time difference will be interpreted in minutes.
  - If neither `--hour` nor `--minute` is specified, `delta` is interpreted in seconds.
- `-K`: Maximum path length. Must be specified.

### Example

```bash
python main.py -d 10 --minute -K 3
```

This example sets the maximum time difference to 10 minutes and the maximum path length to 3.


## Running the Baseline Script


1. Run the script with the following command:

```bash
python baseline.py -d <max_time_difference> [--hour/--minute] -K <max_path_length>
```

#### Parameters

- `-d` or `--delta`: Maximum time difference between consecutive interactions. Must be specified.
- `--hour`: If present, the time difference will be interpreted in hours.
- `--minute`: If present, the time difference will be interpreted in minutes.
  - If neither `--hour` nor `--minute` is specified, `delta` is interpreted in seconds.
- `-K`: Maximum path length. Must be specified.

### Example

```bash
python baseline.py -d 10 --minute -K 3
```

This example sets the maximum time difference to 10 minutes and the maximum path length to 3.
