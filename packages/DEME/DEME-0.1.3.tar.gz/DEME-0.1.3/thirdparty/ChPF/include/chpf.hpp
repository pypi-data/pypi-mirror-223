// Copyright (c) 2021, University of Wisconsin - Madison
// SPDX-License-Identifier: BSD-3-clause

#include <cstdint>
#ifndef CHPF_WRITER_HPP
#define CHPF_WRITER_HPP 1

#include <iostream>
#include <fstream>
#include <array>
#include <string>
#include <vector>
#include <type_traits>
#include <functional>

#include <utils/types.h>
#include <utils/compression.hpp>


namespace chpf {

class Writer {
public:

	const uint16_t CHPF_DEFAULT_VERSION = 2;

	enum class FieldType {
		INT8 = 0,
		INT16,
		INT32,
		INT64,
		UINT8,
		UINT16,
		UINT32,
		UINT64,
		HALF,
		FLOAT,
		DOUBLE,
		UNKNOWN
	};

	// ChPF v3 Header Flags
	static constexpr uint16_t HEADER_FLAG_KEYS = (1 << 1); // Set when a list of keys is expected to follow the header 

	
	template <typename... Ts>
	struct ChPFHeader {
		const uint8_t magic[4] = {0x43, 0x68, 0x50, 0x46}; // UTF-8 letters 'C' 'h' 'P' 'F' 0x46506843
		uint16_t version = 1;
		uint16_t flags = 0;
		uint32_t header_size = 0;
		uint32_t num_keys = 0;
		uint16_t types[sizeof...(Ts)] = {0};
		uint16_t compression = 0;
	};

