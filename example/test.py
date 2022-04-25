import ctypes as C
from ADF_cons2prim.ADF_cons2prim import ADF_cons2prim, VarAD, JacAD

Uc    = (VarAD*4)()
R     = C.c_double(1.0)
gamma = C.c_double(1.4)
Up    = (VarAD*4)()

cons2prim = ADF_cons2prim()
cons2prim.setVars(Uc, R, gamma, Up)
cons2prim.setup()

jac = JacAD()
jac.create(4, 4, Uc, Up)

Uc[0].data = 0.5
Uc[1].data = 0.1
Uc[2].data = 0.2
Uc[3].data = 1.0 / (1.4 - 1.0) + 0.05
cons2prim.calculate()
for i in range(4): print(Up[i].data)

jac.calculate()
for i in range(jac.nRows):
    for j in range(jac.offsets[i], jac.offsets[i+1]):
        print(i, jac.colIds[j], jac.elems[j])

for i in range(4): Uc[i].delete()
for i in range(4): Up[i].delete()
jac.delete()