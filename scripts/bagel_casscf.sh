#!/bin/bash

root_dir=$(pwd)/$(dirname $0)

config_name='Li2'
trel=false
save_rdms=false
save_ints=false
bagel_init_hf_only=false
do_internal=true
do_pt2=true
use_caspt2_intermediate=false
tol=1.0E-10
maxiters=30
bagel_exe='/home/mmm0043/Programs/bagel_master/obj/src/BAGEL'
neci_bin='/home/mmm0043/Programs/neci_hbrdm/build_debug/bin'

if [ "$trel" = true ]; then
	neci_exe=$neci_bin'/kneci'
else
	neci_exe=$neci_bin'/neci'
fi

if [ "$do_internal" = true ]; then
	if [ "$trel" = true ]; then
		python $root_dir/write_bagel_inps.py 'casscf_bagel_inp_internal' $config_name
		$bagel_exe casscf_bagel_inp_internal.json > casscf_bagel_inp_internal.json.out
		e_casscf=$(python $root_dir/pickup_output.py 'get_casscf_energy_internal' 'casscf_bagel_inp_internal.json.out')
		printf '\nBAGEL internal CASSCF energy: %12.10f\n' $e_casscf
		if [ "$do_pt2" = true ]; then
			python $root_dir/write_bagel_inps.py 'caspt2_bagel_inp_internal' $config_name
			$bagel_exe caspt2_bagel_inp_internal.json > caspt2_bagel_inp_internal.json.out
			e_casscf=$(python $root_dir/pickup_output.py 'get_casscf_energy_internal' 'caspt2_bagel_inp_internal.json.out')
			e_caspt2=$(python $root_dir/pickup_output.py 'get_caspt2_energy' 'caspt2_bagel_inp_internal.json.out')
			echo 'BAGEL internal CASSCF energy (from CASPT2 calc): ' $e_casscf
			echo 'BAGEL internal CASPT2 energy: ' $e_caspt2
		fi
	else
		python $root_dir/write_bagel_inps.py 'casscf_bagel_inp_non_rel_internal' $config_name
		$bagel_exe casscf_bagel_inp_non_rel_internal.json > casscf_bagel_inp_non_rel_internal.json.out
		e_casscf=$(python $root_dir/pickup_output.py 'get_casscf_energy_internal' 'casscf_bagel_inp_non_rel_internal.json.out')
		printf '\nBAGEL internal CASSCF energy: %12.10f\n' $e_casscf
		if [ "$do_pt2" = true ]; then
			python $root_dir/write_bagel_inps.py 'caspt2_bagel_inp_non_rel_internal' $config_name
			$bagel_exe caspt2_bagel_inp_non_rel_internal.json > caspt2_bagel_inp_non_rel_internal.json.out
			e_casscf=$(python $root_dir/pickup_output.py 'get_casscf_energy_internal' 'caspt2_bagel_inp_non_rel_internal.json.out')
			e_caspt2=$(python $root_dir/pickup_output.py 'get_caspt2_energy' 'caspt2_bagel_inp_non_rel_internal.json.out')
			echo 'BAGEL internal CASSCF energy (from CASPT2 calc): ' $e_casscf
			echo 'BAGEL internal CASPT2 energy: ' $e_caspt2
		fi
	fi
fi

printf '\nInitialising CASSCF reference\n'
if [ "$trel" = true ]; then
	python $root_dir/write_bagel_inps.py 'init_bagel_inp' $config_name $bagel_init_hf_only
    $bagel_exe init_bagel_inp.json > init_bagel_inp.json.out
else
	python $root_dir/write_bagel_inps.py 'init_bagel_inp_non_rel' $config_name $bagel_init_hf_only
    $bagel_exe init_bagel_inp_non_rel.json > init_bagel_inp_non_rel.json.out
fi

# write BAGEL casscf input file for iterations
if [ "$trel" = true ]; then
	python $root_dir/write_bagel_inps.py 'casscf_bagel_inp' $config_name
else
	python $root_dir/write_bagel_inps.py 'casscf_bagel_inp_non_rel' $config_name
fi
# write NECI RDM input file for casscf iterations
if [ "$trel" = true ]; then
	python $root_dir/write_neci_inps.py 'casscf' $config_name > input.neci
else
	python $root_dir/write_neci_inps.py 'casscf_non_rel' $config_name > input.neci
fi

