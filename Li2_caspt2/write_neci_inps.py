import sys
import neci_inps, bagel_inps

func_name = sys.argv[1]
config_name = sys.argv[2]

config = bagel_inps.configs[config_name]

if func_name=='casscf':
	string = neci_inps.casscf(config)

elif func_name=='casscf_non_rel':
	string = neci_inps.casscf_non_rel(config)

elif func_name=='caspt2':
	string = neci_inps.caspt2(config)

elif func_name=='caspt2_non_rel':
	string = neci_inps.caspt2_non_rel(config)

elif func_name=='caspt2_aux_non_rel':
	string = neci_inps.caspt2_aux_non_rel(config)
else:
	assert(0)

print string
