bagel_basis = "/home/mmm0043/Programs/bagel_master/src/basis/{}.json"
configs ={ 
	'water':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz-jkfit"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "O",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]},
				{ "atom" : "H",  "xyz" : [    0.584,     -0.775,     0.0]},
				{ "atom" : "H",  "xyz" : [    0.584,     0.775,     0.0]}
			]
		},
		'ncore':3,
		'ncas':4,
		'nelecas':4
	},
	'Be':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "Be",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':0,
		'ncas':5,
		'nelecas':4
	},
	'Li2':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "Li",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]},
				{ "atom" : "Li",  "xyz" : [    1.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':0,
		'ncas':5,
		'nelecas':6
	},
	'Be2':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "Be",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]},
				{ "atom" : "Be",  "xyz" : [    1.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':2,
		'ncas':4,
		'nelecas':6
	},
	'Be_core':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "Be",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':1,
		'ncas':4,
		'nelecas':2
	},
	'C':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz-jkfit"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "C",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':0,
		'ncas':5,
		'nelecas':6
	},
	'He':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvtz"),
			"df_basis" : bagel_basis.format("cc-pvtz"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "He",  "xyz" : [   -0.00000,     -0.000000,     -0.000000]}
			]
		},
		'ncore':0,
		'ncas':2,
		'nelecas':2
	},
	'H2':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz-jkfit"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "H",  "xyz" : [    0.0,     0.0,     0.0]},
				{ "atom" : "H",  "xyz" : [    1.0,     0.0,     0.0]}
			]
		},
		'ncore':0,
		'ncas':2,
		'nelecas':2
	},
	'N2':
	{
		'mol_spec':
		{
			"title" : "molecule",
			"basis" : bagel_basis.format("cc-pvdz"),
			"df_basis" : bagel_basis.format("cc-pvdz-jkfit"),
			"angstrom" : True,
			"geometry" : [
				{ "atom" : "N",  "xyz" : [    0.0,     0.0,     0.0]},
				{ "atom" : "N",  "xyz" : [    1.4,     0.0,     0.0]}
			]
		},
		'ncore':4,
		'ncas':6,
		'nelecas':6
	},
}

mydhf={
	"title" : "dhf",
	"gaunt" : True,
	"breit" : True,
	"robust" : True,
	"thresh" : 1.0e-10,
	"maxiter" : 1000
	}

myhf={
	"title" : "hf",
	"robust" : True,
	"thresh" : 1.0e-10,
	"maxiter" : 1000
	}

def init_bagel_inp(config, dhf_only=True):
	if dhf_only:
		return \
		{ "bagel" : [
			config['mol_spec'],
			mydhf,
			{
			  "title" : "zfci",
			  "only_ints" : True,
			  "ncore" : config['ncore'],
			  "norb" :  config['ncas'],
			  "frozen" : False,
			  "state" : [1]
			}
		]}
	else:
		return \
		{ "bagel" : [ 
			config['mol_spec'],
			{
			  "title" : "dhf",
			  "gaunt" : True,
			  "breit" : True,
			},
			{
			  "title"  : "zcasscf",
			  "external_rdm" : "noref",
			  "gaunt" : True,
			  "breit" : True,
			  "state" : [1],
			  "maxiter" : 0,
			  "nact"       : config['ncas'],
			  "nclosed"    : config['ncore'] 
			},
			{
			  "title" : "zfci",
			  "state" : [1],
			  "only_ints" : True,
			  "ncore" : config['ncore'],
			  "norb" :  config['ncas']
			}
		]}

def casscf_bagel_inp(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		{
		  "title" : "zcasscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 1,
		  "external_rdm" : "fciqmc",
		  "state" : [1]
		},
		{
		  "title" : "zfci",
		  "only_ints" : True,
		  "ncore" : config['ncore'],
		  "norb" : config['ncas'],
		  "frozen" : False,
		  "state" : [1]
		}
	]}

