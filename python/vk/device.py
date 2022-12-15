#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkDevice:
    def __init__(self, instance):
        p = new_puint32_t()
        vkEnumeratePhysicalDevices(instance.v, p, None)
        self.num = puint32_t_value(p)
        self.v = []
        self.properties = []
        if (self.num != 0):
            pa = new_paVkPhysicalDevice(self.num)
            vkEnumeratePhysicalDevices(instance.v, p, pa)
            for i in range(0, self.num):
                d = paVkPhysicalDevice_getitem(pa, i)
                self.v.append(d)
                p = new_pVkPhysicalDeviceProperties()
                vkGetPhysicalDeviceProperties(d, p)
                self.properties.append(p)

    def print(self, n):
        print("Device: %u" % n)
        print("\tapiVersion:    " + hex(self.properties[n].apiVersion))
        print("\tdriverVersion: " + hex(self.properties[n].driverVersion))
        print("\tvendorID:      " + hex(self.properties[n].vendorID))
        print("\tdeviceID:      " + hex(self.properties[n].deviceID))
        print("\tdeviceType     " + strVkPhysicalDeviceType(self.properties[n].deviceType))
        print("\tdeviceName:    " + self.properties[n].deviceName)
        print("\tlimits:")
        v = self.properties[n].limits.maxComputeSharedMemorySize
        print("\t\tmaxComputeSharedMemorySize:     %u" % v)
        x = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupCount, 0)
        y = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupCount, 1)
        z = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupCount, 2)
        print("\t\tmaxComputeWorkGroupCount:       %u %u %u" % (x, y, z))
        v = self.properties[n].limits.maxComputeWorkGroupInvocations
        print("\t\tmaxComputeWorkGroupInvocations: %u" % v)
        x = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupSize, 0)
        y = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupSize, 1)
        z = pauint32_t_getitem(self.properties[n].limits.maxComputeWorkGroupSize, 2)
        print("\t\tmaxComputeWorkGroupSize:        %u %u %u" % (x, y, z))
