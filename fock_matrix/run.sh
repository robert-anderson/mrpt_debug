#!/bin/bash

root_dir=$(pwd)/$(dirname $0)

bagel_exe='/home/mmm0043/Programs/bagel_master/obj/src/BAGEL'
neci_exe='/home/mmm0043/Programs/neci_hbrdm/build_debug/bin/neci'

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


# do HF and dump integrals
cat > bagel.json <<- EOM
{
    "bagel": [
		$mol_chunk
        {
            "title": "hf"
        },
        {
            "title"  : "casscf",
            "external_rdm" : "noref",
            "state" : [1],
            "maxiter" : 0,
            "canonical" : true,
            "nact"       : $nclosed,
            "nclosed"    : $nact 
        },
        {
            "only_ints": true,
            "title": "fci",
            "frozen": false,
            "ncore": $nclosed,
            "norb": $nact,
            "state": [
                1
            ]
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

spin-restrict 0
sym 0 0 0 0
nonuniformrandexcits 4IND-WEIGHTED
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
    
write-spin-free-rdm
printonerdm
print-one-rdm-occupations
endlog
end
EOM

rm bagel.json
# do casscf
cat > bagel.json <<- EOM
{
    "bagel": [
		$mol_chunk
        {
            "nstate": [
                1
            ],
            "nclosed": $nclosed,
            "title": "casscf",
            "maxiter_micro": 100,
            "nact": $nact,
            "external_rdm" : "fciqmc",
            "canonical" : true,
            "maxiter": 1
        },
        {
            "only_ints": true,
            "nstate": 1,
            "title": "fci",
            "frozen": false,
            "ncore": $nclosed,
            "norb": $nact
        }
    ]
}
EOM

MAX_ITER=10
for i in $(seq 1 $MAX_ITER); do
    $neci_exe neci.inp > neci.initial.out
    rm RDMEstimates INITIATORStats FCIMCStats 2RDM_POPSFILE
    mv spinfree_TwoRDM.1 fciqmc_0_0.rdm2
    mv spinfree_OneRDM.1 fciqmc_0_0.rdm1
    $bagel_exe bagel.json > "bagel.casscf."$i".out"
    grep "TOTAL ENERGY" neci.initial.out
done

# rotating to semi-canonical orbitals
cat > bagel.json <<- EOM
{
    "bagel": [
		$mol_chunk
        {
            "nstate": [
                1
            ],
            "nclosed": $nclosed,
            "title": "casscf",
            "maxiter_micro": 100,
            "canonical":true,
            "nact": $nact,
            "external_rdm" : "fciqmc",
            "maxiter": 1
        },
        {
            "only_ints": true,
            "nstate": 1,
            "title": "fci",
            "frozen": false,
            "ncore": $nclosed,
            "norb": $nact
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
            "nstate": [
                1
            ],
            "nclosed": $nclosed,
            "title": "casscf",
            "maxiter_micro": 100,
            "algorithm" : "noopt",
            "nact": $nact,
            "external_rdm" : "fciqmc",
            "maxiter": 1
        },
        {
            "title" : "smith",
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


