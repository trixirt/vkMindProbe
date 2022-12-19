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
    def __init__(self, memory, sizes, shader):
        self.instance = vkInstance()
        self.devices = vkDevices(self.instance)
        self.dIdx, self.qIdx, self.mIdx = self.devices.pick(memory)
        self.device = self.devices.create(self.dIdx, self.qIdx)
        self.deviceMemory = vkMemory(self.device, self.mIdx)
        self.deviceMemory.allocate(memory)
        self.buffers = vkBuffer(self.device, self.deviceMemory.v, self.qIdx)
        self.buffers.allocate(sizes)
        self.shader = vkShader(self.device, self.buffers, shader)
        self.command = vkCommand(self.device, self.qIdx)
    def run(self, x, y, z):
        self.command.begin(self.shader, x, y, z)
        self.command.submit()
        self.command.end()
