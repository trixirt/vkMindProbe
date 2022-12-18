#
# Copyright 2022 Tom Rix trix@redhat.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# glslc parser from
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import re
import shutil
import subprocess
from vk import *

class vkShader:
    def __init__(self, device, buffers, comp, spv):
        self.parser = None
        self.d = device
        self.b = buffers
        self.c = os.path.abspath(comp)
        self.s = os.path.abspath(spv)
        self.ss = 0
        self.sc = None
        self.v = None
        f = open(self.c, 'r')
        self.cc = f.read()
        f.close()
        self.cl = []
        self.create()
        self.build()

    def __del__(self):
        self.clean()

    def bind(self):
        num = self.bindings()
        p = new_paVkDescriptorSetLayoutBinding(num)
        self.cl.append([delete_paVkDescriptorSetLayoutBinding, p])
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
        self.cl.append([delete_pVkDescriptorSetLayout, pdsl])
        vkCreateDescriptorSetLayout(self.d, info, None, pdsl);
        v = pVkDescriptorSetLayout_value(pdsl)
        self.cl.append([vkDestroyDescriptorSetLayout, self.d, v, None])
        info = VkPipelineLayoutCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO
        info.setLayoutCount = 1
        info.pSetLayouts = pdsl
        p = new_pVkPipelineLayout()
        self.cl.append([delete_pVkPipelineLayout, p])
        vkCreatePipelineLayout(self.d, info, None, p)
        self.pipelineLayout = pVkPipelineLayout_value(p)
        self.cl.append([vkDestroyPipelineLayout, self.d, self.pipelineLayout, None])
        info = VkComputePipelineCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO
        info.stage.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO
        info.stage.stage = VK_SHADER_STAGE_COMPUTE_BIT
        info.stage.module = self.v
        info.stage.pName = "main"
        info.layout = self.pipelineLayout
        p = new_pVkPipeline()
        self.cl.append([delete_pVkPipeline, p])
        vkCreateComputePipelines(self.d, None, 1, info, None, p)
        self.pipeline = pVkPipeline_value(p)
        self.cl.append([vkDestroyPipeline, self.d, self.pipeline, None])
        ps = VkDescriptorPoolSize()
        ps.type = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
        ps.descriptorCount = num
        info = VkDescriptorPoolCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO
        info.maxSets = 1
        info.poolSizeCount = 1
        info.pPoolSizes =  ps.this
        p = new_pVkDescriptorPool()
        self.cl.append([delete_pVkDescriptorPool, p])
        vkCreateDescriptorPool(self.d, info, None, p)
        v = pVkDescriptorPool_value(p)
        self.cl.append([vkDestroyDescriptorPool, self.d, v, None])
        info = VkDescriptorSetAllocateInfo()
        info.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO
        info.descriptorPool = v
        info.descriptorSetCount = 1
        info.pSetLayouts = pdsl
        self.descriptorSet = new_pVkDescriptorSet()
        self.cl.append([delete_pVkDescriptorSet, self.descriptorSet])
        vkAllocateDescriptorSets(self.d, info, self.descriptorSet)
        self.cl.append([vkFreeDescriptorSets, self.d, v, 1, self.descriptorSet])
        v = pVkDescriptorSet_value(self.descriptorSet)
        p = new_paVkWriteDescriptorSet(num)
        for i in range(0, num):
            info = VkDescriptorBufferInfo()
            info.buffer = self.b.v[i]
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
        vkUpdateDescriptorSets(self.d, num, p, 0, None);

    def bindings(self):
        # layout(set = 0, binding = 0)
        m = re.findall(r'layout\(.*binding.*', self.cc)
        return len(m)
    
    def build(self, args=[]):
        if not self.v:
            return
        self.init_parser()
        self.args = self.parser.parse_args(args)
        if not os.path.isfile(self.args.glslc) or not os.access(self.args.glslc, os.X_OK):
            raise self.parser.error("Invalid glslc executable")

        # Base command for generating SPIR-V code
        command = [self.args.glslc, "-c", "--target-spv=spv1.6", "-fshader-stage=compute",
                   self.args.infile, "-o", self.args.outfile]
        if self.args.define:
            command.extend(self.args.define)
        if self.args.glslc_arg:
            command.extend(self.args.glslc_arg)

        if self.args.verbose:
            print("glslc command: '{}'".format(" ".join(command)))
        r = subprocess.check_output(command).decode("ascii")
        if self.args.verbose:
            print("result: '{}'".format(" ".join(r)))

        self.s = self.args.outfile
        self.ss = read_file(self.s, None, 0)
        self.create()

    def init_parser(self):
        if self.parser is None:
            self.parser = argparse.ArgumentParser(prog="vkShader::build")
            self.parser.add_argument(
                "-i",
                "--infile",
                metavar="<shader-source-file>",
                type=str,
                help="Input source code file",
                default=self.c)
            self.parser.add_argument(
                "-o",
                "--outfile",
                metavar="<spirv-output-file>",
                type=str,
                help="Output SPIR-V code file",
                default=self.s)
            self.parser.add_argument(
                "-d",
                "--define",
                metavar="<macro>",
                type=str,
                action="append",
                help="A #define in the format of 'FOO=BAR'")
            self.parser.add_argument(
                "-g",
                "--glslc",
                metavar="<glslc-executable>",
                type=str,
                help="Path to glslc executable",
                default=shutil.which('glslc'))
            self.parser.add_argument(
                "-a",
                "--glslc-arg",
                metavar="<glslc-arg>",
                type=str,
                action="append",
                help="Additional arguments to pass to glslc")
            self.parser.add_argument(
                "-v",
                "--verbose",
                action="store_true",
                help="Print in verbose mode")

    def clean(self):
        if self.cl == None:
            return
        for c in reversed(self.cl):
            l = len(c)
            if l == 2:
                c[0](c[1])
            elif l == 3:
                c[0](c[1], c[2])
            elif l == 4:
                c[0](c[1], c[2], c[3])
            elif l == 5:
                c[0](c[1], c[2], c[3], c[4])
        self.cl.clear()

    def create(self):
        self.clean()
        self.ss = read_file(self.s, None, 0)
        if self.ss > 0:
            self.sc = new_pauint32_t(self.ss)
            self.cl.append([delete_puint32_t, self.sc])
            read_file(self.s, self.sc, self.ss)
            info          = VkShaderModuleCreateInfo()
            info.sType    = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO
            info.codeSize = self.ss
            info.pCode    = self.sc
            p = new_pVkShaderModule()
            self.cl.append([delete_pVkShaderModule, p])
            vkCreateShaderModule(self.d, info, None, p)
            self.v = pVkShaderModule_value(p)
            self.cl.append([vkDestroyShaderModule, self.d, self.v, None])
            self.bind()

