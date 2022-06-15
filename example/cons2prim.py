import pyADF as AD

def cons2prim(
    inputs_AD = { 'Uc':[4] },
    inputs = { 'R':[], 'gamma':[] }
):
    rho   = inputs_AD['Uc'][0]
    rhoU  = inputs_AD['Uc'][1:3]
    rhoE  = inputs_AD['Uc'][3]
    gamma = inputs['gamma']
    R     = inputs['R']
    
    U = [rhoU[0]/rho, rhoU[1]/rho]
    #p = (gamma-1.0) * (rhoE - 0.5 * rho * (U[0]**2 + U[1]**2))
    p = AD.processExternalFunction('calcP', args=[gamma, rhoE, rho, U[0], U[1]])
    H = (rhoE+p)/rho

    outputs = {}
    if rho > 1.0 : outputs_AD = { 'Up' : [p, U[0], U[1], H] }
    else: outputs_AD = { 'Up' : [rho, U[0], U[1], p] }

    return outputs, outputs_AD

if __name__=='__main__':
    AD.compile(cons2prim, disableDerivs=True)
