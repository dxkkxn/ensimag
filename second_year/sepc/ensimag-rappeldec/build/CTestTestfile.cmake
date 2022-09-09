# CMake generated Testfile for 
# Source directory: /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec
# Build directory: /user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test([=[ListeChainee]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/listechainee")
set_tests_properties([=[ListeChainee]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;57;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[valgrindListeChainee]=] "valgrind" "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/listechainee")
set_tests_properties([=[valgrindListeChainee]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;58;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[GC]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/ensitestgc" "--all")
set_tests_properties([=[GC]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;60;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[ValgrindGC]=] "valgrind" "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/ensitestgc" "--all")
set_tests_properties([=[ValgrindGC]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;61;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[Binaire]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/../tests/binairestests.rb")
set_tests_properties([=[Binaire]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;63;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[Hello]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/../tests/hellotests.rb")
set_tests_properties([=[Hello]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;65;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[Flottants]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/../tests/flottantstests.rb")
set_tests_properties([=[Flottants]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;67;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[TriComplexe]=] "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/fqsort")
set_tests_properties([=[TriComplexe]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;69;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
add_test([=[valgrindTriComplexe]=] "valgrind" "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/build/fqsort")
set_tests_properties([=[valgrindTriComplexe]=] PROPERTIES  _BACKTRACE_TRIPLES "/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;70;add_test;/user/1/benjelly/ensimag/second_year/sepc/ensimag-rappeldec/CMakeLists.txt;0;")
