import os
from inspect import signature
from subprocess import call

from .Scalar.GraphEntity import GraphEntity
from .utils import *
from .CodeGeneration.misc import writeStructFile, writeOtherFiles
from .CodeGeneration.calculate import writeCalculateFile
from .CodeGeneration.FormattedBuffer import FormattedBuffer

# Set debug mode here
debugMode = True

def DEBUG(msg):
    if debugMode: print(msg)

def compile(func, functype='REPLACE', prefix='.', disableDerivs=False):

    G = GraphEntity.graph
    funcname = 'ADF_'+func.__name__
    dirname = os.path.join(prefix, funcname)

    vars = {
        'inputs'     : {},
        'outputs'    : {},
        'inputs_AD'  : {},
        'outputs_AD' : {},
    }
    shapes = {
        'inputs'     : {},
        'outputs'    : {},
        'inputs_AD'  : {},
        'outputs_AD' : {},
    }

    # Get input shapes --------------------------------------------------------
    funcsig = signature(func)
    for k,v in funcsig.parameters.items():
        if k=='inputs_AD': shapes['inputs_AD'] = v.default
        if k=='inputs'   : shapes['inputs'   ] = v.default

    # Create input variables --------------------------------------------------
    for name, shape in shapes['inputs_AD'].items():
        vars['inputs_AD'][name] = getInput(shape)
    for name, shape in shapes['inputs'   ].items():
        vars['inputs'   ][name] = getInput(shape)

    # Define function to compile a single set of conditional values -----------
    def compileBranch(f, inputs_AD, inputs, maxsize=0, disableDerivs=False):
        G.initCompilationPass()
        outputs, outputs_AD = f(inputs_AD=inputs_AD, inputs=inputs)
        for var in outputs.values(): setAsOutput(var)
        for var in outputs_AD.values(): setAsOutput(var)
        G.finalizeCompilationPass(disableDerivs=disableDerivs)
        return G.tapeSize if G.tapeSize>maxsize else maxsize,\
               outputs, outputs_AD

    # Evaluate compile passes for different conditional branches --------------
    maxsize, vars['outputs'], vars['outputs_AD'] = \
        compileBranch(func, vars['inputs_AD'], vars['inputs'], \
                      disableDerivs=disableDerivs)
    DEBUG('Initial branch compiled')
    while(G.conditionalHandler.nKnownConditionals)>0:
        maxsize, vars['outputs'], vars['outputs_AD'] = \
            compileBranch(func, vars['inputs_AD'], vars['inputs'], \
                          maxsize=maxsize, disableDerivs=disableDerivs)
    DEBUG('Final branch compiled')

    # Get output shapes -------------------------------------------------------
    for name, var in vars['outputs'   ].items():
        shapes['outputs'   ][name] = getOutputShape(var)
    for name, var in vars['outputs_AD'].items():
        shapes['outputs_AD'][name] = getOutputShape(var)

    # Create ADF directory ----------------------------------------------------
    call('mkdir -p '+dirname+'/src', shell=True)

    # Create header file ------------------------------------------------------
    buffer = FormattedBuffer()
    writeStructFile(buffer, funcname, shapes, G.includes, maxsize)
    with open(dirname+'/'+funcname+'.h', 'w') as f:
        f.write(buffer.getContents())
    DEBUG('Wrote struct file')

    # Create init function ----------------------------------------------------
    buffer = FormattedBuffer()
    writeOtherFiles(buffer, funcname, vars)
    with open(dirname+'/src/init.c', 'w') as f:
        f.write(buffer.getContents())
    DEBUG('Wrote init file')

    # Create calculate function -----------------------------------------------
    buffer = FormattedBuffer()
    fbuf = GraphEntity.graph.forwardBuffer
    rbuf = GraphEntity.graph.reverseBuffer
    rbuf.lines = rbuf.lines[::-1]
    writeCalculateFile(buffer, funcname, functype, shapes, fbuf, rbuf)
    with open(dirname+'/src/calculate.c', 'w') as f:
        f.write(buffer.getContents())
    DEBUG('Wrote calculate file')

    # Run pymake --------------------------------------------------------------
    pwd = os.getcwd()
    os.chdir(dirname)
    call('pymake', shell=True)
    os.chdir(pwd)
