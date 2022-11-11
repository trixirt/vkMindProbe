# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http:/unlicense.org/>

# Copied from
# https://www.duskborn.com/posts/a-simple-vulkan-compute-example/

import sys
from ctypes import *
from vk import *

appInfo                   = VkApplicationInfo()
appInfo.sType             = VK_STRUCTURE_TYPE_APPLICATION_INFO
appInfo.apiVersion        = vk_make_api_version(0,1,3,0)

instInfo                  = VkInstanceCreateInfo()
instInfo.sType            = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
instInfo.pApplicationInfo = appInfo.this

p = new_pVkInstance()
res = vkCreateInstance(instInfo, None, p)
if (res):
    sys.exit("could not create vk instance")

instance = pVkInstance_value(p)

pNumGPUs = new_puint32_t()
res = vkEnumeratePhysicalDevices(instance, pNumGPUs, None)
NumGPUs = puint32_t_value(pNumGPUs)

paGPUs = new_paVkPhysicalDevice(NumGPUs)
res = vkEnumeratePhysicalDevices(instance, pNumGPUs, paGPUs)

physicalDevice = None
pQueueFamilyIndex = new_puint32_t()
for gpuIdx in range(0, NumGPUs):
    pNum = new_puint32_t()
    physicalDevice = paVkPhysicalDevice_getitem(paGPUs, gpuIdx)
    res = vkGetPhysicalDeviceQueueFamilyProperties(physicalDevice, pNum, None)
    nQueue = puint32_t_value(pNum)
    paQueueFamilyProperties = new_paVkQueueFamilyProperties(nQueue)
    res = vkGetPhysicalDeviceQueueFamilyProperties(physicalDevice, pNum, paQueueFamilyProperties)
    for qIdx in range(0, nQueue):
        prop = paVkQueueFamilyProperties_getitem(paQueueFamilyProperties, qIdx)
        if (prop.queueFlags & VK_QUEUE_COMPUTE_BIT):
            puint32_t_assign(pQueueFamilyIndex, qIdx)
            break

queueFamilyIndex = puint32_t_value(pQueueFamilyIndex)

queueCreateInfo                       = VkDeviceQueueCreateInfo()
queueCreateInfo.sType                 = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO
queueCreateInfo.queueFamilyIndex      = queueFamilyIndex
queueCreateInfo.queueCount            = 1

deviceCreateInfo                      = VkDeviceCreateInfo()
deviceCreateInfo.sType                = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO; 
deviceCreateInfo.queueCreateInfoCount = 1
deviceCreateInfo.pQueueCreateInfos    = queueCreateInfo.this

pDevice = new_pVkDevice()
res = vkCreateDevice(physicalDevice, deviceCreateInfo.this, None, pDevice)
device = pVkDevice_value(pDevice)

physicalDeviceProperties = new_pVkPhysicalDeviceProperties()
vkGetPhysicalDeviceProperties(physicalDevice, physicalDeviceProperties)
# Something meaningful should be printed out
# ex/ NVIDIA A30
print("What this is running on...")
print(physicalDeviceProperties.deviceName)

physicalDeviceMemoryProperties = new_pVkPhysicalDeviceMemoryProperties()
vkGetPhysicalDeviceMemoryProperties(physicalDevice, physicalDeviceMemoryProperties)
bufferSize = 1024 * 4
memoryMin = 2 * bufferSize
memoryAllocateInfo = VkMemoryAllocateInfo()
memoryAllocateInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO
memoryAllocateInfo.allocationSize = memoryMin

for memIdx in range (0, physicalDeviceMemoryProperties.memoryTypeCount):
    memoryType = paVkMemoryType_getitem(physicalDeviceMemoryProperties.memoryTypes, memIdx)
    if ((memoryType.propertyFlags & VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT) and
        (memoryType.propertyFlags & VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)):
        memoryHeap = paVkMemoryHeap_getitem(physicalDeviceMemoryProperties.memoryHeaps, memoryType.heapIndex)
        if (memoryHeap.size >= memoryMin):
            memoryAllocateInfo.memoryTypeIndex = memIdx
            break

pDeviceMemory = new_pVkDeviceMemory()
vkAllocateMemory(device, memoryAllocateInfo, None, pDeviceMemory)
deviceMemory = pVkDeviceMemory_value(pDeviceMemory)

ppPayload = new_ppvoid()
vkMapMemory(device, deviceMemory, 0, memoryMin, 0, ppPayload)
pPayload = ppvoid_value(ppPayload)
uPayload = void_to_uint32_t(pPayload)

for i in range(0,1024):
    pauint32_t_setitem(uPayload, i, 1024-i)

