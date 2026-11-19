"""Command-line interface for ATLAS benchmark."""
import argparse
import json
from .beam import Beam, convergence_study

def main():
    parser = argparse.ArgumentParser(description='ATLAS cantilever convergence benchmark')
    parser.add_argument('--load', type=float, default=1000.0, help='Tip load in newtons')
    parser.add_argument('--length', type=float, default=1.0, help='Beam length in meters')
    parser.add_argument('--output', default='', help='Optional JSON output file')
    args = parser.parse_args()
    result = convergence_study(Beam(end_load=args.load, length=args.length))
    output = json.dumps(result, indent=2)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(output + '\n')
    print(output)

if __name__ == '__main__':
    main()
