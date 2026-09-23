# (C) Copyright 2025- ECMWF.
# (C) Copyright 2026- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

include(CMakePrintHelpers)

set(  nonsuff_srcs  "" )
set( suff_srcs test_mpl_alltoallv_mod )

set (_test_mpl_alltoallv_mod_RANKSUFFS 2RM 2RD 2IM)		# REAL4 REAL8 INT
set (_test_mpl_allreduce_mod_RANKSUFFS 2RM 2RD 2IM 1IM)         # REAL4 REAL8 INT INT_SCALAR
set (_test_mpl_gatherv_mod_RANKSUFFS 2RD 2RM 1CH 2IM 1IM)	# REAL4 REAL8 CHARACTER INT INT_SCALAR
set (_test_mpl_scatterv_mod_RANKSUFFS 2RM 2RD 2IM)		# REAL4 REAL8 INT
set (_test_mpl_bytes_mod_RANKSUFFS 2RM 2RD 2IM)			# REAL4 REAL8 INTEGER
set (_test_mpl_read_mod_RANKSUFFS 2IM 2RD)			# INT REAL8
set (_test_mpl_write_mod_RANKSUFFS 2IM 2RD)			# INT REAL8
								# REAL4 REAL8 INT INT2 INT8 INT_SCALAR REAL42
								# REAL43 REAL82 CHAR_SCALAR CHAR REAL4_SCALAR REAL8_SCALAR REAL83 
set (_test_mpl_recv_mod_RANKSUFFS  2RM 2RD 2IM 3IM  2ID  1IM  3RM 4RM 3RD 1CH 2CH 1RM 1RD 4RD )
								# REAL4 REAL8 INT INT2 INT8 INT_SCALAR REAL42 REAL43 REAL82 
								# CHAR_SCALAR CHAR REAL4_SCALAR REAL8_SCALAR REAL83
set (_test_mpl_send_mod_RANKSUFFS 2RM 2RD 2IM 2IX 1IM 3RM 4RM 3RD 4RD 1CH 2CH 1RM 1RD )

set(_ranksuffs)
get_cmake_property(_all_vars VARIABLES)
foreach(_var ${_all_vars})
  if(_var MATCHES "_RANKSUFFS")
  	list(APPEND _ranksuffs ${_var})
  endif()
endforeach()
	
## expand ranksuff sources
fiat_expand_fypp_ranksuff(
   PYTHON_MODULE_DIR      ${PROJECT_SOURCE_DIR}/python_utils
   SOURCE_DIR             ${CMAKE_CURRENT_SOURCE_DIR}
   INPUT_SRCS             ${suff_srcs}
   OUTPUT_SRCS            srcs
   CORE			  TRUE
   RANKSUFFS		  ${_ranksuffs}
)
fiat_expand_fypp(
   PYTHON_MODULE_DIR      ${PROJECT_SOURCE_DIR}/python_utils
   SOURCE_DIR             ${CMAKE_CURRENT_SOURCE_DIR}
   INPUT_SRCS             ${nonsuff_srcs}
   OUTPUT_SRCS            srcs
)

foreach (FUNC ${suff_srcs} )
foreach (RANKSUFF ${_${FUNC}_RANKSUFFS})
ecbuild_add_test( TARGET ${FUNC}_${RANKSUFF} 
		  SOURCES ${FUNC}_${RANKSUFF}.F90
		  LIBS ${fiatlib} ${OMP}
		  LINKER_LANGUAGE Fortran DEFINITIONS ${FCKIT_DEFINITIONS}
	          CONDITION HAVE_MPI
    		  MPI 3 )
endforeach()
endforeach()

foreach (FUNC ${nonsuff_srcs})
ecbuild_add_test(
    TARGET  ${FUNC}
    SOURCES ${FUNC}.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS}
)
endforeach()
