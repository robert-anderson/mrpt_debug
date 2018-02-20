
lines = None
with open('FOCKMAT', 'r') as f:
	lines = f.readlines()

with open('FOCKMAT', 'w') as f:
	i = 1
	for line in lines:
		j = 1
		for val in line.split():
			if j>=i:
				f.write('{}    {}    {}\n'.format(val, i, j))
			if j==len(lines):
				break
			j+=1
		i+=1
