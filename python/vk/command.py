#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkCommand:
    def __init__(self, device, queue):
        info = VkCommandPoolCreateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO
        info.queueFamilyIndex = queue
        p = new_pVkCommandPool()
        vkCreateCommandPool(device, info, None, p)
        v = pVkCommandPool_value(p)
        info = VkCommandBufferAllocateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO
        info.commandPool = v
        info.level =  VK_COMMAND_BUFFER_LEVEL_PRIMARY
        info.commandBufferCount = 1
        self.p = new_pVkCommandBuffer()
        vkAllocateCommandBuffers(device, info, self.p)
        self.c = pVkCommandBuffer_value(self.p)
        p = new_pVkQueue()
        vkGetDeviceQueue(device, queue, 0, p)
        self.q = pVkQueue_value(p)

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
        

