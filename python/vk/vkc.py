#
# Copyright 2022 Tom Rix trix@redhat.com
#
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

class vkc:
    def __init__(self, sizes, shader):
        memory = 1024
        for s in sizes:
            memory = memory + s
        self.instance = vkInstance()
        self.devices = vkDevices(self.instance)
        self.dIdx, self.qIdx, self.mIdx = self.devices.pick(memory)
        self.device = self.devices.create(self.dIdx, self.qIdx)
        self.memory = vkMemory(self.device, self.mIdx)
        self.memory.allocate(memory)
        self.buffers = vkBuffer(self.device, self.memory.v, self.qIdx)
        self.buffers.allocate(sizes)
        self.shader = vkShader(self.device, self.buffers, shader)
        self.command = vkCommand(self.device, self.qIdx)
        self.mm = new_ppvoid()

    def __del__(self):
        delete_ppvoid(self.mm)
        self.command.clean()
        self.shader.clean()
        self.buffers.clean()
        self.memory.clean()
        self.devices.clean()
        self.instance.clean()

    def run(self, x, y, z):
        self.command.begin(self.shader, x, y, z)
        self.command.submit()
        self.command.end()

    def maps(self):
        r = []
        size = self.buffers.extent()
        self.memory.map(self.mm, size)
        v = ppvoid_value(self.mm)
        for b in self.buffers.o:
            p = pointer_add(v, b)
            r.append(p)
        return r

    def unmap(self):
        self.memory.unmap()
