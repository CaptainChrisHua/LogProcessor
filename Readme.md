# Flow Log Processor - Engineering Position at Illumio

This project is a solution to the Online Assessment for an Engineering position at Illumio. 

The Flow Log Processor is a Python tool designed to parse and tag network flow log data based on destination port (`dstport`) and protocol combinations. Each log entry is tagged according to a lookup table, and the output includes a summary of tag counts and port/protocol combinations.

## Project Dependencies

- Python 3.x
- `csv` and `collections` (part of the standard Python library)

## Setup and Installation

**Clone the Repository**:
```bash
git clone https://github.com/CaptainChrisHua/LogProcessor.git
```

**Prepare Required Files**:
- `lookup_table.csv`: A CSV file containing mappings for `dstport`, `protocol`, and `tag`. The file contents can be directly copied from the OA email. Format example:
  ```csv
  dstport,protocol,tag
  25,tcp,sv_P1
  443,tcp,sv_P2
  23,tcp,sv_P1
  110,tcp,email
    ```

- `flow_logs.txt`: A text file containing flow logs, where each line follows a specific format. The content can also be directly copied from the OA email. Example:
```text
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK
```


## Running the Project

**Run the Program**:
```bash
python main.py
```

## Output: 
The program will generate a summary file with:

```text
Tag Counts:
Tag,Count
Untagged,8
sv_P2,1
sv_P1,2
email,3

Port/Protocol Combination Counts:
Port,Protocol,Count
49153,tcp,1
49154,tcp,1
49155,tcp,1
```