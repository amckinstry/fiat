# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

# Based on fieldType in field_api.


class ecType(object):
    def __init__(self, **kwargs):
      try:
        """Pass either ecType(kind='JPIM',rank=2) rank and kind separately, or
         ecType(ranksuff='2IM') together

        Then ecType('ranksuff').datatype == 'INTEGER(KIND=JPIM)'
        """
        self.__dict__ = kwargs
        try:
            self.rank = int(self.ranksuff[:1])
            self.kind = "JP" + self.ranksuff[1:]
            self.suffix = self.ranksuff[1:]
        except:
            # ranksuff not passed
            self.suffix = self.kind[2:]

        tt = self.suffix[0]
        ss = self.suffix[1]

        th = {"R": "REAL", "I": "INTEGER", "L": "LOGICAL", "C": "CHARACTER"}
        td = {"R": "0.0", "I": "0", "L": ".FALSE.", "C": ""}
        ts = {"M": "4", "D": "8", "B": "8", "H": "1"}
        tm = {
            "RM": "MPI_REAL4",
            "RD": "MPI_REAL8",
            "IM": "MPI_INTEGER",
            "IB": "MPI_INTEGER8",
            "CH": "MPI_BYTE",  # Used for size
        }
        tk = {
            "RM": "REAL(KIND=JPRM)",
            "RD": "READ(KIND=JPRD)",
            "IM": "INTEGER(KIND=JPIM)",
            "IB": "INTEGER(KIND=JPIB)",
            "CH": "CHARACTER(LEN=*)",
        }
        if tt == "C":
            self.datatype = "CHARACTER(LEN=*)"
        else:
            self.datatype = th[tt] + "(KIND=" + self.kind + ")"
        self.rank = int(self.rank)

        if self.ranksuff == "1CH" or self.ranksuff.startswith("0"):
            self.scalar = True
        else:
            self.scalar = False

        self.default = td[tt] + "_" + self.kind
        self.base_type = th[tt]

        dimension = {
            0: "",
            1: ",DIMENSION(:)",
            2: ",DIMENSION(:,:)",
            3: ",DIMENSION(:,:,:)",
        }
        self.dimension = dimension[self.rank]
        self.datasize = ts[ss] + "_JPIB"
        self.mpi_datatype = tm[self.suffix]
      except Exception as ex:
          breakpoint()
          print(ex)
          
# Notes:
# 1RM => 'REAL(KIND=JPRM),  but 0CH => 'CHARACTER(LEN=*)'

# Helper fns
def kind(ranksuff):
    return ecType(ranksuff=ranksuff).kind


def dim(ranksuff):
    return ecType(ranksuff=ranksuff).rank - 1


def dimension(ranksuff):
    return ecType(ranksuff=ranksuff).dimension


def datatype(ranksuff):
    return ecType(ranksuff=ranksuff).datatype


def mpi_datatype(ranksuff):
    return ecType(ranksuff=ranksuff).mpi_datatype


def base_type(ranksuff):
    return ecType(ranksuff=ranksuff).base_type

def scalar(ranksuff):
    return ecType(ranksuff=ranksuff).scalar

def datasize(ranksuff):
    return ecType(ranksuff=ranksuff).datasize

def is_not_contiguous(ranksuff, varname):
     sub  = {
         '0' : '''.not. IS_CONTIGUOUS({varname})''',
         '4':  '''(LOC({varname}(UBOUND({varname},1))) - LOC({varname}(LBOUND({varname},1)))) &
      &           /= 4_JPIB*(ICOUNT - 1)''', 
         '8':  '''(LOC({varname}(UBOUND({varname},1))) - &
      &          LOC({varname}(LBOUND({varname},1)))) /= 8_JPIB*(ICOUNT - 1)''', 
         'I8': '''(LOC({varname}(UBOUND({varname},1))) - &
      &            LOC({varname}(LBOUND({varname},1)))) /= 8_JPIB*(ICOUNT - 1)''', 
         '42': '''(LOC({varname}(UBOUND({varname},1),UBOUND({varname},2))) - &
      &         LOC({varname}(LBOUND({varname},1),LBOUND({varname},2)))) &
      &             /= 4_JPIB*(ICOUNT - 1) ''', 
        '82': '''(LOC({varname}(UBOUND({varname},1),UBOUND({varname},2))) - &
      &         LOC({varname}(LBOUND({varname},1),LBOUND({varname},2)))) &
      &             /= 8_JPIB*(ICOUNT - 1)''', 
        '43': '''(LOC({varname}(UBOUND({varname},1),UBOUND({varname},2),UBOUND({varname},3))) - &
      &         LOC({varname}(LBOUND({varname},1),LBOUND({varname},2),LBOUND({varname},3)))) &
      &              /= 4_JPIB*(ICOUNT - 1)''', 
        '83': '''(LOC({varname}(UBOUND({varname},1),UBOUND({varname},2),UBOUND({varname},3))) - &
      &         LOC({varname}(LBOUND({varname},1),LBOUND({varname},2),LBOUND({varname},3)))) &
      &              /= _JPIB*(ICOUNT - 1)''', 
      }
     v = { '1RM': '0','1RD': '8','1IM': '4','2IM' :  '4','1IB':  '8','0IM' : '4','2RM': '42', 
           '2RD': '82','3RM': '43','3RD': '83','0RM': '4','0RD': '8','OCH': '8','1CH': '-1' }
     s = sub[v[ranksuff]]
     return s.replace('{varname}',varname)


#### === NOT CURRENTLY USED ====

kinds = ["JPRM", "JPRD", "JPIM", "JPLM", "JPIA"]


def getECTypesDict(ranks=[1, 2, 3, 4, 5], kinds=kinds):

    d = {}
    for t in [ecType(kind=kind, rank=rank) for (kind) in kinds for rank in ranks]:
        d[t.name] = t

    # if hasView != None:
    #  l = [ft for ft in l if ft.hasView == hasView]

    # if ganged != None:
    #  l = [ft for ft in l if ft.ganged == ganged]

    return d


def useParkind1(kinds=kinds):
    return "USE PARKIND1, ONLY : " + ", ".join(kinds)
