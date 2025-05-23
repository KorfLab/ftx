import argparse


def validate(arg):
	pass


def gfftokgf(arg):
	pass

def kgftogff(arg):
	pass

def kgftojson(arg):
	pass

def kgftosql(arg):
	pass

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	sub = parser.add_subparsers(required=True, help='sub-commands')

	## validate
	s1 = sub.add_parser('validate', help='validate a KGF file')
	s1.add_argument('--kgf', metavar='<file.kgf>', required=True)
	s1.set_defaults(func=validate)

	## gfftokgf
	s2 = sub.add_parser('gfftokgf', help='convert from gff to kgf')
	s2.set_defaults(func=gfftokgf)

	## kgftogff
	s3 = sub.add_parser('kgftogff', help='convert from kgf to gff')
	s3.set_defaults(func=kgftogff)

	## kgftojson
	s4 = sub.add_parser('kgftojson', help='convert from kgf to json')
	s4.set_defaults(func=kgftojson)

	## kgftosql
	s4 = sub.add_parser('kgftojson', help='convert from kgf to sql')
	s4.set_defaults(func=kgftosql)

	## execute sub-command
	arg = parser.parse_args()
	arg.func(arg)
