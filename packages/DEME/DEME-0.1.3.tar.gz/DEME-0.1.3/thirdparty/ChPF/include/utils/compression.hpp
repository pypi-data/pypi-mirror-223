// Copyright (c) 2022, University of Wisconsin - Madison
// SPDX-License-Identifier: BSD-3-clause

#ifndef CHPF_COMPRESSION_HPP
#define CHPF_COMPRESSION_HPP

#include <iostream>
#include <vector>
#include <cstdint>
#include <memory>

#ifdef CHPF_HAS_ZLIB
#include <zlib.h> 
#endif

#ifdef CHPF_HAS_ZSTD
#include <zstd.h>
#endif

namespace chpf {

class Compressor {
public:

	Compressor() { 
		this->compression_done = false;
	}
	virtual ~Compressor() {};

	enum class Type {
		USE_DEFAULT = -1,
		NONE = 0,
		#ifdef CHPF_HAS_ZLIB
		ZLIB = 1,
		#endif
		#ifdef CHPF_HAS_ZSTD
		ZSTD = 2,
		#endif
	};
	
	inline bool eof() { return this->compression_done; }

	// Compress one "line" of data 
	virtual void compress(std::vector<uint8_t>& dest, std::vector<uint8_t>& src) = 0;

	// Check the status of the compressor 
	virtual bool good() = 0;

	// Compress any remaining buffered data while attempting to clean up the stream 
	virtual void finalize(std::vector<uint8_t>& dest) = 0;

protected:	
	
	bool compression_done; 
};


class CompressNone : public Compressor {
public:
	// The NONE compressor does not maintain any state of its own
	CompressNone() : Compressor() {};

	~CompressNone() {};
	
	inline bool good() { return true; } 

	inline void compress(std::vector<uint8_t>& dest, std::vector<uint8_t>& src) {
		// Copy output data directly from the source data
		dest.resize(src.size());
		dest.assign(src.begin(), src.end());
	}

	inline void finalize(std::vector<uint8_t>& dest) {
		dest.clear();
		this->compression_done = true;
	}

};


#ifdef CHPF_HAS_ZLIB
class CompressZlib : public Compressor {
public:

	static const size_t CHPF_ZLIB_BLOCK_SIZE = 16384;
	
	inline CompressZlib() : Compressor() {
		this->zstr.zalloc = Z_NULL;
		this->zstr.zfree = Z_NULL;
		this->zstr.opaque = Z_NULL;
		this->zstr.data_type = Z_BINARY;
		
		this->zlib_response = deflateInit(&this->zstr, Z_DEFAULT_COMPRESSION);
	}

	inline bool good() {
		return (this->zlib_response == Z_OK);
	}
	
	inline void compress(std::vector<uint8_t>& dest, std::vector<uint8_t>& src) {
		 
		size_t dest_index = 0;
		// The destination buffer must be large enough to hold an entire compressed block 
		dest.resize(CHPF_ZLIB_BLOCK_SIZE); 

		// Initialize a temporary buffer large enough to hold a chunk of compressed data 
		std::vector<uint8_t> compression_buf(CHPF_ZLIB_BLOCK_SIZE);
		
		// Tell zlib how much (and which) data we want to compress
		this->zstr.avail_in = src.size();
		this->zstr.next_in = reinterpret_cast<Bytef*>(&src[0]);
		
		do {
			// Inform the zlib context how much room there is for output
			this->zstr.avail_out = compression_buf.size();
			this->zstr.next_out = reinterpret_cast<Bytef*>(&compression_buf[0]);

			// Attempt to compress
			this->zlib_response = deflate(&this->zstr, Z_NO_FLUSH);

			if (this->zlib_response == Z_STREAM_ERROR) {
				std::cerr << "Internal Zlib error during compression!\n";
				break;
			}

			// If any of the available buffer space has been consumed, write out the data 
			if (this->zstr.avail_out != compression_buf.size()) {
				for (size_t i = 0; i < (compression_buf.size() - this->zstr.avail_out); i++) {
					dest[dest_index] = compression_buf[i];
					dest_index++;
					
					// If we're running low on space (<20% remaining), allocate more
					if (dest_index > ((dest.size() / 100) * 80)) {
						dest.resize(dest.size() + CHPF_ZLIB_BLOCK_SIZE); 
					}
				}
			}

		} while (this->zstr.avail_in != 0);

		// Shrink the output buffer to fit the amount of data that was copied out 
		dest.resize(dest_index);

	}

