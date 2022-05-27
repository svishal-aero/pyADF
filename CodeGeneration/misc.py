import os
from .FormattedBuffer import FormattedBuffer

pyad_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def writeStructFile(buffer: FormattedBuffer, functionName, shapes, includeLines, max_size):
    buffer.write('#pragma once')
    buffer.write('')
    for includeLine in includeLines: buffer.write(includeLine)
    buffer.write('')
    buffer.write('#pragma pack(1)')
    buffer.write('typedef struct '+functionName)
    buffer.openScope()
    buffer.write('double ___phi[%d];' % (max_size))
    buffer.write('double ___psi[%d];' % (max_size))
    for name in shapes['inputs_AD' ].keys(): buffer.write('double *'+name+';')
    for name in shapes['inputs'    ].keys(): buffer.write('double *'+name+';')
    for name in shapes['outputs'   ].keys(): buffer.write('double *'+name+';')
    for name in shapes['outputs_AD'].keys(): buffer.write('double *'+name+';')
    for oName in shapes['outputs_AD'].keys():
        for iName in shapes['inputs_AD'].keys():
            buffer.write('double *d_'+oName+'__d_'+iName+';')
    buffer.closeScope()
    buffer.write(functionName+';')
    buffer.write('#pragma pack()')
    buffer.write('')
    buffer.write('void '+functionName+'__init('+functionName+' *self);')
    buffer.write('void '+functionName+'__calculate('+functionName+' *self);')

def writeOtherFiles(buffer: FormattedBuffer, functionName, vars):
    buffer.write('#include <stdlib.h>')
    buffer.write('#include "../'+functionName+'.h"')
    buffer.write('')
    buffer.write('void '+functionName+'__init('+functionName+' *self'+')')
    buffer.openScope()
    for name in vars['inputs_AD'].keys():  buffer.write('self->'+name+' = NULL;')
    for name in vars['inputs'].keys():     buffer.write('self->'+name+' = NULL;')
    for name in vars['outputs_AD'].keys(): buffer.write('self->'+name+' = NULL;')
    for name in vars['outputs'].keys():    buffer.write('self->'+name+' = NULL;')
    for oName in vars['outputs_AD'].keys():
        for iName in vars['inputs_AD'].keys():
            buffer.write('self->d_'+oName+'__d_'+iName+' = NULL;')
    buffer.closeScope()
