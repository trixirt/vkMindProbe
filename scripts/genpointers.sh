#!/bin/sh
set -x
rm _vc_pointers.i
rm _vc_arrays.i
rm _vc_array_functions.i
rm _vc_cast.i
T=`grep '* p' vc.h | sort -u | awk '{ print $1 }' | sort -u | tr -d '*' | sort -u`
M=`grep typedef vc.h | grep struct | sort -u | awk '{ print $3 }' | grep -v _T`
T="float double int8_t int16_t int32_t int64_t uint8_t uint16_t uint32_t uint64_t VkInstance $T"
T="$T $M"
for t in $T; do
    echo "%pointer_functions(${t}, p${t});" >> _vc_pointers.i
    echo "%allocators(${t}, p${t});" >> _vc_pointers.i
    echo "%pointer_cast(void *, ${t} *, void_to_${t});" >> _vc_cast.i
    echo "%pointer_cast(${t} *, void *, ${t}_to_void);" >> _vc_cast.i
done
for t in $T; do
    echo "%array_class(${t}, a${t});" >> _vc_arrays.i
done
for t in $T; do
    echo "%array_functions(${t}, pa${t});" >> _vc_array_functions.i
done

sort -u _vc_pointers.i > s
mv s _vc_pointers.i
sort -u _vc_arrays.i > s
mv s _vc_arrays.i
sort -u _vc_array_functions.i > s
mv s _vc_array_functions.i
sort -u _vc_cast.i > s
mv s _vc_cast.i

