# -*- coding:utf-8 -*-
from src.log_processor import FlowLogProcessor

processor = FlowLogProcessor('lookup_table.csv', 'flow_logs.txt', 'output.txt')

processor.process()
