#!/usr/bin/env python
#
# Copyright Tom Rix trix@redhat.com
#

import sys
from vk import *

instance = vkInstance()
devices = vkDevice(instance)
for i in range(0, devices.num):
    devices.print(i)
