# -*- coding:utf-8 -*-
import csv
from collections import defaultdict


class FlowLogProcessor:
    def __init__(self, lookup_file, flow_log_file, output_file):
        """
        Initialize the processor with file paths.
        :param lookup_file: Path to the lookup table CSV file.
        :param flow_log_file: Path to the flow log file.
        :param output_file: Path to the output file.
        """
        self.lookup_file = lookup_file
        self.flow_log_file = flow_log_file
        self.output_file = output_file
        self.lookup_table = self.load_lookup_table()

    def load_lookup_table(self):
        """
        Load lookup table from a CSV file. If empty, create a default header.
        :return: Dictionary mapping (dstport, protocol) to tags.
        """
        lookup_table = defaultdict(list)
        try:
            with open(self.lookup_file, 'r+', encoding='ascii', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                if headers is None:  # Write default header if file is empty
                    writer = csv.writer(file)
                    writer.writerow(['dstport', 'protocol', 'tag'])
                    return lookup_table
                for row in reader:
                    if len(row) == 3:
                        dstport, protocol, tag = row
                        lookup_table[(int(dstport), protocol.lower())].append(tag)
        except FileNotFoundError:
            print(f"Error: File {self.lookup_file} not found.")

        return lookup_table

    def parse_flow_logs(self):
        """
        Parse flow logs and extract dstport and protocol fields.
        :return: List of (dstport, protocol) tuples.
        """
        flow_logs = []
        with open(self.flow_log_file, 'r', encoding='ascii') as file:
            for line in file:
                fields = line.strip().split()
                if len(fields) >= 13:
                    dstport = int(fields[6])
                    protocol = "tcp" if fields[7] == '6' else "udp" if fields[7] == '17' else "icmp"
                    flow_logs.append((dstport, protocol))
        return flow_logs

    def tag_flow_logs(self):
        """
        Apply tags to flow logs based on lookup table.
        :return: (tag counts, port/protocol counts).
        """
        flow_logs = self.parse_flow_logs()
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        for dstport, protocol in flow_logs:
            tags = self.lookup_table.get((dstport, protocol), ['Untagged'])
            for tag in tags:
                tag_counts[tag] += 1
            port_protocol_counts[(dstport, protocol)] += 1

        return tag_counts, port_protocol_counts

    def write_output(self, tag_counts, port_protocol_counts):
        """
        Write tag and port/protocol counts to an output file.

        :param tag_counts: Tag frequency dictionary.
        :param port_protocol_counts: Port/protocol frequency dictionary.
        """
        with open(self.output_file, 'w', encoding='ascii') as file:
            file.write("Tag Counts:\nTag,Count\n")
            for tag, count in tag_counts.items():
                file.write(f"{tag},{count}\n")

            file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_counts.items():
                file.write(f"{port},{protocol},{count}\n")

    def process(self):
        """
        Main processing function to tag flow logs and output results.
        """
        tag_counts, port_protocol_counts = self.tag_flow_logs()
        self.write_output(tag_counts, port_protocol_counts)
        print("Processing complete. Results written to output file.")
