__author__ = 'geoffroy'

from pymatgen.core.structure import Structure
from pymatgen.core.periodic_table import Element
from mpcollab.defects.defectsmaker import DefectsMaker
from mpcollab.defects.vasp import make_vasp_defect_files
import json


def example_maker():
        #print open("/home/geoffroy/codes/MPCollab/mpcollab/defects/PbTiO3.json",'r')
        #print json.loads(open("/home/geoffroy/codes/MPCollab/mpcollab/defects/PbTiO3.json",'r').read())
        struct=Structure.from_dict(json.loads(open("PbTiO3.json",'r').read()))
        print struct
        make_vasp_defect_files(DefectsMaker(struct,{Element('Pb'):(0,2),Element('Ti'):(0,4),Element('O'):(-2,0),
                                                Element('Al'):(3,4), Element('V'):(3,4),Element("Cr"):(3,4),Element('Ga'):(3,4),
                                                Element('Fe'):(3,4),Element('Co'):(3,4),Element('Ni'):(3,4),
                                                Element('K'):(1,2),Element('Na'):(1,2),Element("N"):(-3,-2)},{Element('Pb'):[Element('Na'),Element('K')],
                                                Element('Ti'):[Element(e) for e in ['Al','V','Cr','Ga','Fe','Co','Ni']],Element('O'):[Element('N')]},
                                                {Element('Pb'):2,Element('Ti'):4,Element('O'):-2},standardized=False).defects,
                                                "./",
                                                "mp-20459",struct.composition)


if __name__ == '__main__':
    example_maker()