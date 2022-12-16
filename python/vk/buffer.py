#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkBuffer:
    def __init__(self, device, memory, queue):
        self.v = []
        self.d = device
        self.m = memory
        self.q = queue
        self.pq = new_puint32_t()
        puint32_t_assign(self.pq, queue)
    def allocate(self, size):
        self.s = size
        info                       = VkBufferCreateInfo()
        info.sType                 = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO
        info.usage                 = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT
        info.sharingMode           = VK_SHARING_MODE_EXCLUSIVE
        info.queueFamilyIndexCount = 1
        info.pQueueFamilyIndices   = self.pq
        o = 0
        for s in self.s:
            info.size = s
            p = new_pVkBuffer()
            vkCreateBuffer(self.d, info.this, None, p)
            v = pVkBuffer_value(p)
            vkBindBufferMemory(self.d, v, self.m, o)
            o += s
            self.v.append(v)
