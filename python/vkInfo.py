#!/usr/bin/env python
#
# Copyright Tom Rix trix@redhat.com
#

import sys
from vk import *

instance = vkInstance()

pNumGPUs = new_puint32_t()
vkEnumeratePhysicalDevices(instance.v, pNumGPUs, None)
NumGPUs = puint32_t_value(pNumGPUs)
if (NumGPUs == 0):
    sys.exit("No gpus")

paGPUs = new_paVkPhysicalDevice(NumGPUs)
vkEnumeratePhysicalDevices(instance.v, pNumGPUs, paGPUs)

for i in range(0, NumGPUs):
    physicalDevice = paVkPhysicalDevice_getitem(paGPUs, i)
    p = new_pVkPhysicalDeviceProperties()
    vkGetPhysicalDeviceProperties(physicalDevice, p)
    print("PhysicalDeviceProperties")
    print("\tapiVersion:    " + hex(p.apiVersion))
    print("\tdriverVersion: " + hex(p.driverVersion))
    print("\tvendorID:      " + hex(p.vendorID))
    print("\tdeviceID:      " + hex(p.deviceID))
    print("\tdeviceType     " + strVkPhysicalDeviceType(p.deviceType))
    print("\tdeviceName:    " + p.deviceName)
    print("\tlimits:")
    v = p.limits.maxComputeSharedMemorySize
    print("\t\tmaxComputeSharedMemorySize:     %u" % v)
    x = pauint32_t_getitem(p.limits.maxComputeWorkGroupCount, 0)
    y = pauint32_t_getitem(p.limits.maxComputeWorkGroupCount, 1)
    z = pauint32_t_getitem(p.limits.maxComputeWorkGroupCount, 2)
    print("\t\tmaxComputeWorkGroupCount:       %u %u %u" % (x, y, z))
    v = p.limits.maxComputeWorkGroupInvocations
    print("\t\tmaxComputeWorkGroupInvocations: %u" % v)
    x = pauint32_t_getitem(p.limits.maxComputeWorkGroupSize, 0)
    y = pauint32_t_getitem(p.limits.maxComputeWorkGroupSize, 1)
    z = pauint32_t_getitem(p.limits.maxComputeWorkGroupSize, 2)
    print("\t\tmaxComputeWorkGroupSize:        %u %u %u" % (x, y, z))

