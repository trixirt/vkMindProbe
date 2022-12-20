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

class vkMemory:
    def __init__(self, device, memoryIndex):
        self.cl = []
        self.d = device
        self.i = memoryIndex
        self.s = 0

    def __del__(self):
        self.clean()

    def clean(self):
        vkClean.sweep(self)

    def allocate(self, size):
        if size > self.s:
            self.clean()
            self.s = size
            info = VkMemoryAllocateInfo()
            info.sType           = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO
            info.allocationSize  = self.s
            info.memoryTypeIndex = self.i
            p = new_pVkDeviceMemory()
            vkClean.dust(self, [delete_pVkDeviceMemory, p])
            vkAllocateMemory(self.d, info, None, p)
            v = pVkDeviceMemory_value(p)
            vkClean.dust(self, [vkFreeMemory, self.d, v, None])
            self.v = v

    def map(self, data, size, offset = 0, flags = 0):
        vkMapMemory(self.d, self.v, offset, size, flags, data)

    def unmap(self):
        vkUnmapMemory(self.d, self.v)
