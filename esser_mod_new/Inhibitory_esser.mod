COMMENT
Two state kinetic scheme synapse described by rise time tau1,
and decay time constant tau2. The normalized peak condunductance is 1.
Decay time MUST be greater than rise time.

The solution of A->G->bath with rate constants 1/tau1 and 1/tau2 is
 A = a*exp(-t/tau1) and
 G = a*tau2/(tau2-tau1)*(-exp(-t/tau1) + exp(-t/tau2))
	where tau1 < tau2

If tau2-tau1 is very small compared to tau1, this is an alphasynapse with time constant tau2.
If tau1/tau2 is very small, this is single exponential decay with time constant tau2.

The factor is evaluated in the initial block 
such that an event of weight 1 generates a
peak conductance of 1.

Because the solution is a sum of exponentials, the
coupled equations can be solved as a pair of independent equations
by the more efficient cnexp method.

ENDCOMMENT

NEURON {
	POINT_PROCESS Inh_esser
	RANGE tau1_GABAA, tau2_GABAA, e_GABAA, i_GABAA, tau_m, gpeak_GABAA, tau1_GABAB, tau2_GABAB, e_GABAB, i_GABAB, gpeak_GABAB
	NONSPECIFIC_CURRENT i
	RANGE g, gGABAA, gGABAB, i, wratio
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	tau1_GABAA = 0.1 (ms) <1e-9,1e9>
	tau2_GABAA = 10 (ms) <1e-9,1e9>
	tau_m = 15 (ms) <1e-9,1e9>
	e_GABAA=0	(mV)
	gpeak_GABAA = 0.1

	tau1_GABAB = 0.1 (ms) <1e-9,1e9>
	tau2_GABAB = 10 (ms) <1e-9,1e9>
	e_GABAB=0	(mV)
	gpeak_GABAB = 0.1
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
	i_GABAA
	i_GABAB
	gGABAA
	gGABAB
	wratio
	factor_GABAA
	factor_GABAB
}

STATE {
	A_GABAA (uS)
	B_GABAA (uS)
	A_GABAB (uS)
	B_GABAB (uS)
}

INITIAL {
	LOCAL tp_GABAA, tp_GABAB
	if (tau1_GABAA/tau2_GABAA > 0.9999) {
		tau1_GABAA = 0.9999*tau2_GABAA
	}
	if (tau1_GABAA/tau2_GABAA < 1e-9) {
		tau1_GABAA = tau2_GABAA*1e-9
	}
	A_GABAA = 0
	B_GABAA = 0
	tp_GABAA = (tau1_GABAA*tau2_GABAA)/(tau2_GABAA - tau1_GABAA) * log(tau2_GABAA/tau1_GABAA)
	factor_GABAA = -exp(-tp_GABAA/tau1_GABAA) + exp(-tp_GABAA/tau2_GABAA)
	factor_GABAA = 1/factor_GABAA

	if (tau1_GABAB/tau2_GABAB > 0.9999) {
		tau1_GABAB = 0.9999*tau2_GABAB
	}
	if (tau1_GABAB/tau2_GABAB < 1e-9) {
		tau1_GABAB = tau2_GABAB*1e-9
	}
	A_GABAB = 0
	B_GABAB = 0
	tp_GABAB = (tau1_GABAB*tau2_GABAB)/(tau2_GABAB - tau1_GABAB) * log(tau2_GABAB/tau1_GABAB)
	factor_GABAB = -exp(-tp_GABAB/tau1_GABAB) + exp(-tp_GABAB/tau2_GABAB)
	factor_GABAB = 1/factor_GABAB
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	gGABAA = B_GABAA - A_GABAA
	i_GABAA = gGABAA*(v - e_GABAA)/tau_m
	gGABAB = B_GABAB - A_GABAB
	i_GABAB = gGABAB*(v - e_GABAB)/tau_m
	i = i_GABAA + i_GABAB
}

DERIVATIVE state {
	A_GABAA' = -A_GABAA/tau1_GABAA
	B_GABAA' = -B_GABAA/tau2_GABAA
	A_GABAB' = -A_GABAB/tau1_GABAB
	B_GABAB' = -B_GABAB/tau2_GABAB
}

NET_RECEIVE(weight (uS)) {
	A_GABAA = A_GABAA + weight*factor_GABAA*gpeak_GABAA
	B_GABAA = B_GABAA + weight*factor_GABAA*gpeak_GABAA
	A_GABAB = A_GABAB + wratio*weight*factor_GABAB*gpeak_GABAB
	B_GABAB = B_GABAB + wratio*weight*factor_GABAB*gpeak_GABAB
}
