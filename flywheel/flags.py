import argparse

parser = argparse.ArgumentParser(description='Flywheel')
parser.add_argument('--email', action='store_true', help='if set, will trigger email')
parser.add_argument('--debug', action='store_true', help='if set, will enable debug information')

global args
args = parser.parse_args()

def flags():
  return args