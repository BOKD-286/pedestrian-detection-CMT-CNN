################################################################################################
# Command alias for debugging messages
# Usage:
#   dmgs(<message>)
function(dmsg)
  message(STATUS ${ARGN})
endfunction()

################################################################################################
# Removes duplicates from list(s)
# Usage:
#   caffe_list_unique(<list_variable> [<list_variable>] [...])
macro(caffe_list_unique)
  foreach(__lst ${ARGN})
    if(${__lst})
      list(REMOVE_DUPLICATES ${__lst})
    endif()
  endforeach()
endmacro()

################################################################################################
# Clears variables from lsit
# Usage:
#   caffe_list_unique(<variables_list>)
macro(caffe_clear_vars)
  foreach(_var ${ARGN})
    unset(${_var})
  endforeach()
endmacro()

################################################################################################
# Removes duplicates from string
# Usage:
#   caffe_string_unique(<string_variable>)
function(caffe_string_unique __string)
  if(${__string})
    set(__list ${${__string}})
    separate_arguments(__list)
    list(REMOVE_DUPLICATES __list)
    foreach(__e ${__list})
      set(__str "${__str} ${__e}")
    endforeach()
    set(${__string} ${__str} PARENT_SCOPE)
  endif()
endfunction()

################################################################################################
# Prints list element per line
# Usage:
#   caffe_print_list(<list>)
function(caffe_print_list)
  foreach(e ${ARGN})
    message(STATUS ${e})
  endforeach()
endfunction()

################################################################################################
# Function merging lists of compiler flags to single string.
# Usage:
#   caffe_merge_flag_lists(out_variable <list1> [<list2>] [<list3>] ...)
function(caffe_merge_flag_lists out_var)
  set(__result "")
  foreach(__list ${ARGN})
    foreach(__flag ${${__list}})
      string(STRIP ${__flag} __flag)
      set(__result "${__result} ${__flag}")
    endforeach()
  endforeach()
  string(STRIP ${__result} __result)
  set(${out_var} ${__result} PARENT_SCOPE)
endfunction()

################################################################################################
# Converts all paths in list to absolute
# Usage:
#   caffe_convert_absolute_paths(<list_variable>)
function(caffe_convert_absolute_paths variable)
  set(__dlist "")
  foreach(__s ${${variable}})
    get_filename_component(__abspath ${__s} ABSOLUTE)
    list(APPEND __list ${__abspath})
  endforeach()
  set(${variable} ${__list} PARENT_SCOPE)
endfunction()

################################################################################################
# Reads set of version defines from the header file
# Usage:
#   caffe_parse_header(<file> <define1> <define2> <define3> ..)
macro(caffe_parse_header FILENAME FILE_VAR)
  set(vars_regex "")
  set(__parnet_scope OFF)
  set(__add_cache OFF)
  foreach(name ${ARGN})
    if("${name}" STREQUAL "PARENT_SCOPE")
      set(__parnet_scope ON)
    elseif("${name}" STREQUAL "CACHE")
      set(__add_cache ON)
    elseif(vars_regex)
      set(vars_regex "${vars_regex}|${name}")
    else()
      set(vars_regex "${name}")
    endif()
  endforeach()
  if(EXISTS "${FILENAME}")
    file(STRINGS "${FILENAME}" ${FILE_VAR} REGEX "#define[ \t]+(${vars_regex})[ \t]+[0-9]+" )
  else()
    unset(${FILE_VAR})
  endif()
  foreach(name ${ARGN})
    if(NOT "${name}" STREQUAL "PARENT_SCOPE" AND NOT "${name}" STREQUAL "CACHE")
      if(${FILE_VAR})
        if(${FILE_VAR} MATCHES ".+[ \t]${name}[ \t]+([0-9]+).*")
          string(REGEX REPLACE ".+[ \t]${name}[ \t]+([0-9]+).*" "\\1" ${name} "${${FILE_VAR}}")
        else()
          set(${name} "")
        endif()
        if(__add_cache)
          set(${name} ${${name}} CACHE INTERNAL "${name} parsed from ${FILENAME}" FORCE)
        elseif(__parnet_scope)
          set(${name} "${${name}}" PARENT_SCOPE)          
        endif()
      else()
        unset(${name} CACHE)
      endif()
    endif()
  endforeach()
endmacro()

################################################################################################
# Reads single version define from the header file and parses it
# Usage:
#   caffe_parse_header_single_define(<library_name> <file> <define_name>)
function(caffe_parse_header_single_define LIBNAME HDR_PATH VARNAME)
  set(${LIBNAME}_H "")
  if(EXISTS "${HDR_PATH}")
    file(STRINGS "${HDR_PATH}" ${LIBNAME}_H REGEX "^#define[ \t]+${VARNAME}[ \t]+\"[^\"]*\".*$" LIMIT_COUNT 1)
  endif()

  if(${LIBNAME}_H)
    string(REGEX REPLACE "^.*[ \t]${VARNAME}[ \t]+\"([0-9]+).*$" "\\1" ${LIBNAME}_VERSION_MAJOR "${${LIBNAME}_H}")
    string(REGEX REPLACE "^.*[ \t]${VARNAME}[ \t]+\"[0-9]+\\.([0-9]+).*$" "\\1" ${LIBNAME}_VERSION_MINOR  "${${LIBNAME}_H}")
    string(REGEX REPLACE "^.*[ \t]${VARNAME}[ \t]+\"[0-9]+\\.[0-9]+\\.([0-9]+).*$" "\\1" ${LIBNAME}_VERSION_PATCH "${${LIBNAME}_H}")
    set(${LIBNAME}_VERSION_MAJOR ${${LIBNAME}_VERSION_MAJOR} ${ARGN} PARENT_SCOPE)
    set(${LIBNAME}_VERSION_MINOR ${${LIBNAME}_VERSION_MINOR} ${ARGN} PARENT_SCOPE)
    set(${LIBNAME}_VERSION_PATCH ${${LIBNAME}_VERSION_PATCH} ${ARGN} PARENT_SCOPE)
    set(${LIBNAME}_VERSION_STRING "${${LIBNAME}_VERSION_MAJOR}.${${LIBNAME}_VERSION_MINOR}.${${LIBNAME}_VERSION_PATCH}" PARENT_SCOPE)

    # append a TWEAK version if it exists:
    set(${LIBNAME}_VERSION_TWEAK "")
    if("${${LIBNAME}_H}" MATCHES "^.*[ \t]${VARNAME}[ \t]+\"[0-9]+\\.[0-9]+\\.[0-9]+\\.([0-9]+).*$")
      set(${LIBNAME}_VERSION_TWEAK "${CMAKE_MATCH_1}" ${ARGN} PARENT_SCOPE)
    endif()
    if(${LIBNAME}_VERSION_TWEA