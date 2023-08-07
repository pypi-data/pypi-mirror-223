# Installable ChPFConfig.cmake (base file) 
#
# Provides the following package variables:
#
# ChPF_INCLUDE_DIRS
# ChPF_LIBRARIES
#
# Additionally, ChPF may require the following libraries: 
#	On all platforms: 
#	- ZLIB::ZLIB
#	On Unix-like platforms:
#	- PkgConfig::ZSTD
# 

cmake_path(GET CMAKE_CURRENT_LIST_FILE PARENT_PATH ChPFCMakeDir)

if (NOT TARGET ChPF AND NOT ChPF_BINARY_DIR)
	include("${ChPFCMakeDir}/ChPFTargets.cmake")
endif()


set(ChPF_INCLUDE_DIRS /DEM-Engine/thirdparty/ChPF/include)
set(ChPF_LIBRARIES ChPF::ChPF)

