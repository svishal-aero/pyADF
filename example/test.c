#include <stdio.h>
#include <stdlib.h>
#include "ADF_cons2prim/ADF_cons2prim.h"

#define DEPINDEX__Up__Uc 0

int main()
{
    double R = 1.0;
    double gamma = 1.4;

    //==================================================================
    // Create variables
    //==================================================================

    ADF_cons2prim cons2prim;
    ADF_cons2prim__init(&cons2prim);
    
    ArrayAD Uc;
    ArrayAD__init(&Uc);
    Uc.shape[0] = 1;
    Uc.shape[1] = 4;
    ArrayAD__create(&Uc);

    ArrayAD Up;
    ArrayAD__init(&Up);
    Up.shape[0] = 1;
    Up.shape[1] = 4;
    ArrayAD__init(&Up);
    Up.nDeps = 1;
    ArrayAD__initDeps(&Up);
    Up.deps[0].arrayAD = &Uc;
    Up.deps[0].hasNaturalConn = 1;
    Up.deps[0].indicesIsACopy = 0;
    Up.deps[0].sensArrIsACopy = 0;
    ArrayAD__finalizeDeps(&Up);

    JacobianAD J;
    JacobianAD__init(&J);
    JacobianAD__create(&J, &Up, &Uc);

    //==================================================================
    // Set input values
    //==================================================================

    Uc.data[0] = 0.5;
    Uc.data[1] = 0.1;
    Uc.data[2] = 0.2;
    Uc.data[3] = 1.0 / (1.4 - 1.0) + 0.05;

    //==================================================================
    // Calculate outputs and sensitivities
    //==================================================================

    cons2prim.Uc         = Uc.data + 0;
    cons2prim.R          = &R;
    cons2prim.gamma      = &gamma;
    cons2prim.Up         = Up.data + 0;
    cons2prim.d_Up__d_Uc = Up.deps[DEPINDEX__Up__Uc].sensArr
                         + 0 * Up.eSize * Uc.eSize;

    ADF_cons2prim__calculate(&cons2prim);

    JacobianAD__calculate(&J);

    //==================================================================
    // Print outputs
    //==================================================================

    for(int i=0; i<4; i++)
    {
        printf("%le\n", Up.data[i]);
    }
    printf("All ok\n");

    int jacind=0;
    for(int i=0; i<J.M; i++)
    {
        for(int j=J.offsets[i]; j<J.offsets[i+1]; j++)
        {
            for(int ii=0; ii<J.m; ii++)
            {
                for(int jj=0; jj<J.n; jj++)
                {
                    printf("Row=(%d,%d) Column=(%d,%d) Entry=%+le\n",
                            i, ii, j, jj, J.entries[jacind++]);
                }
            }
        }
    }

    //==================================================================
    // Delete stuff
    //==================================================================

    JacobianAD__delete(&J);
    ArrayAD__delete(&Up);
    ArrayAD__delete(&Uc);
}
