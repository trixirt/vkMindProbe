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
from vk import *

class vkCommand:
    def __init__(self, device, queue):
        self.d = device
        self.cl = []
        info = VkCommandPoolCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO
        info.queueFamilyIndex = queue
        p = new_pVkCommandPool()
        vkClean.dust(self,[delete_pVkCommandPool, p])
        vkCreateCommandPool(device, info, None, p)
        v = pVkCommandPool_value(p)
        vkClean.dust(self, [vkDestroyCommandPool, self.d, v, None])
        info = VkCommandBufferAllocateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO
        info.commandPool = v
        info.level =  VK_COMMAND_BUFFER_LEVEL_PRIMARY
        info.commandBufferCount = 1
        self.p = new_pVkCommandBuffer()
        vkClean.dust(self, [delete_pVkCommandBuffer, self.p])
        vkAllocateCommandBuffers(device, info, self.p)
        vkClean.dust(self, [vkFreeCommandBuffers, self.d, info.commandPool, info.commandBufferCount, self.p])
        self.c = pVkCommandBuffer_value(self.p)
        p = new_pVkQueue()
        vkGetDeviceQueue(device, queue, 0, p)
        self.q = pVkQueue_value(p)

    def __del__(self):
        self.clean()

    def clean(self):
        vkClean.sweep(self)

    def begin(self, shader, x, y, z):
        info = VkCommandBufferBeginInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO
        info.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT
        vkBeginCommandBuffer(self.c, info)
        vkCmdBindPipeline(self.c, VK_PIPELINE_BIND_POINT_COMPUTE, shader.pipeline)
        vkCmdBindDescriptorSets(self.c, VK_PIPELINE_BIND_POINT_COMPUTE, shader.pipelineLayout, 0, 1, shader.descriptorSet, 0, None)
        vkCmdDispatch(self.c, x, y, z)
        vkEndCommandBuffer(self.c);

    def submit(self):
        info = VkSubmitInfo()
        info.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO
        info.commandBufferCount = 1
        info.pCommandBuffers = self.p
        vkQueueSubmit(self.q, 1, info, None)

    def end(self):
        vkQueueWaitIdle(self.q)
        

