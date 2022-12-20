#
# Copyright 2022 Tom Rix trix@redhat.com
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
        self.cl.append([delete_pVkCommandPool, p])
        vkCreateCommandPool(device, info, None, p)
        v = pVkCommandPool_value(p)
        self.cl.append([vkDestroyCommandPool, self.d, v, None])
        info = VkCommandBufferAllocateInfo()
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO
        info.commandPool = v
        info.level =  VK_COMMAND_BUFFER_LEVEL_PRIMARY
        info.commandBufferCount = 1
        self.p = new_pVkCommandBuffer()
        self.cl.append([delete_pVkCommandBuffer, self.p])
        vkAllocateCommandBuffers(device, info, self.p)
        self.cl.append([vkFreeCommandBuffers, self.d, info.commandPool, info.commandBufferCount, self.p])
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

    def submit(self):
        info = VkSubmitInfo()
        info.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO
        info.commandBufferCount = 1
        info.pCommandBuffers = self.p
        vkQueueSubmit(self.q, 1, info, None)

    def end(self):
        vkQueueWaitIdle(self.q)
        

