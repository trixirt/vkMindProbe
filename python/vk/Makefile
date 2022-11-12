
vc_helpers=../../swig/vc_array_functions.i  ../../swig/vc_arrays.i  ../../swig/vc_cast.i  ../../swig/vc_pointers.i

_vk.so : ../../src/util.o vk_python.o
	gcc -shared $^ -lvulkan -o $@

vk_python.c : $(vc_helpers) ../../swig/vk.i ../../swig/vc.h
	swig -Wall -python -I../../include -o $@ ../../swig/vk.i

vk_python.o : vk_python.c
	gcc -c -fpic -I /usr/include/python3.9 -I ../../include $^ -o $@

clean:
	- rm *.o *.so
	- rm vk_python.c vk.py
	- rm -rf __pycache__
