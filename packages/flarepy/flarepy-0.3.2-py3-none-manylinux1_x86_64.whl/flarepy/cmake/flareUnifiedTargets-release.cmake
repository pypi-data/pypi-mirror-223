#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "flare::flare_unified" for configuration "Release"
set_property(TARGET flare::flare_unified APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(flare::flare_unified PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/flarepy/libflare_unified.so"
  IMPORTED_SONAME_RELEASE "libflare_unified.so"
  )

list(APPEND _cmake_import_check_targets flare::flare_unified )
list(APPEND _cmake_import_check_files_for_flare::flare_unified "${_IMPORT_PREFIX}/flarepy/libflare_unified.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
