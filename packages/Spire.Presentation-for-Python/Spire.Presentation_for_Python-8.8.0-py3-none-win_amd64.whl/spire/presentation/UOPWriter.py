from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.presentation.common import *
from spire.presentation import *
from ctypes import *
import abc

class UOPWriter (SpireObject) :
    """

    """
    @staticmethod

    def OoxToUof(ooxFileName:str,uosFileName:str):
        """

        """
        
        GetDllLibPpt().UOPWriter_OoxToUof.argtypes=[ c_wchar_p,c_wchar_p]
        GetDllLibPpt().UOPWriter_OoxToUof( ooxFileName,uosFileName)

