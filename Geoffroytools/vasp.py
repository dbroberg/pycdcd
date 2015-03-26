#!/usr/bin/env python

"""
TODO create a VaspInputSet instead?
"""

__author__ = "Geoffroy Hautier"
__copyright__ = "Copyright 2014, The Materials Project"
__version__ = "1.0"
__maintainer__ = "Geoffroy Hautier"
__email__ = "geoffroy@uclouvain.be"
__status__ = "Development"
__date__ = "November 4, 2012"

from pymatgen.io.vaspio.vasp_input import Kpoints
from pymatgen.io.vaspio_set import MPVaspInputSet
import json
import os

def make_vasp_defect_files(dictio, path_base, task_id, compo, hse=False):
    """
    simple static method creating VASP files ready for defect computations
    Args:
        dictio:
            the defects data as a dictionnary
        path_base:
            where do we write the files
        task_id:
            some id of the bulk computed data
        compo:
            Composition of the bulk computed data
        hse:
            hse run or not
    """
    count=1
    for site in dictio:
        for charge in site['charges']:
            print charge
            for s in site['supercells']:
                dict_transf={'history':[{'source':task_id}], 'compo': compo.to_dict, 'defect_type': site['short_name'], 'defect_site': site['unique_sites'].to_dict, 'charge': charge, 'supercell': s['size']}
                dict_params=MPVaspInputSet().get_all_vasp_input(s['structure'])
                incar=dict_params['INCAR']
                incar['IBRION']=2
                incar['ISIF']=0
                incar['ISPIN']=1
                incar['LWAVE']=False
                #incar['EDIFF']=0.0001
                incar['EDIFF']=0.001
                incar['ISMEAR']=0
                incar['SIGMA']=0.05
                incar['LVHAR']=True
                incar['LORBIT']=11
                incar['ALGO']="Fast"
                #incar['ALGO']="Normal"
                if hse == True:
                    incar['LHFCALC']=True
                    incar["ALGO"]="All"
                    incar["HFSCREEN"]=0.2
                    incar["PRECFOCK"]="Fast"
                    incar["AEXX"]=0.45
                kpoint=Kpoints.monkhorst_automatic()
                path=path_base+"/"+compo.reduced_formula+"_"+str(task_id)+"/"+str(site['short_name'])+"/"+"charge"+str(charge)+"/"
                os.makedirs(path)
                f=open(path+"/transformations.json",'w')
                f.write(json.dumps(dict_transf))
                comp=s['structure'].composition
                sum_elec=0
                elts=set()
                for p in dict_params['POTCAR']:
                    if p.element not in elts:
                        sum_elec+=comp.to_dict[p.element]*p.nelectrons
                        elts.add(p.element)
                    #print p.element
                    #print comp.to_dict[p.element]
                    #print p.valence
                print sum_elec
                if charge != 0:
                    incar['NELECT']=sum_elec-charge
                dict_params['POTCAR'].write_file(path+"POTCAR")
                incar.write_file(path+"INCAR")
                kpoint.write_file(path+"KPOINTS")
                dict_params['POSCAR'].write_file(path+"POSCAR")
                #print Poscar(s['structure'])
                #Poscar(s['structure']).write_file(path+"POSCAR")
                count=count+1
                f.close()