def casscf_bagel_inp_internal(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		mydhf,
		{
		  "title" : "zcasscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 100,
		  "state" : [1]
		},
	]}

# to read in higher body rdms for PT2 correction
def caspt2_bagel_inp(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		{
		  "title" : "zcasscf",
		  "algorithm" : "noopt",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "external_rdm" : "fciqmc",
		  "state" : [1] 
		},

		{
		  "title" : "relsmith",
		  "method" : "caspt2",
		  "external_rdm" : "fciqmc",
		  "frozen" : False
		}
	]}

def caspt2_bagel_inp_internal(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		mydhf,
		{
		  "title" : "zcasscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 500,
		  "state" : [1]
		},
		{
		  "title" : "relsmith",
		  "method" : "caspt2",
		  "frozen" : False
		}
	]}






def init_bagel_inp_non_rel(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		myhf,
		{
		  "title" : "fci",
		  "only_ints" : True,
		  "ncore" : config['ncore'],
		  "norb" : config['ncas'],
		  "frozen" : False,
		  "nstate" : 1
		}
	]}


def init_bagel_inp_non_rel(config, hf_only=True):
	if hf_only:
		return \
		{ "bagel" : [
			config['mol_spec'],
			myhf,
			{
			  "title" : "fci",
			  "only_ints" : True,
			  "ncore" : config['ncore'],
			  "norb" :  config['ncas'],
			  "frozen" : False,
			  "state" : [1]
			}
		]}
	else:
		return \
		{ "bagel" : [ 
			config['mol_spec'],
			{
			  "title" : "hf"
			},
			{
			  "title"  : "casscf",
			  "external_rdm" : "noref",
			  "state" : [1],
			  "maxiter" : 0,
			  "nact"       : config['ncas'],
			  "nclosed"    : config['ncore'] 
			},
			{
			  "title" : "fci",
			  "state" : [1],
			  "only_ints" : True,
			  "ncore" : config['ncore'],
			  "norb" :  config['ncas'],
		  	  "frozen" : False,
			}
		]}


def casscf_bagel_inp_non_rel(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		{
		  "title" : "casscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 1,
		  "external_rdm" : "fciqmc",
		  "nstate" : [1],
		  "maxiter_micro" : 100
		},
		{
		  "title" : "fci",
		  "only_ints" : True,
		  "ncore" : config['ncore'],
		  "norb" : config['ncas'],
		  "frozen" : False,
		  "nstate" : 1
		}
	]}


def casscf_bagel_inp_non_rel_internal(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		myhf,
		{
		  "title" : "casscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 100,
		  "nstate" : 1
		}
	]}

def caspt2_dump_fockmat(config):
	return \
	{
    "bagel": [
		config['mol_spec'],
		 {
		  "title" : "casscf",
		  "algorithm" : "noopt",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "external_rdm" : "fciqmc",
		  "nstate" : 1 
		},

		{
		  "title" : "smith",
		  "method" : "caspt2",
		  "external_rdm" : "noref",
		  "frozen" : False
		}
	]}


# to read in higher body rdms for PT2 correction
def caspt2_bagel_inp_non_rel(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		 {
		  "title" : "casscf",
		  "algorithm" : "noopt",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "external_rdm" : "fciqmc",
		  "nstate" : 1 
		},

		{
		  "title" : "smith",
		  "method" : "caspt2",
		  "external_rdm" : "fciqmc",
		  "frozen" : False
		}
	]}

def caspt2_bagel_inp_non_rel_internal(config):
	return \
	{ "bagel" : [
		config['mol_spec'],
		myhf,
		{
		  "title" : "casscf",
		  "nclosed" : config['ncore'],
		  "nact" : config['ncas'],
		  "maxiter" : 500,
		  "nstate" : 1
		},
		{
		  "title" : "smith",
		  "method" : "caspt2",
		  "frozen" : False
		}
	]}

