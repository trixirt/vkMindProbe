%module vk
%{
typedef unsigned int uint32_t;
typedef long unsigned int uint64_t;

#include <vulkan/vulkan.h>
// helpers
#include "util.h"

%}

typedef unsigned int uint32_t;
typedef long unsigned int uint64_t;

%include "typemaps.i"
%include "cpointer.i"
%include "carrays.i"
%include "cmalloc.i"
%include "cdata.i"
%include "vc.h"
// helpers
%include "util.h"

/* pointer helpers */
%include "vc_pointers.i"
%include "vc_arrays.i"
%include "vc_array_functions.i"
%include "vc_cast.i"
