#include <math.h>

#define CONST(zid,val) ___phi[zid] = val;
#define EQUAL(zid,xid) ___phi[zid] = ___phi[xid];

#define D_EQUAL(zid,xid) ___psi[xid] = ___psi[zid];

#define ADD(zid,xid,yid) ___phi[zid] = ___phi[xid]+___phi[yid];
#define SUB(zid,xid,yid) ___phi[zid] = ___phi[xid]-___phi[yid];
#define MUL(zid,xid,yid) ___phi[zid] = ___phi[xid]*___phi[yid];
#define DIV(zid,xid,yid) ___phi[zid] = ___phi[xid]/___phi[yid];
#define POW(zid,xid,yid) ___phi[zid] = pow(___phi[xid],___phi[yid]);
#define NEG(zid,xid)     ___phi[zid] = -___phi[xid];
#define EXP(zid,xid)     ___phi[zid] = exp(___phi[xid]);
#define LOG(zid,xid)     ___phi[zid] = log(___phi[xid]);
#define SIN(zid,xid)     ___phi[zid] = sin(___phi[xid]);
#define COS(zid,xid)     ___phi[zid] = cos(___phi[xid]);
#define TAN(zid,xid)     ___phi[zid] = tan(___phi[xid]);
#define FABS(zid,xid)    ___phi[zid] = fabs(___phi[xid]);
#define SQRT(zid,xid)    ___phi[zid] = sqrt(___phi[xid]);
#define SINH(zid,xid)    ___phi[zid] = sinh(___phi[xid]);
#define COSH(zid,xid)    ___phi[zid] = cosh(___phi[xid]);
#define TANH(zid,xid)    ___phi[zid] = tanh(___phi[xid]);

#define FMAX(zid,xid,yid) ___phi[zid] = (___phi[xid]>___phi[yid]) ? ___phi[xid] : ___phi[yid];
#define FMIN(zid,xid,yid) ___phi[zid] = (___phi[xid]<___phi[yid]) ? ___phi[xid] : ___phi[yid];

#define D_ADD(zid,xid,yid) ___psi[xid] += ___psi[zid];             ___psi[yid] += ___psi[zid];
#define D_SUB(zid,xid,yid) ___psi[xid] += ___psi[zid];             ___psi[yid] -= ___psi[zid];
#define D_MUL(zid,xid,yid) ___psi[xid] += ___psi[zid]*___phi[yid]; ___psi[yid] += ___psi[zid]*___phi[xid];
#define D_DIV(zid,xid,yid) ___psi[xid] += ___psi[zid]/___phi[yid]; ___psi[yid] -= ___psi[zid]*___phi[zid]/___phi[yid];
#define D_POW(zid,xid,yid) ___psi[xid] += ___psi[zid]*___phi[yid]*pow(___phi[xid], ___phi[yid]-1); \
                           ___psi[yid] += ___psi[zid]*___phi[zid]*log(fabs(___phi[xid]));
#define D_NEG(zid,xid)     ___psi[xid] -= ___psi[zid];
#define D_EXP(zid,xid)     ___psi[xid] += ___psi[zid]*___phi[zid];
#define D_LOG(zid,xid)     ___psi[xid] += ___psi[zid]/___phi[xid];
#define D_SIN(zid,xid)     ___psi[xid] += ___psi[zid]*cos(___phi[xid]);
#define D_COS(zid,xid)     ___psi[xid] -= ___psi[zid]*sin(___phi[xid]);
#define D_TAN(zid,xid)     ___psi[xid] += ___psi[zid]*(1.0+___phi[zid]*___phi[zid]);
#define D_FABS(zid,xid)    ___psi[xid] += ___psi[zid]*((___phi[xid]>=0)?1:-1);
#define D_SQRT(zid,xid)    ___psi[xid] += ___psi[zid]*0.5*pow(___phi[xid], -0.5);
#define D_SINH(zid,xid)    ___psi[xid] += ___psi[zid]*cosh(___phi[xid]);
#define D_COSH(zid,xid)    ___psi[xid] += ___psi[zid]*sinh(___phi[xid]);
#define D_TANH(zid,xid)    ___psi[xid] += ___psi[zid]*(1.0-___phi[zid]*___phi[zid]);

#define D_FMAX(zid,xid,yid) if(___phi[xid]>___phi[yid]) ___psi[xid] += ___psi[zid]; else ___psi[yid] += ___psi[zid];
#define D_FMIN(zid,xid,yid) if(___phi[xid]<___phi[yid]) ___psi[xid] += ___psi[zid]; else ___psi[yid] += ___psi[zid];