#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkMemory:
    def __init__(self, device, memoryIndex, size):
        self.d = device
        self.i = memoryIndex
        self.s = size
    def allocate(self):
        info = VkMemoryAllocateInfo()
        info.sType           = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO
        info.allocationSize  = self.s
        info.memoryTypeIndex = self.i
        p = new_pVkDeviceMemory()
        vkAllocateMemory(self.d, info, None, p)
        v = pVkDeviceMemory_value(p)
        self.v = v
    def map(self, offset, size, flags, data):
        vkMapMemory(self.d, self.v, offset, size, flags, data)
    def unmap(self):
        vkUnmapMemory(self.d, self.v)
