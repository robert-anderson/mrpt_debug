import sys
import bagel_inps
import json

func_name = sys.argv[1]
config_name = sys.argv[2]
hf_only = True
try:
	hf_only = sys.argv[3]=='true'
except IndexError:
	pass

config = bagel_inps.configs[config_name]

if func_name=='caspt2_bagel_inp':
	json_dict = bagel_inps.caspt2_bagel_inp(config)

elif func_name=='caspt2_bagel_inp_internal':
	json_dict = bagel_inps.caspt2_bagel_inp_internal(config)

elif func_name=='caspt2_dump_fockmat':
	json_dict = bagel_inps.caspt2_dump_fockmat(config)

elif func_name=='caspt2_dump_fockmat_non_rel':
	json_dict = bagel_inps.caspt2_dump_fockmat_non_rel(config)

elif func_name=='caspt2_bagel_inp_non_rel':
	json_dict = bagel_inps.caspt2_bagel_inp_non_rel(config)

elif func_name=='caspt2_bagel_inp_non_rel_internal':
	json_dict = bagel_inps.caspt2_bagel_inp_non_rel_internal(config)

elif func_name=='casscf_bagel_inp':
	json_dict = bagel_inps.casscf_bagel_inp(config)

elif func_name=='casscf_bagel_inp_internal':
	json_dict = bagel_inps.casscf_bagel_inp_internal(config)

elif func_name=='casscf_bagel_inp_non_rel':
	json_dict = bagel_inps.casscf_bagel_inp_non_rel(config)

elif func_name=='casscf_bagel_inp_non_rel_internal':
	json_dict = bagel_inps.casscf_bagel_inp_non_rel_internal(config)

elif func_name=='init_bagel_inp':
	json_dict = bagel_inps.init_bagel_inp(config, hf_only)

elif func_name=='init_bagel_inp_non_rel':
	json_dict = bagel_inps.init_bagel_inp_non_rel(config, hf_only)
else:
	assert(0)

with open('{}.json'.format(sys.argv[1]), 'w') as outfile:
	json.dump(json_dict, outfile, sort_keys=False, indent=4, separators=(',', ': '))
