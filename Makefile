
vc_helpers=vc_array_functions.i  vc_arrays.i  vc_cast.i  vc_pointers.i

_vk.so : $(vc_helpers) vk.i util.o vc.h
	swig -Wall -python -o vk_python.c vk.i 
	gcc -c -fpic vk_python.c -I /usr/include/python3.9
	gcc -shared util.o vk_python.o -lvulkan -o _vk.so

util.o : util.c util.h
	gcc -c -fpic util.c

shader.spv: shader.comp
	glslc -c -Werror --target-spv=spv1.6 -o shader.spv shader.comp

test: shader.spv
	python VkComputeSample.py

clean:
	- rm *.o *.so
	- rm vk_python.c vk.py
