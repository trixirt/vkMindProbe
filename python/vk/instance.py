#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkInstance:
    def __init__(self):
        appInfo                   = VkApplicationInfo()
        appInfo.sType             = VK_STRUCTURE_TYPE_APPLICATION_INFO
        appInfo.apiVersion        = vk_make_api_version(0,1,3,0)
        instInfo                  = VkInstanceCreateInfo()
        instInfo.sType            = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        instInfo.pApplicationInfo = appInfo
        p = new_pVkInstance()
        vkCreateInstance(instInfo, None, p)
        self.v = pVkInstance_value(p)