print("Buffer before, note the 0's in the 2nd half")
v = pauint32_t_getitem(uPayload, 0)
print(v)
v = pauint32_t_getitem(uPayload, 1023)
print(v)
v = pauint32_t_getitem(uPayload, 1024)
print(v)
v = pauint32_t_getitem(uPayload, 2047)
print(v)

vkUnmapMemory(device, deviceMemory)

bufferCreateInfo                       = VkBufferCreateInfo()
bufferCreateInfo.sType                 = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO
bufferCreateInfo.size                  = bufferSize
bufferCreateInfo.usage                 = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT
bufferCreateInfo.sharingMode           = VK_SHARING_MODE_EXCLUSIVE
bufferCreateInfo.queueFamilyIndexCount = 1
bufferCreateInfo.pQueueFamilyIndices   = pQueueFamilyIndex

pInBuffer = new_pVkBuffer()
vkCreateBuffer(device, bufferCreateInfo.this, None, pInBuffer)
inBuffer = pVkBuffer_value(pInBuffer)
vkBindBufferMemory(device, inBuffer, deviceMemory, 0)

pOutBuffer = new_pVkBuffer()
vkCreateBuffer(device, bufferCreateInfo.this, None, pOutBuffer)
outBuffer = pVkBuffer_value(pOutBuffer)
vkBindBufferMemory(device, outBuffer, deviceMemory, bufferSize)

shaderFileSize = read_file("../shader/echo.spv", None, 0)
shaderCode = new_pauint32_t(shaderFileSize)
read_file("../shader/echo.spv", shaderCode, shaderFileSize)
shaderInfo          = VkShaderModuleCreateInfo()
shaderInfo.sType    = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO
shaderInfo.codeSize = shaderFileSize
shaderInfo.pCode    = shaderCode
pShaderModule       = new_pVkShaderModule()
vkCreateShaderModule(device, shaderInfo, None, pShaderModule)
shaderModule = pVkShaderModule_value(pShaderModule)

paDescriptorSetLayoutBindings = new_paVkDescriptorSetLayoutBinding(2)
b = VkDescriptorSetLayoutBinding()
b.binding         = 0
b.descriptorType  = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
b.descriptorCount = 1
b.stageFlags      = VK_SHADER_STAGE_COMPUTE_BIT
b.stageFlags      = VK_SHADER_STAGE_ALL
paVkDescriptorSetLayoutBinding_setitem(paDescriptorSetLayoutBindings, 0, b)
b.binding         = 1
paVkDescriptorSetLayoutBinding_setitem(paDescriptorSetLayoutBindings, 1, b)

descriptorSetLayoutCreateInfo = VkDescriptorSetLayoutCreateInfo()
descriptorSetLayoutCreateInfo.sType        = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO
descriptorSetLayoutCreateInfo.bindingCount = 2
descriptorSetLayoutCreateInfo.pBindings    = paDescriptorSetLayoutBindings
pDescriptorSetLayout = new_pVkDescriptorSetLayout()
vkCreateDescriptorSetLayout(device, descriptorSetLayoutCreateInfo, None, pDescriptorSetLayout);
descriptorSetLayout = pVkDescriptorSetLayout_value(pDescriptorSetLayout)

pipelineLayoutCreateInfo = VkPipelineLayoutCreateInfo()
pipelineLayoutCreateInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO
pipelineLayoutCreateInfo.setLayoutCount = 1
pipelineLayoutCreateInfo.pSetLayouts = pDescriptorSetLayout
pPipelineLayout = new_pVkPipelineLayout()
vkCreatePipelineLayout(device, pipelineLayoutCreateInfo, None, pPipelineLayout)
pipelineLayout = pVkPipelineLayout_value(pPipelineLayout)

computePipelineCreateInfo = VkComputePipelineCreateInfo()
computePipelineCreateInfo.sType = VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO
computePipelineCreateInfo.stage.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO
computePipelineCreateInfo.stage.stage = VK_SHADER_STAGE_COMPUTE_BIT
computePipelineCreateInfo.stage.module = shaderModule
computePipelineCreateInfo.stage.pName = "main"
computePipelineCreateInfo.layout = pipelineLayout
pPipeline = new_pVkPipeline()
vkCreateComputePipelines(device, None, 1, computePipelineCreateInfo, None, pPipeline)
pipeline = pVkPipeline_value(pPipeline)

descriptorPoolSize = VkDescriptorPoolSize()
descriptorPoolSize.type = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
descriptorPoolSize.descriptorCount = 2
descriptorPoolCreateInfo = VkDescriptorPoolCreateInfo()
descriptorPoolCreateInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO
descriptorPoolCreateInfo.maxSets = 1
descriptorPoolCreateInfo.poolSizeCount = 1
descriptorPoolCreateInfo.pPoolSizes =  descriptorPoolSize.this
pDescriptorPool = new_pVkDescriptorPool()
vkCreateDescriptorPool(device, descriptorPoolCreateInfo, None, pDescriptorPool)
descriptorPool = pVkDescriptorPool_value(pDescriptorPool)

