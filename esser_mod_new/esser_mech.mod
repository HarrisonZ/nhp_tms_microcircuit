TITLE esser_mech.mod 

NEURON {
    SUFFIX esser_mech
    POINT_PROCESS esser_mech
    USEION na READ ena WRITE ina
    USEION k READ ek WRITE ik
    RANGE gNa_leak, gK_leak, theta_eq, tau_theta, tau_spike, tau_m, gspike, C, tspike, vrefrac, ifake, vaux
    NONSPECIFIC_CURRENT ispike
}
UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S) = (siemens)
}

PARAMETER {
    gNa_leak = 0.14 (S/cm2)
    gK_leak = 1.0 (S/cm2)
    C = 0.85 
    theta_eq = -53 (mV)
    tau_theta = 2 (ms)
    tau_spike = 1.75 
    tau_m = 15
    tspike = 2 (ms)
    vap = 30 (mV)
}
ASSIGNED {
    v (mV)
    ena (mV)
    ek (mV)

    ina (mA/cm2)
    ik (mA/cm2)
    ispike (mA/cm2)
    gspike (S/cm2)
    ifake (mA/cm2)
    vaux (mV)
}

STATE {
    theta (mV)
}

BREAKPOINT {
	SOLVE states METHOD cnexp
    ina = gNa_leak*(v-ena)/tau_m     : Sodium-like leak current
    ik = gK_leak*(v-ek)/tau_m    : Potassium-like leak current
    ispike = gspike*(v-ek)/tau_spike 
    ifake = 0
    vaux = v - theta
}

INITIAL {
    net_send(0,1)
    theta = theta_eq
    gspike = 0
    ena = 30 (mV)
    ek = -90 (mV)
    v = -75.263 (mV)
}

DERIVATIVE states {
    theta' = (-(theta - theta_eq) + C*(v - theta_eq))/tau_theta  : threshold 
}

NET_RECEIVE (w) {
    if (flag == 1){
        WATCH (vaux > 0) 2
    }else if (flag == 2){
        net_event(t)
        gspike = 1 
        v = vap
        theta = vap 
        vaux = vap
        net_send(tspike,3)
    }else if (flag == 3){
        gspike = 0
        net_send(0,1)
    }
}

COMMENT

NET_RECEIVE (w) {
    if (flag == 1){
        WATCH (v > theta) 2
    }else if (flag == 2){
        t0 = t
        net_event(t)
        gspike = 1 
        v = vap
        theta = vap 
        if (t - t0 > tspike){
            net_send(0,3)
        } else {
            gspike = 1 
        }
    }else if (flag == 3){
        gspike = 0
        net_send(0,1)
    }
}
ENDCOMMENT
