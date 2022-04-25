main: test.c
	gcc -g \
	test.c ADF_cons2prim/src/init.c ADF_cons2prim/src/calculate.c \
	-L../../JacobianAD -Wl,-rpath=../../JacobianAD -lJacobianAD \
	-L../../ArrayAD -Wl,-rpath=../../ArrayAD -lArrayAD \
	-L../../SensAD -Wl,-rpath=../../SensAD -lSensAD \
	-lm
