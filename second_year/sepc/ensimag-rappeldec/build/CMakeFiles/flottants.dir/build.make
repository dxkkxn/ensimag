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
include CMakeFiles/flottants.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/flottants.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/flottants.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/flottants.dir/flags.make

CMakeFiles/flottants.dir/src/flottants.c.o: CMakeFiles/flottants.dir/flags.make
CMakeFiles/flottants.dir/src/flottants.c.o: ../src/flottants.c
CMakeFiles/flottants.dir/src/flottants.c.o: CMakeFiles/flottants.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/flottants.dir/src/flottants.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/flottants.dir/src/flottants.c.o -MF CMakeFiles/flottants.dir/src/flottants.c.o.d -o CMakeFiles/flottants.dir/src/flottants.c.o -c /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/flottants.c

CMakeFiles/flottants.dir/src/flottants.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/flottants.dir/src/flottants.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/flottants.c > CMakeFiles/flottants.dir/src/flottants.c.i

CMakeFiles/flottants.dir/src/flottants.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/flottants.dir/src/flottants.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/src/flottants.c -o CMakeFiles/flottants.dir/src/flottants.c.s

# Object files for target flottants
flottants_OBJECTS = \
"CMakeFiles/flottants.dir/src/flottants.c.o"

# External object files for target flottants
flottants_EXTERNAL_OBJECTS =

flottants: CMakeFiles/flottants.dir/src/flottants.c.o
flottants: CMakeFiles/flottants.dir/build.make
flottants: CMakeFiles/flottants.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable flottants"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/flottants.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/flottants.dir/build: flottants
.PHONY : CMakeFiles/flottants.dir/build

CMakeFiles/flottants.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/flottants.dir/cmake_clean.cmake
.PHONY : CMakeFiles/flottants.dir/clean

CMakeFiles/flottants.dir/depend:
	cd /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/CMakeFiles/flottants.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/flottants.dir/depend

