
vc_helpers=../swig/vc_array_functions.i  ../swig/vc_arrays.i  ../swig/vc_cast.i  ../swig/vc_pointers.i

_vk.so : $(vc_helpers) ../swig/vk.i ../src/util.o ../swig/vc.h
	swig -Wall -python -I../include -o vk_python.c ../swig/vk.i
	gcc -c -fpic vk_python.c -I /usr/include/python3.9 -I ../include
	gcc -shared ../src/util.o vk_python.o -lvulkan -o _vk.so

test: _vk.so ../shader/echo.spv
	python VkComputeSample.py

clean:
	- rm *.o *.so
	- rm vk_python.c vk.py
