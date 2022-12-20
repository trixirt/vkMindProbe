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

class vkBuffer:
    def __init__(self, device, memory, queue):
        self.v = []
        self.d = device
        self.m = memory
        self.q = queue
        self.s = []
        self.o = []
        self.cl = []
        self.pq = new_puint32_t()
        puint32_t_assign(self.pq, queue)

    def __del__(self):
        delete_puint32_t(self.pq)

    def allocate(self, size):
        self.clean()
        self.s = size
        self.o = []
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
            self.cl.append([delete_pVkBuffer, p])
            vkCreateBuffer(self.d, info.this, None, p)
            v = pVkBuffer_value(p)
            self.cl.append([vkDestroyBuffer, self.d, v, None])
            if o != 0:
                p = new_pVkMemoryRequirements()
                self.cl.append([delete_pVkMemoryRequirements, p])
                vkGetBufferMemoryRequirements(self.d, v, p)
                m = pVkMemoryRequirements_value(p)
                a = m.alignment
                print(o)
                if (o % a):
                    o = o + (a - (o % a))
            vkBindBufferMemory(self.d, v, self.m, o)
            self.o.append(o)
            o += s
            self.v.append(v)

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

    def extent(self):
        r = 0
        i = len(self.s)
        if i > 0:
            i = i - 1
            r = self.s[i] + self.o[i]
        return r
