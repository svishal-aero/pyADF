import os
import numpy as np
from .FormattedBuffer import FormattedBuffer

defDir = os.path.dirname(os.path.abspath(__file__))

def writeCalculateFile(buffer: FormattedBuffer, functionName, functionType, shapes, forwardBuffer, reverseBuffer):
    buffer.write('#include "../'+functionName+'.h"')
    buffer.write('#include "'+defDir+'/CHeaders/defineOps.h"')
    buffer.write('')
    buffer.write(functionName+' adf_'+functionName[4:]+';')
    buffer.write('')
    buffer.write('static void calculateDerivatives('+functionName+' *self);')
    buffer.write('static void updateDerivs('+functionName+' *self, int size);')
    buffer.write('static void setInputs('+functionName+' *self);')
    buffer.write('static void getOutputs('+functionName+' *self, int size);')
    calculate(buffer, functionName, forwardBuffer)
    calculateDerivatives(buffer, functionName, reverseBuffer)
    updateDerivs(buffer, functionName, shapes['inputs_AD'], shapes['outputs_AD'])
    setInputs(buffer, functionName, shapes['inputs_AD'], shapes['inputs'])
    getOutputs(buffer, functionName, functionType, shapes['outputs'], shapes['outputs_AD'])

def calculate(buffer: FormattedBuffer, functionName, forwardBuffer: FormattedBuffer):
    buffer.write('')
    buffer.write('void '+functionName+'__calculate')
    buffer.write('(')
    buffer.write('\t'+functionName+' *self')
    buffer.write(')')
    buffer.openScope()
    buffer.write('double *___psi = self->___psi;')
    buffer.write('double *___phi = self->___phi;')
    buffer.write('setInputs(self);')
    buffer.lines.append(forwardBuffer.getContents(indent=buffer.indent))
    buffer.closeScope()

def calculateDerivatives(buffer: FormattedBuffer, functionName, reverseBuffer: FormattedBuffer):
    buffer.write('')
    buffer.write('static void calculateDerivatives('+functionName+' *self)')
    buffer.openScope()
    buffer.write('double *___psi = self->___psi;')
    buffer.write('double *___phi = self->___phi;')
    buffer.lines.append(reverseBuffer.getContents(indent=buffer.indent))
    buffer.closeScope()
    buffer.write('')
    buffer.write('#include "'+defDir+'/CHeaders/undefOps.h"')
    buffer.write('')

def updateDerivs(buffer: FormattedBuffer, functionName, inputs_AD, outputs_AD):
    buffer.write('static void updateDerivs('+functionName+' *self, int size)')
    buffer.openScope()
    buffer.write('int iOutput, iSens, iInput;')
    iNameList = list(inputs_AD.keys())
    iShapeList = list(inputs_AD.values())
    oNameList = list(outputs_AD.keys())[::-1]
    oShapeList = list(outputs_AD.values())[::-1]
    buffer.write('iOutput = size-1;')
    for oName, oShape in zip(oNameList, oShapeList):
        buffer.write('for(int j=%d; j>=0; j--)' % (int(np.prod(oShape))-1) )
        buffer.openScope()
        buffer.write('for(int iVar=0; iVar<size; iVar++) self->___psi[iVar] = 0.0;')
        buffer.write('self->___psi[iOutput--] = 1.0;')
        buffer.write('calculateDerivatives(self);')
        buffer.write('iInput = 0;')
        for iName, iShape in zip(iNameList, iShapeList):
            buffer.write('for(int i=0; i<%d; i++)' % (int(np.prod(iShape))))
            buffer.openScope()
            buffer.write('self->d_'+oName+'__d_'+iName+'[j*%d+i] = self->___psi[iInput++];' % (int(np.prod(iShape))))
            buffer.closeScope()
        buffer.closeScope()
    buffer.closeScope()
    buffer.write('')

def setInputs(buffer: FormattedBuffer, functionName, inputs_AD, inputs):
    buffer.write('static void setInputs('+functionName+' *self)')
    buffer.openScope()
    buffer.write('int iInput = 0;')
    for name, shape in inputs_AD.items():
        buffer.write('for(int i=0; i<%d; i++)' % (int(np.prod(shape))) )
        buffer.openScope()
        buffer.write('self->___phi[iInput++] = self->'+name+'[i];')
        buffer.closeScope()
    for name, shape in inputs.items():
        buffer.write('for(int i=0; i<%d; i++)' % (int(np.prod(shape))) )
        buffer.openScope()
        buffer.write('self->___phi[iInput++] = self->'+name+'[i];')
        buffer.closeScope()
    buffer.closeScope()
    buffer.write('')

def getOutputs(buffer: FormattedBuffer, functionName, functionType, outputs, outputs_AD):
    buffer.write('static void getOutputs('+functionName+' *self, int size)')
    buffer.openScope()
    buffer.write('int iOutput = size-1;')
    nameList = list(outputs_AD.keys())[::-1]
    shapeList = list(outputs_AD.values())[::-1]
    for name, shape in zip(nameList, shapeList):
        buffer.write('for(int i=%d; i>=0; i--)' % (int(np.prod(shape))-1) )
        buffer.openScope()
        if functionType=='REPLACE':
            buffer.write('self->'+name+'[i] = self->___phi[iOutput--];')
        if functionType=='UPDATE':
            buffer.write('self->'+name+'[i] += self->___phi[iOutput--];')
        buffer.closeScope()
    nameList = list(outputs.keys())[::-1]
    shapeList = list(outputs.values())[::-1]
    for name, shape in zip(nameList, shapeList):
        buffer.write('for(int i=%d; i>=0; i--)' % (int(np.prod(shape))-1) )
        buffer.openScope()
        if functionType=='REPLACE':
            buffer.write('self->'+name+'[i] = self->___phi[iOutput--];')
        if functionType=='UPDATE':
            buffer.write('self->'+name+'[i] += self->___phi[iOutput--];')
        buffer.closeScope()
    buffer.closeScope()
    buffer.write('')