descriptorSetAllocateInfo = VkDescriptorSetAllocateInfo()
descriptorSetAllocateInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO
descriptorSetAllocateInfo.descriptorPool = descriptorPool
descriptorSetAllocateInfo.descriptorSetCount = 1
descriptorSetAllocateInfo.pSetLayouts = pDescriptorSetLayout
pDescriptorSet = new_pVkDescriptorSet()
res = vkAllocateDescriptorSets(device, descriptorSetAllocateInfo, pDescriptorSet)
descriptorSet = pVkDescriptorSet_value(pDescriptorSet)

inDescriptorBufferInfo = VkDescriptorBufferInfo()
inDescriptorBufferInfo.buffer = inBuffer
inDescriptorBufferInfo.offset = 0
inDescriptorBufferInfo.range = vk_whole_size()
outDescriptorBufferInfo = VkDescriptorBufferInfo()
outDescriptorBufferInfo.buffer = outBuffer
outDescriptorBufferInfo.offset = 0
outDescriptorBufferInfo.range = vk_whole_size()

paWriteDescriptorSet = new_paVkWriteDescriptorSet(2)
s = VkWriteDescriptorSet()
s.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET
s.dstSet = descriptorSet
s.dstBinding = 0
s.dstArrayElement = 0
s.descriptorCount = 1
s.descriptorType = VK_DESCRIPTOR_TYPE_STORAGE_BUFFER
s.pBufferInfo = inDescriptorBufferInfo.this
paVkWriteDescriptorSet_setitem(paWriteDescriptorSet, 0, s)
s.dstBinding = 1
s.pBufferInfo = outDescriptorBufferInfo.this
paVkWriteDescriptorSet_setitem(paWriteDescriptorSet, 1, s)
vkUpdateDescriptorSets(device, 2, paWriteDescriptorSet, 0, None);

commandPoolCreateInfo = VkCommandPoolCreateInfo()
commandPoolCreateInfo.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO
commandPoolCreateInfo.queueFamilyIndex = queueFamilyIndex
pCommandPool = new_pVkCommandPool()
res = vkCreateCommandPool(device, commandPoolCreateInfo, None, pCommandPool)
commandPool = pVkCommandPool_value(pCommandPool)

commandBufferAllocateInfo = VkCommandBufferAllocateInfo()
commandBufferAllocateInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO
commandBufferAllocateInfo.commandPool = commandPool
commandBufferAllocateInfo.level =  VK_COMMAND_BUFFER_LEVEL_PRIMARY
commandBufferAllocateInfo.commandBufferCount = 1
pCommandBuffer = new_pVkCommandBuffer()
vkAllocateCommandBuffers(device, commandBufferAllocateInfo, pCommandBuffer)
commandBuffer = pVkCommandBuffer_value(pCommandBuffer)

commandBufferBeginInfo = VkCommandBufferBeginInfo()
commandBufferBeginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO
commandBufferBeginInfo.flags = VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT
vkBeginCommandBuffer(commandBuffer, commandBufferBeginInfo)
vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_COMPUTE, pipeline)
vkCmdBindDescriptorSets(commandBuffer, VK_PIPELINE_BIND_POINT_COMPUTE, pipelineLayout, 0, 1, pDescriptorSet, 0, None)
vkCmdDispatch(commandBuffer, 1024, 1, 1)
vkEndCommandBuffer(commandBuffer);

pQueue = new_pVkQueue()
vkGetDeviceQueue(device, queueFamilyIndex, 0, pQueue)
queue = pVkQueue_value(pQueue)

submitInfo = VkSubmitInfo()
submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO
submitInfo.commandBufferCount = 1
submitInfo.pCommandBuffers = pCommandBuffer
vkQueueSubmit(queue, 1, submitInfo, None)
vkQueueWaitIdle(queue)

res = vkMapMemory(device, deviceMemory, 0, memoryMin, 0, ppPayload)
pPayload = ppvoid_value(ppPayload)
uPayload = void_to_uint32_t(pPayload)

print("Buffer after, check if 2nd half has changed to match 1st half")
v = pauint32_t_getitem(uPayload, 0)
print(v)
v = pauint32_t_getitem(uPayload, 1023)
print(v)
v = pauint32_t_getitem(uPayload, 1024)
print(v)
v = pauint32_t_getitem(uPayload, 2047)
print(v)

