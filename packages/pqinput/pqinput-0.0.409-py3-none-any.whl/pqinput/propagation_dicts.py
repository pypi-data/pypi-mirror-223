#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:52:38 2023

@author: lucas

Propagation dictionaries
"""
# %% Propagation 
def propagation_parameters(dt, steps, wcycle, dir, nfile='norm'):
    propapar = {'dt': dt, 'steps': int(steps), 'wcycle': wcycle, 
                'dir': dir, 'nfile': 'norm'}
    return propapar 

'''Kinectic energy operator'''
def kinectic_operator(mass=0, pml=False, key=None, ref=None, lmap=2, thick=10):
    T = {'head':'T', 'name':"GridNablaSq"}
    if not isinstance(mass, list):
        T.update({'mass':mass})
        if pml: T.update({'name':"GridPML", 'lmap':lmap, 'thick':thick})
    else:
        T.update({'mass':','.join(str(m) for m in mass)})
        if pml: 
            if lmap==2: lmap=[2 for m in mass]
            T.update({'name':"GridPML", 'lmap':','.join(str(l) for l in lmap)})
            try: 
                len(thick)==len(mass)
                T.update({'thick':thick})
            except: pass
    if key: T.update({'key':key}) 
    if ref and not key: T = {'head':'T', 'ref':ref}
    return T

'''Potential energy surfaces'''
def potential_operator(file, offset=None, head='V', name='GridPotential', scale=None): # file MgH/pots/pot_Sig0
    V = {'head':head, 'name':name, 'file':file}
    if scale: V.update({'scale':scale})
    if offset: V.update({'offset':offset})
    return V

'''Diagonal terms: pure states'''
def diagonal_mel(n, Opes, label=None):
    mel = {'head':f'm{n}.{n}', 'name':'Sum', 'heir':Opes}
    if label: mel.update({'label':label})
    return mel

'''Off diagonal terms: interactions'''
def offdiagonal_mel(m,n, file, scale=None, laser=None): # file MgH/mu/mu_Sig0Sig1:: relate to V
    mel = {'head':f'm{m}.{n}', 'name':'GridPotential',  'file':file}
    if scale and not laser: mel.update({'scale':scale})
    if laser and not scale: mel.update({'laser':laser, 'name':'GridDipole'})
    return mel

'''Hamiltonian dictionary'''
def hamiltonian_parameters(Mels):
    Hparams = {'type':'Multistate', 'Mels':Mels} 
    return Hparams
# Hparams = {'type':'Multistate', 'Mels':[Sig0xy, Sig1y, dipx]} 

'''Wavefunction parameters'''
def wavefunction_parameters(wf, ef, vib, label=None, dim=1):
    if dim==1:
        WFpar = {'type':'Multistate', 'states':'',
         'file':[f"../../MgH/efs_{e}/ef_{v}" for e,v in zip(ef, vib)],
         'index':list(wf), 'normalize':'true'}
    if dim==2:
        WFpar = {'type':'Multistate', 'states':'',
             'file':[f"../../MgH/efs_2D/{ef[i][0]}ef{vib[i][0]}_{ef[i][1]}ef{vib[i][1]}" 
                     for i, _ in enumerate(wf)], 'index':list(wf), 'normalize':True}
    if label: WFpar.update({'label':label})
    return WFpar

'''Filter parameters'''
def filter_expeconly(mu, file):
    operators = {'head':'expeconly', 'name':'Multistate', 'states':'', 
                'unity':'False', 'header':f'mu{mu}', 
                f'mu{mu}':{'name':'GridPotential', 'file':file}}
    return operators

def filter_jump(head, elements, seed, max_jump, unity="false", nonhermitian='true'):
    operators = {'head':'apply', 'name':"Jump", "seed":seed, "max_pjump":max_jump,
                    'heir':{ 'head':head,'name':"Multistate",'unity':unity,
                            'nonhermitian':nonhermitian,
            'heir':[{'head':key, 'name':"Scalar", 'value':val}
                    for key,val in elements.items()] }}
    return operators
'''NEED TO CHANGE THIS PART, BECAUSE I WANT ANOTHER OPERATOR AS CHILD 
OF THE JUMP OPERATOR, NOT TWO OPERATORS'''
# %% Save parameters

def saveparameters(ppar, mass, cavity, initial_state, labels, folder, fname=''):
    from unitscvt.aunits import autime as au2sec

    text = f" Parameters for calculations \n"\
    "__________________________________________________\n"\
    f"dt : {ppar['dt']}\n"\
    f"steps : {ppar['steps']}\n"\
    f"wcycle : {ppar['wcycle']}\n"\
    f"dir : {ppar['dir']}\n"\
    f"nfile : {ppar['nfile']}\n"\
    f"tau (fs) : {ppar['dt']*ppar['steps']*au2sec*1e15}\n"\
    f"mass : {mass}\n"\
    f"w01 (au, eV) : {cavity['w01']}\n"\
    f"w12 (au, eV) : {[cavity['w12'] if 'w12' in cavity.keys() else 0]}\n" 
    f"E_x (au) : {cavity['Ex']}\n"\
    f"E_y (au) : {[cavity['Ey'] if 'Ey' in cavity.keys() else 0]}\n"\
    f"initial state : {initial_state}\n"\
    f"figlegend : {labels}\n"
    
    with open(folder + f'Parameters{fname}.txt', 'w') as f:
        f.write(text)
        # f"g_x (au) : {cavity['gx']}\n"\
        # f"g_y (au) : {cavity['gy']}\n"\

def savedict2pars(dictionary, folder, fname=''):
    
    text = " Parameters for calculations \n"\
    "__________________________________________________\n"
        
    for key, value in dictionary.items():
        text += f"{key} : {value}\n"
    
    with open(folder + f'/Parameters{fname}.txt', 'w') as f:
        f.write(text)
