# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.21

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build

# Include any dependencies generated for this target.
include CMakeFiles/ensigc.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/ensigc.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ensigc.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ensigc.dir/flags.make

CMakeFiles/ensigc.dir/src/elempool.c.o: CMakeFiles/ensigc.dir/flags.make
CMakeFiles/ensigc.dir/src/elempool.c.o: ../src/elempool.c
CMakeFiles/ensigc.dir/src/elempool.c.o: CMakeFiles/ensigc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/ensigc.dir/src/elempool.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/ensigc.dir/src/elempool.c.o -MF CMakeFiles/ensigc.dir/src/elempool.c.o.d -o CMakeFiles/ensigc.dir/src/elempool.c.o -c /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/elempool.c

CMakeFiles/ensigc.dir/src/elempool.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ensigc.dir/src/elempool.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/elempool.c > CMakeFiles/ensigc.dir/src/elempool.c.i

CMakeFiles/ensigc.dir/src/elempool.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ensigc.dir/src/elempool.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/elempool.c -o CMakeFiles/ensigc.dir/src/elempool.c.s

CMakeFiles/ensigc.dir/src/bitset1000.cpp.o: CMakeFiles/ensigc.dir/flags.make
CMakeFiles/ensigc.dir/src/bitset1000.cpp.o: ../src/bitset1000.cpp
CMakeFiles/ensigc.dir/src/bitset1000.cpp.o: CMakeFiles/ensigc.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/ensigc.dir/src/bitset1000.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/ensigc.dir/src/bitset1000.cpp.o -MF CMakeFiles/ensigc.dir/src/bitset1000.cpp.o.d -o CMakeFiles/ensigc.dir/src/bitset1000.cpp.o -c /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/bitset1000.cpp

CMakeFiles/ensigc.dir/src/bitset1000.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ensigc.dir/src/bitset1000.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/bitset1000.cpp > CMakeFiles/ensigc.dir/src/bitset1000.cpp.i

CMakeFiles/ensigc.dir/src/bitset1000.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ensigc.dir/src/bitset1000.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/bitset1000.cpp -o CMakeFiles/ensigc.dir/src/bitset1000.cpp.s

# Object files for target ensigc
ensigc_OBJECTS = \
"CMakeFiles/ensigc.dir/src/elempool.c.o" \
"CMakeFiles/ensigc.dir/src/bitset1000.cpp.o"

# External object files for target ensigc
ensigc_EXTERNAL_OBJECTS =

libensigc.so: CMakeFiles/ensigc.dir/src/elempool.c.o
libensigc.so: CMakeFiles/ensigc.dir/src/bitset1000.cpp.o
libensigc.so: CMakeFiles/ensigc.dir/build.make
libensigc.so: CMakeFiles/ensigc.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libensigc.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ensigc.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ensigc.dir/build: libensigc.so
.PHONY : CMakeFiles/ensigc.dir/build

CMakeFiles/ensigc.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ensigc.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ensigc.dir/clean

CMakeFiles/ensigc.dir/depend:
	cd /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles/ensigc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ensigc.dir/depend

