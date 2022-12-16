#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkShader:
    def __init__(self, device, comp, spv):
        self.d = device
        self.c = comp
        self.cs = read_file(self.c, None, 0)
        self.cc = new_pauint32_t(self.cs)
        read_file(self.c, self.cc, self.cs)
        self.s = spv
        self.ss = read_file(self.s, None, 0)
        self.sc = new_pauint32_t(self.ss)
        read_file(self.s, self.sc, self.ss)
        info          = VkShaderModuleCreateInfo()
        info.sType    = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO
        info.codeSize = self.ss
        info.pCode    = self.sc
        p = new_pVkShaderModule()
        vkCreateShaderModule(self.d, info, None, p)
        self.v = pVkShaderModule_value(p)
