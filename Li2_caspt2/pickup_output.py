import sys

def get_casscf_energy_internal(filename):
	with open(filename, 'r') as infile:
		for line in reversed(infile.readlines()):
			try:
				if line.split()[2]=='*':
					return float(line.split()[3])
			except IndexError:
				pass
	return None

def get_caspt2_energy(filename, shift=0.0):
	with open(filename, 'r') as infile:
		for line in reversed(infile.readlines()):
			try:
				if line.split()[0]=='*':
					return float(shift)+float(line.split()[6])
			except IndexError:
				pass
	return None

def get_neci_rdm_energy(filename):
	for line in open(filename):
		if "*TOTAL ENERGY* CALCULATED" in line:
			return float(line.split()[-1])

if __name__=='__main__':
	if sys.argv[1]=='get_casscf_energy_internal':
		print get_casscf_energy_internal(sys.argv[2])
	#elif sys.argv[1]=='get_caspt2_energy_internal':
	#	print get_caspt2_energy_internal(sys.argv[2])
	elif sys.argv[1]=='get_caspt2_energy':
		try:
			print get_caspt2_energy(sys.argv[2], sys.argv[3])
		except IndexError:
			print get_caspt2_energy(sys.argv[2])
	elif sys.argv[1]=='get_neci_rdm_energy':
		print get_neci_rdm_energy(sys.argv[2])