	inline void finalize(std::vector<uint8_t>& dest) {

		size_t dest_index = 0;
		// The destination buffer must be large enough to hold an entire compressed block 
		dest.resize(CHPF_ZLIB_BLOCK_SIZE);

		// Initialize a temporary buffer large enough to hold a chunk of compressed data 
		std::vector<uint8_t> compression_buf(CHPF_ZLIB_BLOCK_SIZE);

		do {
			this->zstr.avail_out = dest.size();
			this->zstr.next_out = reinterpret_cast<Bytef*>(&compression_buf[0]);

			this->zlib_response = deflate(&this->zstr, Z_FINISH);
			
			// If any of the available buffer space has been consumed, write out the data 
			if (this->zstr.avail_out != compression_buf.size()) {
				for (size_t i = 0; i < (compression_buf.size() - this->zstr.avail_out); i++) {
					dest[dest_index] = compression_buf[i];
					dest_index++;

					// If we're running low on space (<20% remaining), allocate more
					if (dest_index > ((dest.size() / 100) * 80)) {
						dest.resize(dest.size() + CHPF_ZLIB_BLOCK_SIZE);
					}
				}
			}
		
		} while (this->zlib_response != Z_STREAM_END);

		dest.resize(dest_index);
	
		deflateEnd(&this->zstr);

		// Set the flag that shows the compression completed successfully
		this->compression_done = true;
	} 

private:

	int zlib_response;
	z_stream zstr;

};
#endif


#ifdef CHPF_HAS_ZSTD
class CompressZstd : public Compressor {
public:

	// Consider setting this higher for multithreaded compression
	// (supported in newer zstd versions only) 
	static const size_t CHPF_ZSTD_WORKER_POOL = 0;
	
	// Arbitrarily chosen allocation size for buffer optimization
	static const size_t CHPF_ZSTD_WRITE_BLOCK_SIZE = 16384;

	inline CompressZstd() : Compressor() {
		
		// Initialize the compressor context 
		this->cctx = ZSTD_createCCtx();
		
		// We should check the context state here, but for simplicity's sake, 
		// we can let the next call throw a proper error code. 
		
		this->status = ZSTD_CCtx_setParameter(this->cctx, ZSTD_c_compressionLevel, ZSTD_defaultCLevel());
		if (!this->_check()) { return; }

		// Setting checksum is a good idea, according to the Zstd maintainers 
		this->status = ZSTD_CCtx_setParameter(this->cctx, ZSTD_c_checksumFlag, 1);
		if (!this->_check()) { return; }

		// Set the number of worker threads the compression engine should use (or 0 for fully synchronous)
		this->status = ZSTD_CCtx_setParameter(this->cctx, ZSTD_c_nbWorkers, CHPF_ZSTD_WORKER_POOL);
	};

	inline ~CompressZstd() {
		// Clean up the compression context, freeing its memory.
		ZSTD_freeCCtx(this->cctx);	
	} 

	// TODO: Add status check 
	inline bool good() { return (ZSTD_isError(this->status) == 0); };

