#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "flare::flare_cpu" for configuration "Release"
set_property(TARGET flare::flare_cpu APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(flare::flare_cpu PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "MKL::RT"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/flarepy/libflare_cpu.so"
  IMPORTED_SONAME_RELEASE "libflare_cpu.so"
  )

list(APPEND _cmake_import_check_targets flare::flare_cpu )
list(APPEND _cmake_import_check_files_for_flare::flare_cpu "${_IMPORT_PREFIX}/flarepy/libflare_cpu.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
