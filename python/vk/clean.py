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
class vkClean:

    def sweep(self):
        if self.cl == None:
            return
        for c in reversed(self.cl):
            l = len(c)
            if l == 2:
                c[0](c[1])
            elif l == 3:
                c[0](c[1], c[2])
            elif l == 4:
                c[0](c[1], c[2], c[3])
            elif l == 5:
                c[0](c[1], c[2], c[3], c[4])
        self.cl.clear()

    def dust(self, l):
        self.cl.append(l)
