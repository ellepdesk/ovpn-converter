import argparse
import re
from os import mkdir


def parse_arguments():
    parser = argparse.ArgumentParser(description='Expand an ovpn file with embedded keys to a directory')
    parser.add_argument('inputfile', metavar='ovpn_file', type=str,
                        help='ovpn file with embedded keys')
    parser.add_argument('outputdir', metavar='output_dir', type=str,
                        help='directory to write the output files to')
    parser.add_argument('--ovpn_file', metavar='ovpn', type=str,
                        help='name of ovpn output file', default=None)
    parser.add_argument('--ca_file', metavar='ca', type=str,
                        help='name of certificate authority file', default='ca.crt')
    parser.add_argument('--cert_file', metavar='cert', type=str,
                        help='name of certificate file', default='client.crt')
    parser.add_argument('--key_file', metavar='key', type=str,
                        help='name of key file', default='client.key')
    args = parser.parse_args()
    if not args.ovpn_file:
        args.ovpn_file = args.inputfile
    args.outputdir = args.outputdir+'/'
    return args


def main(args):
    f = open(args.inputfile, 'r')
    data = f.read()

    regex = '<ca>\n((.*\n)*)</ca>'
    ca = re.search(regex, data, re.MULTILINE).group(1)
    data = re.sub(regex, 'ca '+args.ca_file, data, re.MULTILINE)

    regex = '<cert>\n((.*\n)*)</cert>'
    cert = re.search(regex, data, re.MULTILINE).group(1)
    data = re.sub(regex, 'cert '+args.cert_file, data, re.MULTILINE)

    regex = '<key>\n((.*\n)*)</key>'
    key = re.search(regex, data, re.MULTILINE).group(1)
    data = re.sub(regex, 'key '+args.key_file, data, re.MULTILINE)

    try:
        mkdir(args.outputdir)
    except FileExistsError:
        pass

    f = open(args.outputdir+args.ca_file, 'w')
    f.write(ca)

    f = open(args.outputdir+args.cert_file, 'w')
    f.write(cert)

    f = open(args.outputdir+args.key_file, 'w')
    f.write(key)

    f = open(args.outputdir+args.ovpn_file, 'w')
    f.write(data)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
