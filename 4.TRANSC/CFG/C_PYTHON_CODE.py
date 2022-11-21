#!/usr/bin/env python3

import os

def get_csv_filename():
	HOME_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1])
	return HOME_PATH
