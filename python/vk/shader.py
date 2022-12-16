#
# Copyright 2022 Tom Rix trix@redhat.com
#
import re
from vk import *

class vkShader:
    def __init__(self, device, buffers, comp, spv):
        self.d = device
        self.c = comp
        f = open(self.c, 'r')
        self.cc = f.read()
        f.close()
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
        num = self.bindings()
        p = new_paVkDescriptorSetLayoutBinding(num)
        b = VkDescriptorSetLayoutBinding()
        b.descriptorType  = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
        b.descriptorCount = 1
        b.stageFlags      = VK_SHADER_STAGE_COMPUTE_BIT
        b.stageFlags      = VK_SHADER_STAGE_ALL
        for i in range(0, num):
            b.binding     = i
            paVkDescriptorSetLayoutBinding_setitem(p, i, b)
        info              = VkDescriptorSetLayoutCreateInfo()
        info.sType        = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO
        info.bindingCount = num
        info.pBindings    = p
        pdsl = new_pVkDescriptorSetLayout()
        vkCreateDescriptorSetLayout(device, info, None, pdsl);
        info = VkPipelineLayoutCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO
        info.setLayoutCount = 1
        info.pSetLayouts = pdsl
        p = new_pVkPipelineLayout()
        vkCreatePipelineLayout(device, info, None, p)
        self.pipelineLayout = pVkPipelineLayout_value(p)
        info = VkComputePipelineCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO
        info.stage.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO
        info.stage.stage = VK_SHADER_STAGE_COMPUTE_BIT
        info.stage.module = self.v
        info.stage.pName = "main"
        info.layout = self.pipelineLayout
        p = new_pVkPipeline()
        vkCreateComputePipelines(device, None, 1, info, None, p)
        self.pipeline = pVkPipeline_value(p)
        ps = VkDescriptorPoolSize()
        ps.type = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
        ps.descriptorCount = num
        info = VkDescriptorPoolCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO
        info.maxSets = 1
        info.poolSizeCount = 1
        info.pPoolSizes =  ps.this
        p = new_pVkDescriptorPool()
        vkCreateDescriptorPool(device, info, None, p)
        v = pVkDescriptorPool_value(p)
        info = VkDescriptorSetAllocateInfo()
        info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO
        info.descriptorPool = v
        info.descriptorSetCount = 1
        info.pSetLayouts = pdsl
        self.descriptorSet = new_pVkDescriptorSet()
        vkAllocateDescriptorSets(device, info, self.descriptorSet)
        v = pVkDescriptorSet_value(self.descriptorSet)
        p = new_paVkWriteDescriptorSet(num)
        for i in range(0, num):
            info = VkDescriptorBufferInfo()
            info.buffer = buffers.v[i]
            info.offset = 0
            info.range = vk_whole_size()
            s = VkWriteDescriptorSet()
            s.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET
            s.dstSet = v
            s.dstBinding = i
            s.dstArrayElement = 0
            s.descriptorCount = 1
            s.descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
            s.pBufferInfo = info.this
            paVkWriteDescriptorSet_setitem(p, i, s)
        vkUpdateDescriptorSets(device, num, p, 0, None);

    def bindings(self):
        # layout(set = 0, binding = 0)
        m = re.findall(r'layout\(.*binding.*', self.cc)
        return len(m)