printf '\nStarting CASSCF loop\n'
printf '\n    iter      E_2RDM      difference\n'
for it in $(seq 1 $maxiters); do
	$neci_exe input.neci > out.neci.$it
	e_rdm=$(python $root_dir/pickup_output.py 'get_neci_rdm_energy' 'out.neci.'$it)
	if [ "$it" = 1 ]; then
		printf '   %3d    %12.10f\n' $it $e_rdm
	else
		diff=$( echo $e_rdm - $last_e_rdm | bc)
		printf '   %3d    %12.10f  %12.10f\n' $it $e_rdm $diff
		if [ $( python $root_dir/check_tol.py $e_rdm $last_e_rdm $tol ) = 1 ]; then
			printf '\n Convergence reached.\n'
			break
		fi
	fi
	last_e_rdm=$e_rdm

	if [ "$trel" = true ]; then
		if [ "$save_rdms" = true ]; then
			cp 1RDM.1 'fciqmc_0_0_iter_'$it'.rdm1'
			cp 2RDM.1 'fciqmc_0_0_iter_'$it'.rdm2'
		fi
		mv 2RDM.1 fciqmc_0_0.rdm2
		mv 1RDM.1 fciqmc_0_0.rdm1
	else
		if [ "$save_rdms" = true ]; then
			cp spinfree_OneRDM.1 'fciqmc_0_0_iter_'$it'.rdm1'
			cp spinfree_TwoRDM.1 'fciqmc_0_0_iter_'$it'.rdm2'
		fi
		mv spinfree_TwoRDM.1 fciqmc_0_0.rdm2
		mv spinfree_OneRDM.1 fciqmc_0_0.rdm1
	fi
	if [ "$save_ints" = true ]; then
		mv FCIDUMP FCIDUMP_iter_$it
	fi
	if [ "$trel" = true ]; then
		$bagel_exe casscf_bagel_inp.json > out.bagel.$it
	else
		$bagel_exe casscf_bagel_inp_non_rel.json > out.bagel.$it
	fi
    cp casscf.log casscf.log.$it

done

if [ "$do_pt2" = false ]; then
	exit 0;
fi
printf '\n Computing high body RDMs with NECI.\n'

# write BAGEL casscf input file for CASPT2
if [ "$trel" = true ]; then
	python $root_dir/write_bagel_inps.py 'caspt2_bagel_inp' $config_name
else
	python $root_dir/write_bagel_inps.py 'caspt2_dump_fockmat' $config_name
	$bagel_exe caspt2_dump_fockmat.json > caspt2_dump_fockmat.json.out
	python $root_dir/reformat_fockmat.py
	python $root_dir/write_bagel_inps.py 'caspt2_bagel_inp_non_rel' $config_name
fi
# write NECI RDM input file for higher body RDMs
if [ "$trel" = true ]; then
	if [ "$use_caspt2_intermediate" = true ]; then
		python $root_dir/write_neci_inps.py 'caspt2_aux' $config_name > input.highrdms.neci
	else
		python $root_dir/write_neci_inps.py 'caspt2' $config_name > input.highrdms.neci
	fi
else
	if [ "$use_caspt2_intermediate" = true ]; then
		python $root_dir/write_neci_inps.py 'caspt2_aux_non_rel' $config_name > input.highrdms.neci
	else
		python $root_dir/write_neci_inps.py 'caspt2_non_rel' $config_name > input.highrdms.neci
	fi
fi
$neci_exe input.highrdms.neci > out.neci.highrdms
if [ "$trel" = true ]; then
	if [ "$save_rdms" = true ]; then
		cp 1RDM.1 fciqmc_0_0_iter_pt2.rdm1
		cp 2RDM.1 fciqmc_0_0_iter_pt2.rdm2
		cp 3RDM.1 fciqmc_0_0_iter_pt2.rdm3
		if [ "$use_caspt2_intermediate" = true ]; then
			cp CASPT2_AUX.1 fciqmc_0_0_iter_pt2.rdm4f
		else
			cp 4RDM.1 fciqmc_0_0_iter_pt2.rdm4
		fi
	fi
	mv 1RDM.1 fciqmc_0_0.rdm1
	mv 2RDM.1 fciqmc_0_0.rdm2
	mv 3RDM.1 fciqmc_0_0.rdm3
	if [ "$use_caspt2_intermediate" = true ]; then
		mv CASPT2_AUX.1 fciqmc_0_0.rdm4f
	else
		mv 4RDM.1 fciqmc_0_0.rdm4
		python $root_dir/explicit_4f.py
	fi
else
	if [ "$save_rdms" = true ]; then
		cp spinfree_OneRDM.1 fciqmc_0_0_iter_pt2.rdm1
		cp spinfree_TwoRDM.1 fciqmc_0_0_iter_pt2.rdm2
		cp spinfree_ThreeRDM.1 fciqmc_0_0_iter_pt2.rdm3
		if [ "$use_caspt2_intermediate" = true ]; then
			cp spinfree_CASPT2_AUX.1 fciqmc_0_0_iter_pt2.rdm4f
		else
			cp spinfree_FourRDM.1 fciqmc_0_0_iter_pt2.rdm4f
		fi
	fi
	mv spinfree_OneRDM.1 fciqmc_0_0.rdm1
	mv spinfree_TwoRDM.1 fciqmc_0_0.rdm2
	mv spinfree_ThreeRDM.1 fciqmc_0_0.rdm3
	if [ "$use_caspt2_intermediate" = true ]; then
		mv spinfree_CASPT2_AUX.1 fciqmc_0_0.rdm4f
	else
		mv spinfree_FourRDM.1 fciqmc_0_0.rdm4
		python $root_dir/explicit_4f.py
	fi
fi

if [ "$trel" = true ]; then
	$bagel_exe caspt2_bagel_inp.json > out.bagel.pt2
else
	$bagel_exe caspt2_bagel_inp_non_rel.json > out.bagel.pt2
fi

e_caspt2=$(python $root_dir/pickup_output.py 'get_caspt2_energy' 'out.bagel.pt2' $e_rdm)
printf '\nCASPT2 energy from NECI RDMs: %12.10f\n' $e_caspt2
