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

class vkSpecialization:
    def __init__(self):
        self.cl = []
        self.l = []
        self.p = None
        
    def __del__(self):
        self.clean()

    def append(self, d, s, i):
        self.l.append([d, s, i])

    def bind(self):
        self.clean()
        if len(self.l):
            self.p = new_pVkSpecializationInfo()
            vkClean.dust(self, [delete_pVkSpecializationInfo, self.p])
            v = VkSpecializationInfo()
            v.mapEntryCount = len(self.l)
            pa = new_paVkSpecializationMapEntry(v.mapEntryCount);
            vkClean.dust(self, [delete_paVkSpecializationMapEntry, pa])
            v.pMapEntries = pa.this
            s = 0
            for l in self.l:
                s = s + l[1]
            self
            v.dataSize = s
            p = new_pauint8_t(s)
            vkClean.dust(self, [delete_pauint8_t, p])
            d = uint8_t_to_void(p)
            v.pData = d
            pVkSpecializationInfo_assign(self.p, v)
            o = 0
            i = 0
            for l in self.l:
                v = VkSpecializationMapEntry()
                v.constantID = l[2]
                v.offset = o
                v.size = l[1]
                paVkSpecializationMapEntry_setitem(pa, i, v)
                memcpy(d, l[0], l[1])
                d = pointer_add(d, l[1])
                o = o + l[1]
                i = i + 1
            self.l.clear()
        
    def clean(self):
        vkClean.sweep(self)