	template <typename... Ts>
	constexpr struct ChPFHeader<Ts...> buildHeaderV1() {
		struct ChPFHeader<Ts...> pfh;
		pfh.version = 1;
		pfh.header_size = sizeof(ChPFHeader<Ts...>);
		pfh.num_keys = sizeof...(Ts);
		
		// Do some templated type detection in the weirdest way possible
		std::array<bool, sizeof...(Ts)> int8s { std::is_same<int8_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> int16s { std::is_same<int16_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> int32s { std::is_same<int32_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> int64s { std::is_same<int64_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> uint8s { std::is_same<uint8_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> uint16s { std::is_same<uint16_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> uint32s { std::is_same<uint32_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> uint64s { std::is_same<uint64_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> halfs { std::is_same<chpf_half_t, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> floats { std::is_same<float, typename std::remove_reference<Ts>::type::value_type>::value... };
		std::array<bool, sizeof...(Ts)> doubles { std::is_same<double, typename std::remove_reference<Ts>::type::value_type>::value... };

		std::array<bool, sizeof...(Ts)> chars { std::is_same<char, typename std::remove_reference<Ts>::type::value_type>::value... };

		// Store the detected types into their enum counterparts
		for (size_t i = 0; i < sizeof...(Ts); i++) {
			if (int8s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::INT8);
			}
			else if (int16s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::INT16);
			}
			else if (int32s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::INT32);
			}
			else if (int64s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::INT64);
			}
			else if (uint8s[i] || chars[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::UINT8);
			}
			else if (uint16s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::UINT16);
			}
			else if (uint32s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::UINT32);
			}
			else if (uint64s[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::UINT64);
			}
			else if (halfs[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::HALF);
			}
			else if (floats[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::FLOAT);
			}
			else if (doubles[i]) {
				pfh.types[i] = static_cast<uint16_t>(FieldType::DOUBLE);
			}
			else {
				pfh.types[i] = static_cast<uint16_t>(FieldType::UNKNOWN);
			}
		}

		return pfh;
	}

	template <typename... Ts>
	constexpr struct ChPFHeader<Ts...> buildHeaderV2(Compressor::Type compression) {
		auto pfh = buildHeaderV1<Ts...>();
		pfh.version = 2;
		pfh.compression = static_cast<uint16_t>(compression);
		return pfh;
	}

	template <typename... Ts>
	constexpr struct ChPFHeader<Ts...> buildHeaderV3(Compressor::Type compression, uint16_t flags = 0) {
		auto pfh = buildHeaderV2<Ts...>(compression);
		pfh.version = 3;
		pfh.flags = flags;	
		return pfh;
	}

	// template <typename... Ts>
	// auto getHeaderGeneratorByVersion(uint16_t version) {
	// 	switch(version) {
	// 		case 1:
	// 			return &buildHeaderV1;
	// 		#ifdef CHPF_USE_ZLIB
	// 		case 2:
	// 			return &buildHeaderV2;
	// 		#endif
	// 		default:
	// 			std::cerr << "Version not supported!";
	// 			return std::function<decltype(buildHeaderV1<Ts...>)>();
	// 	}
	// }

	template <typename... Ts>
	constexpr size_t getRowSize() {
		// Create an array using a parameter expansion
		std::array<size_t, sizeof...(Ts)> sizes { sizeof(typename std::remove_reference<Ts>::type::value_type)... };

		size_t accumulator = 0;
		for (size_t i = 0; i < sizeof...(Ts); i++) {
			accumulator += sizes[i];
		}
		
		return accumulator;
	}

	template <typename T, typename Allocator>
	inline void repackParams(std::vector<uint8_t>& streambuf, size_t offset, const size_t idx, const std::vector<T, Allocator>& v)
	{
		for (size_t byte = 0; byte < sizeof(T); byte++) {
			streambuf[offset + byte] = *(reinterpret_cast<const char*>(&v[idx]) + byte);
		}
	}

	template <typename T, typename Allocator, typename... Ts>
	inline void repackParams(std::vector<uint8_t>& streambuf, size_t offset, const size_t idx, const std::vector<T, Allocator>& v, Ts&& ... args) {
		
		for (size_t byte = 0; byte < sizeof(T); byte++) {
			streambuf[offset + byte] = *(reinterpret_cast<const char*>(&v[idx]) + byte);
		}

		offset += sizeof(T);
		repackParams(streambuf, offset, idx, std::forward<Ts>(args)...);
	}

	template <typename T, typename Allocator = std::allocator<T>, typename... Ts>
	void write(std::ostream& stream, Compressor::Type compression, const std::vector<std::string>& keys, const std::vector<T, Allocator>& v, Ts&&... args) {
		
		uint16_t header_flags = 0;
		if (keys.size() > 0) {
			header_flags |= HEADER_FLAG_KEYS;
		}


		// Generate a Chrono Particle Format Header and write it to a file, 
		// then pad it to some multiple of CHPF_OPTIMIZED_BLOCK_SIZE bytes.
		auto header = buildHeaderV3<decltype(v), Ts...>(compression, header_flags);
		uint16_t header_size_orig = header.header_size;

		// Add the size of keys (including terminators) to the expected size of the header. 
		for (auto it = keys.cbegin(); it != keys.cend(); it++) {
			header.header_size += it->length() + 1;
		} 

		uint16_t header_size_padding = CHPF_OPTIMIZED_BLOCK_SIZE - header.header_size % CHPF_OPTIMIZED_BLOCK_SIZE;
		
		// Set the size saved in the file to include the padding
		header.header_size += header_size_padding;
		
		// Exit before writing anything if the stream isn't sane
		if (!stream.good()) {
			return;
		}

		// Write the header (struct only)
		stream.write(reinterpret_cast<char*>(&header), header_size_orig);

		for (auto it = keys.cbegin(); it != keys.cend(); it++) {
			// Write each key AND its null terminator 
			stream.write(
				reinterpret_cast<const char*>(it->c_str()), 
				it->length() + 1
			);
		}
		
		// Write the header's padding
		std::vector<char> padding(header_size_padding);
		stream.write(padding.data(), padding.size());

		std::shared_ptr<Compressor> compression_engine = make_compressor(compression);
		if (!compression_engine->good()) {
			std::cerr << "ERROR: Compression engine failed during initialization!\n";
			return;
		}

		// Declare buffers for sending to and receiving data from the compressor 
		std::vector<uint8_t> row_buffer(getRowSize<decltype(v), Ts...>());
		std::vector<uint8_t> compressed_data;

		// TODO: Consider unrolling this loop and sending a larger block of data to 
		// 	     the compressor. Zstd (and possibly other algorithms) may be 
		// 	     throttled by excessively small buffers. 
		for (size_t i = 0; i < v.size(); i++) {
			repackParams(row_buffer, 0, i, v, std::forward<Ts>(args)...);
			
			compression_engine->compress(compressed_data, row_buffer);

			// Validate that the stream and compression engine are still sane 
			if (!compression_engine->good() || !stream.good()) {
				return;
			}
			
			// Write whatever data was received to the output stream
			stream.write(reinterpret_cast<char*>(compressed_data.data()), compressed_data.size());
		}


		// Finish compressing whatever data is left in the engine's internal buffers
		compression_engine->finalize(compressed_data);

		// Validate that the stream and compression engine are still in their expected states 
		if (!compression_engine->eof() || !stream.good()) {
			return;
		}

		stream.write(reinterpret_cast<char*>(compressed_data.data()), compressed_data.size());

	}

};

} // namespace chpf; 

#endif
