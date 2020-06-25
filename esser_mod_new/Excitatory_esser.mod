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
	POINT_PROCESS Exc_esser
	RANGE tau1_AMPA, tau2_AMPA, e_AMPA, iAMPA, tau_m, gpeak_AMPA, tau1_NMDA, tau2_NMDA, e_NMDA, iNMDA, gpeak_NMDA, i, Mg, a, b 
	NONSPECIFIC_CURRENT i
	RANGE g, gAMPA, gNMDA, wratio
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	: AMPA parameter
	tau1_AMPA = 0.5 (ms) <1e-9,1e9>
	tau2_AMPA = 2.4 (ms) <1e-9,1e9>
	tau_m = 1 (ms) <1e-9,1e9>
	e_AMPA=0	(mV)
	gpeak_AMPA = 0.1
	: NMDA parameter
	tau1_NMDA = 4 (ms) <1e-9,1e9>
	tau2_NMDA = 40 (ms) <1e-9,1e9>
	e_NMDA=0	(mV)
	gpeak_NMDA = 0.1
	Mg = 1
    a = 0.062 (/mV)
    b = 3.57
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
	iAMPA
	iNMDA
	gAMPA
	gNMDA
	wratio
	factor_AMPA
	factor_NMDA
}

STATE {
	A_AMPA (uS)
	B_AMPA (uS)
	A_NMDA (uS)
	B_NMDA (uS)
}

INITIAL {
	LOCAL tp_AMPA, tp_NMDA
	if (tau1_AMPA/tau2_AMPA > 0.9999) {
		tau1_AMPA = 0.9999*tau2_AMPA
	}
	if (tau1_AMPA/tau2_AMPA < 1e-9) {
		tau1_AMPA = tau2_AMPA*1e-9
	}
	A_AMPA = 0
	B_AMPA = 0
	tp_AMPA = (tau1_AMPA*tau2_AMPA)/(tau2_AMPA - tau1_AMPA) * log(tau2_AMPA/tau1_AMPA)
	factor_AMPA = -exp(-tp_AMPA/tau1_AMPA) + exp(-tp_AMPA/tau2_AMPA)
	factor_AMPA = 1/factor_AMPA

	if (tau1_NMDA/tau2_NMDA > 0.9999) {
		tau1_NMDA = 0.9999*tau2_NMDA
	}
	if (tau1_NMDA/tau2_NMDA < 1e-9) {
		tau1_NMDA = tau2_NMDA*1e-9
	}
	A_NMDA = 0
	B_NMDA = 0
	tp_NMDA = (tau1_NMDA*tau2_NMDA)/(tau2_NMDA - tau1_NMDA) * log(tau2_NMDA/tau1_NMDA)
	factor_NMDA= -exp(-tp_NMDA/tau1_NMDA) + exp(-tp_NMDA/tau2_NMDA)
	factor_NMDA = 1/factor_NMDA
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	gAMPA = B_AMPA - A_AMPA
	iAMPA = gAMPA*(v - e_AMPA)/tau_m
	gNMDA = B_NMDA - A_NMDA
	iNMDA = (gNMDA*(v - e_NMDA)*1/(1+exp(-a*v)*(Mg/b)))/tau_m
	i = iAMPA + iNMDA : sum up AMPA and NMDA current
}

DERIVATIVE state {
	A_AMPA' = -A_AMPA/tau1_AMPA
	B_AMPA' = -B_AMPA/tau2_AMPA
	A_NMDA' = -A_NMDA/tau1_NMDA
	B_NMDA' = -B_NMDA/tau2_NMDA
}

NET_RECEIVE(weight (uS)) {
	A_AMPA = A_AMPA + weight*factor_AMPA*gpeak_AMPA 
	B_AMPA = B_AMPA + weight*factor_AMPA*gpeak_AMPA 
	A_NMDA = A_NMDA + wratio*weight*factor_NMDA*gpeak_NMDA
	B_NMDA = B_NMDA + wratio*weight*factor_NMDA*gpeak_NMDA
}
