SPV = 	echo.spv \
	gemm_reference.spv \
	matm.spv \
	memset.spv

%.spv : %.comp
	glslc -c -Werror --target-spv=spv1.6 $< -o $@

all: $(SPV)

clean:
	- rm *.spv
