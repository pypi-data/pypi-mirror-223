// Copyright (c) 2022, University of Wisconsin - Madison
// SPDX-License-Identifier: BSD-3-clause


#ifndef CHPF_TYPES_H
#define CHPF_TYPES_H

// Automatically handle the presence of the half precision type from CUDA
#if defined(__NVCC__) && !defined(CHPF_HAS_FLOAT16) 
	#define CHPF_HAS_FLOAT16 half
#endif

// If no half precision floating point type was defined, let it be void. 
#ifndef CHPF_HAS_FLOAT16
	#define CHPF_HAS_FLOAT16 void
#endif

// Define the type chpf_half_t with whatever float16 type is available 
typedef CHPF_HAS_FLOAT16 chpf_half_t;

// Set a default optimal block size 
#ifndef CHPF_OPTIMIZED_BLOCK_SIZE
#define CHPF_OPTIMIZED_BLOCK_SIZE 512 
#endif

#endif // CHPF_TYPES_H

