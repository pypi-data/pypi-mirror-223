// Copyright (c) 2021, University of Wisconsin - Madison
// SPDX-License-Identifier: BSD-3-clause

#include <fstream>
#include <vector>

// Compile with -DCHPF_USE_ZLIB to enable Zlib compression and tests
#include <chpf.hpp>

int main(int argc, char** argv) {

	std::vector<char> c {'a', 'b', 'c', 'd'};
	std::vector<int>  i {5, 6, 7, 8};
	std::vector<long> l {9l, 10l, 11l, 12l};

	std::ofstream output_file("test.chpf", std::ios_base::binary);
	chpf::Writer pw;

	pw.write(output_file, chpf::Compressor::Type::NONE, {}, c, i, l);
	
	#ifdef CHPF_HAS_ZLIB
	std::ofstream output_file2("test2.chpf", std::ios_base::binary);
	pw.write(output_file2, chpf::Compressor::Type::ZLIB, {}, c, i, l);
	#endif

	#ifdef CHPF_HAS_ZSTD
	std::ofstream output_file3("test3.chpf", std::ios_base::binary);
	pw.write(output_file3, chpf::Compressor::Type::ZSTD, {"some char", "some int", "some long"}, c, i, l);
	#endif

	return 0;
}
