# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

# Based on fieldType in field_api.

kinds = ["JPRM", "JPRD", "JPIM", "JPLM", "JPIA"]

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
            self.datatype = "CHARACTER"
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
          
# Helper fns

def dimension(ranksuff):
    return ecType(ranksuff=ranksuff).dimension


def datatype(ranksuff):
    return ecType(ranksuff=ranksuff).datatype


def mpi_datatype(ranksuff):
    return ecType(ranksuff=ranksuff).mpi_datatype

def scalar(ranksuff):
    return ecType(ranksuff=ranksuff).scalar

def datasize(ranksuff):
    return ecType(ranksuff=ranksuff).datasize

def base_type(ranksuff):
    return ecType(ranksuff=ranksuff).base_type

def useParkind1(kinds=kinds):
    return "USE PARKIND1, ONLY : " + ", ".join(kinds)
