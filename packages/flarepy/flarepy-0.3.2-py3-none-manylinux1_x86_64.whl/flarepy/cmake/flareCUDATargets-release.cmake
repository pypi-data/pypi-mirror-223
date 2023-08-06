#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "flare::flare_cuda" for configuration "Release"
set_property(TARGET flare::flare_cuda APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(flare::flare_cuda PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/flarepy/libflare_cuda.so"
  IMPORTED_SONAME_RELEASE "libflare_cuda.so"
  )

list(APPEND _cmake_import_check_targets flare::flare_cuda )
list(APPEND _cmake_import_check_files_for_flare::flare_cuda "${_IMPORT_PREFIX}/flarepy/libflare_cuda.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
