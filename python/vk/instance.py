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

class vkInstance:
    def __init__(self):
        self.cl = []
        appInfo                   = VkApplicationInfo()
        appInfo.sType             = VK_STRUCTURE_TYPE_APPLICATION_INFO
        appInfo.apiVersion        = vk_make_api_version(0,1,3,0)
        instInfo                  = VkInstanceCreateInfo()
        instInfo.sType            = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        instInfo.pApplicationInfo = appInfo
        p = new_pVkInstance()
        vkClean.dust(self, [delete_pVkInstance, p])
        vkCreateInstance(instInfo, None, p)
        self.v = pVkInstance_value(p)
        vkClean.dust(self, [vkDestroyInstance, self.v, None])

    def __del__(self):
        self.clean()

    def clean(self):
        vkClean.sweep(self)
