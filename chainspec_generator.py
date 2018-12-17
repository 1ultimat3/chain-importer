import os

from importer.chainspec import ChainSpecGenerator
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Blockchain state importer')
    parser.add_argument('--template-spec', '-t', help='Path to the template genesis spec', required=True)
    parser.add_argument('--state', '-s', help='Source state exported from Parity', required=True)
    parser.add_argument('--output', '-o', help='Output path of the resulting genesis', required=True)
    parser.add_argument('--whitelist', '-w', help='Path to Whitelist file, which contains addresses'
                                                  ' to be included from the exported state')
    args = parser.parse_args()
    chainspec = ChainSpecGenerator(
        target_spec_path=os.path.expanduser(args.template_spec),
        state_export=os.path.expanduser(args.state)
    )
    if args.whitelist:
        with open(args.whitelist, 'r') as f:
            whitelist = [_addr.strip() for _addr in f.readlines()]
    else:
        whitelist = []
    chainspec.generate_spec(
        output_path=os.path.expanduser(args.output),
        whitelist=whitelist
    )
