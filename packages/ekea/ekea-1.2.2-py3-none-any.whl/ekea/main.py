from fortlab import Fortlab

from ekea.mpasocn import MPASOcnKernel
from ekea.eam import EAMKernel
from ekea.timing import KernelTimeGenerator, KernelTimeViewer
from ekea.varwhere import VariableList

class EKEA(Fortlab):

    _name_ = "ekea"
    _version_ = "1.2.2"
    _description_ = "E3SM Fortran Kernel Extraction and Analysis"
    _long_description_ = "E3SM Fortran Kernel Extraction and Analysis"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/ekea"
    _builtin_apps_ = [MPASOcnKernel, EAMKernel, KernelTimeGenerator,
                      KernelTimeViewer, VariableList]

    def __init__(self):
        pass
