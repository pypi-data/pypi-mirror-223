from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.presentation.common import *
from spire.presentation import *
from ctypes import *
import abc

class UOPReader (SpireObject) :
    """

    """
    @staticmethod

    def UofToOox(uosFileName:str,ooxFileName:str):
        """

        """
        
        GetDllLibPpt().UOPReader_UofToOox.argtypes=[ c_wchar_p,c_wchar_p]
        GetDllLibPpt().UOPReader_UofToOox( uosFileName,ooxFileName)

