import os
from .FormattedBuffer import FormattedBuffer

pyad_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def writeStructFile(buffer: FormattedBuffer, functionName, shapes, max_size):
    buffer.write('#pragma once')
    buffer.write('#pragma pack(1)')
    buffer.write('')
    buffer.write('#include "'+pyad_dir+'/ArrayAD/ArrayAD.h"')
    buffer.write('#include "'+pyad_dir+'/JacobianAD/JacobianAD.h"')
    buffer.write('')
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
    buffer.write('')
    buffer.write('void '+functionName+'__init('+functionName+' *self);')
    buffer.write('void '+functionName+'__calculate('+functionName+' *self);')

def writeOtherFiles(dirName, functionName, vars):
    with open(dirName+'/src/init.c', 'w') as f:
        f.write('#include <stdlib.h>\n')
        f.write('#include "../'+functionName+'.h"\n')
        f.write('\n')
        f.write('void '+functionName+'__init\n')
        f.write('(\n')
        f.write('\t'+functionName+' *self\n')
        f.write(')\n')
        f.write('{\n')
        for name in vars['inputs_AD'].keys():  f.write('\tself->'+name+' = NULL;\n')
        for name in vars['inputs'].keys():     f.write('\tself->'+name+' = NULL;\n')
        for name in vars['outputs_AD'].keys(): f.write('\tself->'+name+' = NULL;\n')
        for name in vars['outputs'].keys():    f.write('\tself->'+name+' = NULL;\n')
        for oName in vars['outputs_AD'].keys():
            for iName in vars['inputs_AD'].keys():
                f.write('\tself->d_'+oName+'__d_'+iName+' = NULL;\n')
        f.write('}\n')
