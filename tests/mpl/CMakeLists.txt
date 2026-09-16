# (C) Copyright 2026- ECMWF.
# (C) Copyright 2026- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


list( APPEND suff_srcs )
list( APPEND nonsuff_srcs field_factory_module )

## expand ranksuff sources
fiat_expand_fypp_ranksuff(
   PYTHON_MODULE_DIR      ${PROJECT_SOURCE_DIR}/python_utils
   SOURCE_DIR             ${CMAKE_CURRENT_SOURCE_DIR}
   INPUT_SRCS             ${ranksuff_srcs}
   OUTPUT_SRCS            srcs
)

# TODO: Create 
# ----------------------------------------------------------------------------

foreach (SUFF IN REAL4 REAL8 INT INT_SCALAR)
ecbuild_add_test(
    TARGET  fiat_test_mpl_allreduce_${SUFF}_mod
    SOURCES test_mpl_allreduce_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------


foreach (SUFF IN REAL4 REAL8 INTEGER)
ecbuild_add_test(
    TARGET  fiat_test_mpl_bytes_${SUFF}_mod
    SOURCES test_mpl_bytes_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN REAL8 REAL4 CHAR_SCALAR INT INT_SCALAR)
ecbuild_add_test(
    TARGET  fiat_test_mpl_gatherv_${SUFF}_mod
    SOURCES test_mpl_gatherv_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN INT REAL8)
ecbuild_add_test(
    TARGET  fiat_test_mpl_read_${SUFF}_mod
    SOURCES test_mpl_read_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN  REAL4 REAL8 INT INT2 INT8 INT_SCALAR REAL42
                  REAL43 REAL82 CHAR_SCALAR CHAR REAL4_SCALAR REAL8_SCALAR REAL83 )
ecbuild_add_test(
    TARGET  fiat_test_mpl_recv_${SUFF}_mod
    SOURCES test_mpl_recv_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN REAL4 REAL8 INT)
ecbuild_add_test(
    TARGET  fiat_test_mpl_scatterv_${SUFF}_mod
    SOURCES test_mpl_scatterv_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN REAL4 REAL8 INT INT2 INT8 INT_SCALAR REAL42 REAL43 REAL82 CHAR_SCALAR CHAR REAL4_SCALAR REAL8_SCALAR REAL83)
ecbuild_add_test(
    TARGET  fiat_test_mpl_send_${SUFF}_mod
    SOURCES test_mpl_send_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()

# ----------------------------------------------------------------------------

foreach (SUFF IN INT REAL8)
ecbuild_add_test(
    TARGET  fiat_test_mpl_write_${SUFF}_mod
    SOURCES test_mpl_write_${SUFF}_mod.F90
    LIBS    ${fiatlib} ${OMP}
    LINKER_LANGUAGE Fortran
    DEFINITIONS ${FCKIT_DEFINITIONS})
)
endforeach()
