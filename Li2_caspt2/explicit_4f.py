import numpy as np
import itertools

rdm_filename = 'fciqmc_0_0.rdm4'
fock_filename = 'FOCKMAT'
aux_filename = 'fciqmc_0_0.rdm4f'

lines = None
with open(rdm_filename, 'r') as f:
	lines = f.readlines()
nbasis = 0
for line in lines:
	max_ind = max(map(int, line.split()[:8]))
	if max_ind>nbasis:
		nbasis = max_ind

rdm_array = np.zeros((nbasis,)*8)
for line in lines:
	inds = tuple(i-1 for i in map(int, line.split()[:8]))
	val = float(line.split()[-1])
	rdm_array[inds] = val

fock_array = np.zeros((nbasis,)*2)
lines = None
with open(fock_filename, 'r') as f:
	lines = f.readlines()
for line in lines:
	inds = tuple(i-1 for i in map(int, line.split()[1:]))
	val = float(line.split()[0])
	fock_array[inds] = val

aux_array = np.einsum('ijkpabcp,pp->ijkabc', rdm_array, fock_array)

with open(aux_filename, 'w') as f:
	for inds in itertools.product(range(nbasis), repeat=6):
		if abs(aux_array[inds])>1e-12:
			f.write((('{}  '*6)+'{:.20f}\n').format(*(tuple(i+1 for i in inds)+(aux_array[inds],))))


