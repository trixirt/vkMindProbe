#
# Copyright 2022 Tom Rix trix@redhat.com
#
from vk import *

class vkDevice:
    def __init__(self, paPhysicalDevices, index):
        self.v = paVkPhysicalDevice_getitem(paPhysicalDevices, index)
        p = new_pVkPhysicalDeviceProperties()
        vkGetPhysicalDeviceProperties(self.v, p)
        self.properties = p
        p = new_pVkPhysicalDeviceMemoryProperties()
        vkGetPhysicalDeviceMemoryProperties(self.v, p)
        self.memoryProperties = p
        p = new_puint32_t()
        vkGetPhysicalDeviceQueueFamilyProperties(self.v, p, None)
        self.numQueue = puint32_t_value(p)
        self.queueProperties = []
        if (self.numQueue):
            pa = new_paVkQueueFamilyProperties(self.numQueue)
            vkGetPhysicalDeviceQueueFamilyProperties(self.v, p, pa)
            for i in range(0, self.numQueue):
                v = paVkQueueFamilyProperties_getitem(pa, i)
                self.queueProperties.append(v)

    def pick(self, memory):
        for i in range(0, self.numQueue):
            if self.queueProperties[i].queueFlags & VK_QUEUE_COMPUTE_BIT:
                for m in range (0, self.memoryProperties.memoryTypeCount):
                    v = paVkMemoryType_getitem(self.memoryProperties.memoryTypes, m)
                    if ((v.propertyFlags & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT) and
                        (v.propertyFlags & VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)):
                        h = paVkMemoryHeap_getitem(self.memoryProperties.memoryHeaps, v.heapIndex)
                        if (h.size >= memory):
                            return i,m
        return -1,-1;

    def strVkPhysicalDeviceType(self, s):
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

    def print(self):
        print("\tapiVersion:    " + hex(self.properties.apiVersion))
        print("\tdriverVersion: " + hex(self.properties.driverVersion))
        print("\tvendorID:      " + hex(self.properties.vendorID))
        print("\tdeviceID:      " + hex(self.properties.deviceID))
        print("\tdeviceType:    " + self.strVkPhysicalDeviceType(self.properties.deviceType))
        print("\tdeviceName:    " + self.properties.deviceName)
        print("\tlimits:")
        v = self.properties.limits.maxComputeSharedMemorySize
        print("\t\tmaxComputeSharedMemorySize:     %u" % v)
        x = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupCount, 0)
        y = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupCount, 1)
        z = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupCount, 2)
        print("\t\tmaxComputeWorkGroupCount:       %u %u %u" % (x, y, z))
        v = self.properties.limits.maxComputeWorkGroupInvocations
        print("\t\tmaxComputeWorkGroupInvocations: %u" % v)
        x = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupSize, 0)
        y = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupSize, 1)
        z = pauint32_t_getitem(self.properties.limits.maxComputeWorkGroupSize, 2)
        print("\t\tmaxComputeWorkGroupSize:        %u %u %u" % (x, y, z))

class vkDevices :
    def __init__(self, instance):
        p = new_puint32_t()
        vkEnumeratePhysicalDevices(instance.v, p, None)
        self.num = puint32_t_value(p)
        self.v = []
        if (self.num != 0):
            pa = new_paVkPhysicalDevice(self.num)
            vkEnumeratePhysicalDevices(instance.v, p, pa)
            for i in range(0, self.num):
                v = vkDevice(pa, i)
                self.v.append(v)

    def create(self, indexDevice, indexQueue):
        queueCreateInfo                       = VkDeviceQueueCreateInfo()
        queueCreateInfo.sType                 = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO
        queueCreateInfo.queueFamilyIndex      = indexQueue
        queueCreateInfo.queueCount            = 1
        deviceCreateInfo                      = VkDeviceCreateInfo()
        deviceCreateInfo.sType                = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO; 
        deviceCreateInfo.queueCreateInfoCount = 1
        deviceCreateInfo.pQueueCreateInfos    = queueCreateInfo.this
        p = new_pVkDevice()
        vkCreateDevice(self.v[indexDevice].v, deviceCreateInfo.this, None, p)
        v = pVkDevice_value(p)
        return v
        
    def pick(self, memory):
        for i in range(0, self.num):
            if (self.v[i].properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU):
                q,m = self.v[i].pick(memory);
                if m > -1:
                    return i,q,m
        for i in range(0, self.num):
            if (self.v[i].properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU):
                q,m = self.v[i].pick(memory);
                if m > -1:
                    return i,q,m
        for i in range(0, self.num):
            if (self.v[i].properties.deviceType == VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU):
                q,m = self.v[i].pick(memory);
                if m > -1:
                    return i,m
        for i in range(0, self.num):
            if (self.v[i].properties.deviceType == VK_PHYSICAL_DEVICE_CPU):
                q,m = self.v[i].pick(memeory);
                if m > -1:
                    return i,q,m
        for i in range(0, self.num):
            if (self.v[i].properties.deviceType == VK_PHYSICAL_DEVICE_OTHER):
                q,m = self.v[i].pick(memory);
                if m > -1:
                    return i,q,m
        return -1,-1,-1

    def print(self):
        for i in range(0, self.num):
            print("Device: %u" % i)
            self.v[i].print()

