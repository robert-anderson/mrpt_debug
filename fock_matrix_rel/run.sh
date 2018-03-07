#!/bin/bash

root_dir=$(pwd)/$(dirname $0)

bagel_exe='/home/mmm0043/Programs/bagel_master/obj/src/BAGEL'
neci_exe='/home/mmm0043/Programs/neci_hbrdm/build_debug/bin/kneci'

nclosed=0
nact=5

read -r -d '' mol_chunk << EOM
        {
            "geometry": [
                {
                    "xyz": [
                        -0.0,
                        -0.0,
                        -0.0
                    ],
                    "atom": "Li"
                },
                {
                    "xyz": [
                        1.0,
                        -0.0,
                        -0.0
                    ],
                    "atom": "Li"
                }
            ],
            "df_basis": "/home/mmm0043/Programs/bagel_master/src/basis/cc-pvdz.json",
            "basis": "/home/mmm0043/Programs/bagel_master/src/basis/cc-pvdz.json",
            "angstrom": true,
            "title": "molecule"
        },
EOM



#########################################################

# first, clear out working directory
for i in $(ls | grep -v 'run.sh'); do rm $i; done


# do DHF and dump integrals
cat > bagel.json <<- EOM
{
    "bagel" : [
		$mol_chunk
        {
            "title" : "dhf",
            "gaunt" : true,
            "breit" : true,
            "robust" : true,
            "thresh" : 1.0e-10,
            "maxiter" : 1000
        },
        {
          "title" : "zfci",
          "only_ints" : true,
          "ncore" : $nclosed,
          "norb" :  $nact,
          "frozen" : false,
          "state" : [1]
        }
	]
}
EOM
$bagel_exe bagel.json > bagel.initial.out

nelec=$(grep -oE "NELEC= [0-9]+" FCIDUMP | grep -oE [0-9]+)

# run NECI for 2-RDM
cat > neci.inp <<- EOM
title

system read noorder
symignoreenergies
freeformat
electrons $nelec

sym 0 0 0 0
nonuniformrandexcits PICK-VIRT-UNIFORM
nobrillouintheorem
endsys

calc
methods
method vertex fcimc
endmethods
fci-init

tau 0.01
memoryfacpart 2.0
memoryfacspawn 20.0
totalwalkers 5000
nmcyc 4000
seed 17
startsinglepart 100
diagshift 0.100000
rdmsamplingiters 200000
shiftdamp 0.05
truncinitiator
addtoinitiator 3
allrealcoeff
realspawncutoff 0.4
jump-shift
proje-changeref 1.5
stepsshift 10
maxwalkerbloom 3
load-balance-blocks off
endcalc

integral
freeze 0 0
endint

logging
binarypops
exactrdm
explicitallrdm

calcrdmonfly 3 1000 5000
    
printonerdm
print-one-rdm-occupations
endlog
end
EOM

$neci_exe neci.inp > neci.initial.out
rm RDMEstimates INITIATORStats FCIMCStats 2RDM_POPSFILE
mv 2RDM.1 fciqmc_0_0.rdm2
mv 1RDM.1 fciqmc_0_0.rdm1

rm bagel.json
# do zcasscf with no optimisation
cat > bagel.json <<- EOM
{
    "bagel": [
		$mol_chunk
        {
            "nclosed": $nclosed,
            "title": "zcasscf",
            "algorithm":"noopt",
            "nact": $nact,
            "external_rdm" : "fciqmc",
		    "state" : [1],
            "maxiter": 1
        },
		{
            "title" : "zfci",
            "only_ints" : true,
            "ncore": $nclosed,
            "norb": $nact,
            "frozen" : false,
            "state" : [1]
		}
    ]
}
EOM

$bagel_exe bagel.json > bagel.casci.out

# rotating to semi-canonical orbitals
cat > bagel.json <<- EOM
{
    "bagel": [
		$mol_chunk
        {
            "nclosed": $nclosed,
            "title": "zcasscf",
            "canonical":true,
            "nact": $nact,
            "external_rdm" : "fciqmc",
		    "state" : [1],
            "maxiter": 1
        },
		{
            "title" : "zfci",
            "only_ints" : true,
            "ncore": $nclosed,
            "norb": $nact,
            "frozen" : false,
            "state" : [1]
		}
    ]
}
EOM

$bagel_exe bagel.json > bagel.canonical.out

# dumping FOCKMAT in semi-canonical orbital basis
cat > bagel.json <<- EOM


{
    "bagel": [
		$mol_chunk
        {
            "nclosed": $nclosed,
            "title": "zcasscf",
            "algorithm":"noopt",
            "nact": $nact,
            "external_rdm" : "fciqmc",
		    "state" : [1],
            "maxiter": 1
        },
        {
            "title" : "relsmith",
            "method" : "caspt2",
            "external_rdm" : "noref",
            "frozen" : false
        }
    ]
}
EOM

$bagel_exe bagel.json > bagel.fockdump.out
cp FOCKMAT FOCKMAT_BAGEL
python $root_dir/../scripts/reformat_fockmat.py