	inline void compress(std::vector<uint8_t>& dest, std::vector<uint8_t>& src) {
		
		size_t dest_index = 0;
		dest.resize(CHPF_ZSTD_WRITE_BLOCK_SIZE);

		// The output buffer should be large enough to hold whatever 
		// the library thinks is the biggest amount of data that it can put 
		// out at once.
		std::vector<uint8_t> compression_buf(ZSTD_CStreamOutSize());

		// Data input structure (similar to Zlib's .*_in)
		ZSTD_inBuffer inbuf = { &src[0], src.size(), 0 };
		
		do {
			// Data output structure (similar to Zlib's .*_out)
			ZSTD_outBuffer outbuf = { &compression_buf[0], compression_buf.size(), 0 };

			// Perform compression
			this->status = ZSTD_compressStream2(this->cctx, &outbuf, &inbuf, ZSTD_e_continue);

			if (!this->_check()) {
				break;
			}

			// Write out any of the output buffer space that was consumed 
			if (outbuf.pos > 0) {
				for (size_t i = 0; i < outbuf.pos; i++) {
					dest[dest_index] = compression_buf[i];
					dest_index++;

					// If we're running low on space (<20% remaining), allocate more
					if (dest_index > ((dest.size() / 100) * 80)) {
						dest.resize(dest.size() + CHPF_ZSTD_WRITE_BLOCK_SIZE);
					}
				}
			}

		// NOTE: status, if not an error, will contain the number of remaining bytes
		} while (this->status > 0);

		// Truncate the output buffer to fit the amount of data that was actually copied out 
		dest.resize(dest_index);
	}


	inline void finalize(std::vector<uint8_t>& dest) {
		
		size_t dest_index = 0;
		dest.resize(CHPF_ZSTD_WRITE_BLOCK_SIZE);

		// The output buffer should be large enough to hold whatever 
		// the library thinks is the biggest amount of data that it can put 
		// out at once.
		std::vector<uint8_t> compression_buf(ZSTD_CStreamOutSize());

		// Create a throwaway source buffer so we don't pass NULL to Zstd 
		uint8_t dummy[1]; 

		// Data input structure (similar to Zlib's .*_in)
		ZSTD_inBuffer inbuf = { &dummy[0], 0, 0 };
		
		// This _should_ work in a single iteration, but I don't know the Zstd 
		// internals well enough to forgo the possibility of secretly buffered data.
		do {
			// Data output structure (similar to Zlib's .*_out)
			ZSTD_outBuffer outbuf = { &compression_buf[0], compression_buf.size(), 0 };

			// Perform compression
			this->status = ZSTD_compressStream2(this->cctx, &outbuf, &inbuf, ZSTD_e_end);

			if (!this->_check()) {
				break;
			}

			// Write out any of the output buffer space that was consumed 
			if (outbuf.pos > 0) {
				for (size_t i = 0; i < outbuf.pos; i++) {
					dest[dest_index] = compression_buf[i];
					dest_index++;

					// If we're running low on space (<20% remaining), allocate more
					if (dest_index > ((dest.size() / 100) * 80)) {
						dest.resize(dest.size() + CHPF_ZSTD_WRITE_BLOCK_SIZE);
					}
				}
			}

		// NOTE: status, if not an error, will contain the number of remaining bytes
		} while (this->status > 0);

		// Truncate the output buffer to fit the amount of data that was actually copied out 
		dest.resize(dest_index);

		this->compression_done = true;
	}

private:

	// Version of this->good() which also prints an error message. 
	inline bool _check() {
		if (ZSTD_isError(this->status)) {
			std::cerr << ZSTD_getErrorName(this->status) << "\n";
			return false;
		}
		return true;
	}

	size_t status;
	ZSTD_CCtx* cctx;

}; 
#endif


inline std::shared_ptr<Compressor> make_compressor(Compressor::Type type) {

	if (type == Compressor::Type::USE_DEFAULT) {
		#ifdef CHPF_HAS_ZSTD
			type = Compressor::Type::ZSTD;
		#elif defined(CHPF_HAS_ZLIB)
			type = Compressor::Type::ZLIB;
		#else
			type = Compressor::Type::NONE;
		#endif
	} 

	switch (type) {
		case Compressor::Type::NONE:
			return std::make_shared<CompressNone>();
		#ifdef CHPF_HAS_ZLIB
		case Compressor::Type::ZLIB:
			return std::make_shared<CompressZlib>();
		#endif
		#ifdef CHPF_HAS_ZSTD
		case Compressor::Type::ZSTD:
			return std::make_shared<CompressZstd>();
		#endif
		default:
			std::cout << "WARNING: Unsupported compression type! Skipping compression.\n";
			return std::make_shared<CompressNone>();
	}
}




} // namespace chpf;



#endif // CHPF_COMPRESSION_HPP

