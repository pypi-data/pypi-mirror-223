# Copyright (c) 2022, University of Wisconsin - Madison
# SPDX-License-Identifier: BSD-3-clause

# ---------------------------------------------------------------------------- #
# Project Settings
# ---------------------------------------------------------------------------- #

cmake_minimum_required(VERSION 3.14)

# Version Information
set(VERSION_MAJOR 3)
set(VERSION_MINOR 0)

project(
	ChPF
	VERSION ${VERSION_MAJOR}.${VERSION_MINOR}
	LANGUAGES CXX
)


option(USE_ZLIB "If set, enable Zlib compression in ChPF" OFF)
option(USE_ZSTD "If set, enable ZSTD compression in ChPF" OFF)

# ---------------------------------------------------------------------------- #
# Additional Components 
# ---------------------------------------------------------------------------- #

include(cmake/FixNinjaColors.cmake)
fix_ninja_colors()

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

if (USE_ZLIB)
	find_package(ZLIB REQUIRED)
endif()

if (USE_ZSTD)
	if (UNIX)
		include(FindPkgConfig)
		if (PKG_CONFIG_FOUND)
			pkg_check_modules(
				ZSTD REQUIRED 
				IMPORTED_TARGET
				libzstd
			)
		else()
			message(SEND_ERROR "USE_ZSTD was selected, but no pkg-config binary was found!")
		endif()
	else()
		message(SEND_ERROR "Zstd configuration requires pkg-config, this will fail on non-UNIX systems! Zlib is recommended instead.")
	endif()
endif()

# ---------------------------------------------------------------------------- #
# ChPF Library 
# ---------------------------------------------------------------------------- #

add_library(ChPF INTERFACE)

set(CHPF_LIBRARIES)

if(ZLIB_FOUND)
	target_link_libraries(
		ChPF
		INTERFACE ZLIB::ZLIB
	)
	target_compile_definitions(
		ChPF 
		INTERFACE -DCHPF_USE_ZLIB
		INTERFACE -DCHPF_HAS_ZLIB
	)
endif()

if(ZSTD_FOUND)
	target_link_libraries(
		ChPF
		INTERFACE PkgConfig::ZSTD
	)
	target_compile_definitions(
		ChPF
		INTERFACE -DCHPF_HAS_ZSTD
	)
endif()

target_include_directories(
	ChPF
	INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/include> $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>

)


# ---------------------------------------------------------------------------- #
# ChPF Smoke-Test
# ---------------------------------------------------------------------------- #

add_executable(test_chpf)

target_link_libraries(test_chpf 
	PUBLIC ChPF
)


target_sources(
	test_chpf
	PUBLIC test_driver.cpp
)


# ---------------------------------------------------------------------------- #
# Installation
# ---------------------------------------------------------------------------- #


# Install ChPF headers 
install(
	DIRECTORY include
	DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
	FILES_MATCHING
		PATTERN "*.h"
		PATTERN "*.hpp"
)

# Create a blank target for the library 
install(TARGETS ChPF EXPORT ChPFTargets)

# Generate the export file (build tree)
export(
	EXPORT ChPFTargets
	FILE "${CMAKE_CURRENT_BINARY_DIR}/ChPF/ChPFTargets.cmake"
	NAMESPACE ChPF::
)

# Set the install location for the export file
install(
	EXPORT ChPFTargets
	DESTINATION
		${CMAKE_INSTALL_LIBDIR}/cmake/ChPF
	NAMESPACE ChPF::
)


# This macro is used in the Config.cmake file (build tree) 
set (CONF_INCLUDE_DIRS "${CMAKE_SOURCE_DIR}/include")

# Generate ChPFConfig.cmake (build tree)
configure_file(cmake/ChPFConfig.cmake.in
	"${CMAKE_CURRENT_BINARY_DIR}/ChPF/ChPFConfig.cmake"
	@ONLY
)


# These macros are used in the Config.cmake file (install tree)
file(RELATIVE_PATH REL_INCLUDE_DIR "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/cmake/ChPF" "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_INCLUDEDIR}")
set (CONF_INCLUDE_DIRS "\${ChPFCMakeDir}/${REL_INCLUDE_DIR}")

# Generate ChPFConfig.cmake (install tree), placing it in CMAKE_FILES_DIRECTORY to isolate it from the build tree 
configure_file(cmake/ChPFConfig.cmake.in
	"${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/ChPFConfig.cmake"
	@ONLY
)


# Automatically generate the ConfigVersion.cmake file
write_basic_package_version_file(
	${CMAKE_CURRENT_BINARY_DIR}/ChPF/ChPFConfigVersion.cmake
	VERSION ${VERSION_MAJOR}.${VERSION_MINOR}
	COMPATIBILITY AnyNewerVersion
)


# Set install locations for generated config files
install(
	FILES
	        "${CMAKE_CURRENT_BINARY_DIR}/ChPF/ChPFConfig.cmake"
		"${CMAKE_CURRENT_BINARY_DIR}/ChPF/ChPFConfigVersion.cmake"
	DESTINATION
		${CMAKE_INSTALL_LIBDIR}/cmake/ChPF
)





