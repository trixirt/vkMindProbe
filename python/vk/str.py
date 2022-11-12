#
# Copyright Tom Rix trix@redhat.com
#
from vk import *

def strVkPhysicalDeviceType(s):
    if (s == VK_PHYSICAL_DEVICE_TYPE_OTHER):
        return "other"
    elif (s == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU):
        return "integrated gpu"
    elif (s == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU):
        return "descrete gpu"
    elif (s == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU):
        return "virtual gpu"
    elif (s == VK_PHYSICAL_DEVICE_TYPE_CPU):
        return "cpu"
    else:
        return "unknown"
