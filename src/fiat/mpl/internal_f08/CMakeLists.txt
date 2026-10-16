# (C) Copyright 2020- ECMWF.
# (C) Copyright 2024- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

if (NOT HAVE_MPL_F77_DEPRECATED)

    ecbuild_list_add_pattern( LIST fiat_fypp_src GLOB
        *.fypp
    	)
    set (fiat_src_from_fypp "")
    ecbuild_debug(DEBUG2 fiat_expand ${fiat_fypp_src})
    fiat_expand_fypp(
        PYTHON_MODULE_DIR      ${PROJECT_SOURCE_DIR}/python_utils
        SOURCE_DIR             ${CMAKE_CURRENT_SOURCE_DIR}
        INPUT_SRCS             ${fiat_fypp_src}
	OUTPUT_SRCS            fiat_src_from_fypp
    )
    ecbuild_debug(DEBUG2 fiat_expand fiat_src ${fiat_src_from_fypp})
 set( fiat_src_from_fypp ${fiat_src_from_fypp} PARENT_SCOPE )
endif()
