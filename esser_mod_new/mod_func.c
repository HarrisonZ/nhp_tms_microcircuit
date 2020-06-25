#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _Excitatory_esser_reg();
extern void _Inhibitory_esser_reg();
extern void _NMDA_esser_reg();
extern void _esser_mech_reg();
extern void _exp2syn_esser_reg();
extern void _vecevent_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," Excitatory_esser.mod");
fprintf(stderr," Inhibitory_esser.mod");
fprintf(stderr," NMDA_esser.mod");
fprintf(stderr," esser_mech.mod");
fprintf(stderr," exp2syn_esser.mod");
fprintf(stderr," vecevent.mod");
fprintf(stderr, "\n");
    }
_Excitatory_esser_reg();
_Inhibitory_esser_reg();
_NMDA_esser_reg();
_esser_mech_reg();
_exp2syn_esser_reg();
_vecevent_reg();
}
