# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

# Based on fieldType in field_api.

class ecType (object):
  def __init__ (self, **kwargs):
    """ Pass either ecType(kind='JPIM',rank=2) rank and kind separately, or
     ecType(ranksuff='2IM') together

     Then ecType('ranksuff').datatype == 'INTEGER(KIND=JPIM)'
    """
    self.__dict__ = kwargs
    try:
      self.rank = int(self.ranksuff[:1])
      self.kind = self.ranksuff[1:]
      self.suffix = self.ranksuff[1:]
    except:
      # ranksuff not passed
      self.suffix = self.kind[2:]

    tt = self.suffix[0]
    ss = self.suffix[1]

    th = {'R': 'REAL', 'I': 'INTEGER', 'L': 'LOGICAL', 'C': 'CHARACTER'}
    td = {'R':  '0.0', 'I':       '0', 'L': '.FALSE.', 'C': ''}
    ts = {'M': '4',    'D':       '8', 'B': '8', 'H':   '1'}
    tm = {'RM' : 'MPI_REAL4', 'RD' : 'MPI_REAL8', 'IM' : 'MPI_INTEGER', 'ID' : 'MPI_INTEGER8' }

    if 'tt' == 'C':
      self.type ='CHARACTER(LEN=*)'
      self.rank = 0
    else:
      self.type = th[tt] + '(KIND=' + self.kind + ')'
      self.rank = int (self.rank)

    self.default = td[tt] + '_' + self.kind

    self.name = '%s%s' % (self.rank, self.suffix);
    self.shape = ','.join ([':'] * int (self.rank))
    self.viewRank = self.rank-1
    self.viewShape = ','.join ([':'] * (self.rank-1))
    self.lbptr = ', '.join (list (map (lambda i: "LBOUNDS(" + str (i+1) + "):", range (0, self.rank))))
    #self.hasView = self.rank > 1
    #self.ganged = self.rank > 2
    self.datasize = ts[ss] + '_JPIB'
    self.mpi_datatype = tm[self.suffix]

# Notes:
# 1RM => 'REAL(KIND=JPRM,  but 0CH => 'CHARACTER(LEN=*)'

kinds = ['JPRM', 'JPRD', 'JPIM', 'JPLM','XXCH'  ]

# Helper fns
def kind(ranksuff):
  return ecType(ranksuff=ranksuff).kind
def dim(ranksuff):
  return ecType(ranksuff=ranksuff).rank -1



#### === NOT USED ====

def getECTypesDict (ranks=[1,2,3,4,5], kinds=kinds):
  
  d = {}
  for t in [ecType (kind=kind, rank=rank) for (kind) in kinds for rank in ranks]:
    d[t.name] = t
  
  #if hasView != None:
  #  l = [ft for ft in l if ft.hasView == hasView]
  
  #if ganged != None:
  #  l = [ft for ft in l if ft.ganged == ganged]
  
  return d

def useParkind1 (kinds=kinds):
  return 'USE PARKIND1, ONLY : ' + ', '.join (kinds)

