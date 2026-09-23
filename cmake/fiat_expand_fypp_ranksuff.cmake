# (C) Copyright 2022- ECMWF.
# (C) Copyright 2022- Meteo-France.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

##############################################################################
#.rst:
#
# fiat_expand_fypp_ranksuff
# ==============================
# 
# Preprocess a given set of .fypp files over the rank
# and suffix (i.e. field data-type) matrix. ::
# 
#             fiat_expand_fypp_ranksuff( PYTHON_MODULE_DIR <python-util-module-dir> 
#                                        SOURCE_DIR        <source-directory> 
#                                        INPUT_SRCS        <fypp files>
#                                        OUTPUT_SRCS       <processed F90 files>
#					 RANKSUFFS	  <ranksuff vars>
#                                        [CORE] )
#
# Input variables
# ---------------
#
# :PYTHON_MODULE_DIR:  Directory containing ecType.py python module.
# :SOURCE_DIR:         Directory containing .fypp files to be processed.
# :INPUT_SRCS:         List of .fypp files to be processed.
# :OUTPUT_SRCS:        List of processed .F90 files named ${func}_${ranksuff}.F90
# :RANKSUFFS:          List of ranksuff suffixes to do 
# :CORE:               Flag to determine whether ${rank}${suff}.F90
#                      files are to be generated
#
##############################################################################

macro( fiat_expand_fypp_ranksuff )

    set( options CORE )
    set( oneValueArgs PYTHON_MODULE_DIR SOURCE_DIR )
    set( multiValueArgs INPUT_SRCS OUTPUT_SRCS RANKSUFFS )

    cmake_parse_arguments( _PAR "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

    foreach (FUNC ${_PAR_INPUT_SRCS} "")
	   
        if( ${_PAR_CORE} )
    	 foreach (RANKSUFF ${_${FUNC}_RANKSUFFS})
             add_custom_command (OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}.F90
       	      COMMAND ${FYPP}  -Dranksuff=\\\'${RANKSUFF}\\\'  ${fypp_defines} -m os -M ${_PAR_PYTHON_MODULE_DIR} -m ecType 
               ${_PAR_SOURCE_DIR}/${FUNC}_RANKSUFF.fypp > ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}.F90
               DEPENDS ${_PAR_SOURCE_DIR}/${FUNC}_RANKSUFF.fypp
               VERBATIM)
             list(APPEND ${_PAR_OUTPUT_SRCS} ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}${suff}.F90)
           endforeach ()
        else()
           foreach (FUNC ${_PAR_INPUT_SRCS})
             add_custom_command (OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}.F90
       	      COMMAND ${FYPP} -Dranksuff=\\\'${RANKSUFF}\\\' ${fypp_defines} -m os -M ${_PAR_PYTHON_MODULE_DIR} -m ecType
               ${_PAR_SOURCE_DIR}/${FUNC}_RANKSUFF.fypp > ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}.F90
               DEPENDS ${_PAR_SOURCE_DIR}/${FUNC}_RANKSUFF.fypp
               VERBATIM)
             list(APPEND ${_PAR_OUTPUT_SRCS} ${CMAKE_CURRENT_BINARY_DIR}/${FUNC}_${RANKSUFF}.F90)
           endforeach ()
        endif()
    endforeach ()

endmacro()
