
def casscf(system):
	return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

spin-restrict 0
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
'''.format(d=system)

def casscf_non_rel(system):
	return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

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
'''.format(d=system)
    
def caspt2(system):
	if system['nelecas']==2:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

spin-restrict 0
sym 0 0 0 0
nonuniformrandexcits PICK-VIRT-UNIFORM
(nonuniformrandexcits 4IND-WEIGHTED
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
'''.format(d=system)
	else:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

spin-restrict 0
sym 0 0 0 0
nonuniformrandexcits PICK-VIRT-UNIFORM
(nonuniformrandexcits 4IND-WEIGHTED
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

four-body-rdm
calc-three-from-four-rdm
    
printonerdm
print-one-rdm-occupations
endlog
end
'''.format(d=system)


def caspt2_aux(system):
	if system['nelecas']==2:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

spin-restrict 0
sym 0 0 0 0
nonuniformrandexcits PICK-VIRT-UNIFORM
(nonuniformrandexcits 4IND-WEIGHTED
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
'''.format(d=system)
	else:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

spin-restrict 0
sym 0 0 0 0
nonuniformrandexcits PICK-VIRT-UNIFORM
(nonuniformrandexcits 4IND-WEIGHTED
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

four-body-rdm
caspt2-intermediates
    
printonerdm
print-one-rdm-occupations
endlog
end
'''.format(d=system)


def caspt2_non_rel(system):
	if system['nelecas']==2:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

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
'''.format(d=system)
	else:
		return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

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
    
four-body-rdm
calc-three-from-four-rdm
    
write-spin-free-rdm
printonerdm
print-one-rdm-occupations
endlog
end
'''.format(d=system)






def caspt2_aux_non_rel(system):
	return '''
title

system read noorder
symignoreenergies
freeformat
electrons {d[nelecas]}

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
    
four-body-rdm
caspt2-intermediates
    
write-spin-free-rdm
printonerdm
print-one-rdm-occupations
endlog
end
'''.format(d=system)
