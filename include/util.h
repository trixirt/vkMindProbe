//
// Copyright 2022 Tom Rix trix@redhat.com
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
uint32_t vk_make_api_version(uint32_t variant, uint32_t major, uint32_t minor, uint32_t patch);
/* from gendefines.sh */
int vk_api_version_1_0 ();
int vk_api_version_1_1 ();
int vk_api_version_1_2 ();
int vk_api_version_1_3 ();
int vk_api_version_major(uint32_t version);
int vk_api_version_minor(uint32_t version);
int vk_api_version_patch(uint32_t version);
int vk_api_version_variant(uint32_t version);
uint32_t vk_attachment_unused ();
uint32_t vk_false ();
int vk_header_version ();
int vk_header_version_complete ();
int vk_lod_clamp_none ();
uint32_t vk_luid_size ();
uint32_t vk_max_description_size ();
uint32_t vk_max_device_group_size ();
uint32_t vk_max_driver_info_size ();
uint32_t vk_max_driver_name_size ();
uint32_t vk_max_memory_heaps ();
uint32_t vk_max_memory_types ();
uint32_t vk_max_physical_device_name_size ();
uint32_t vk_queue_family_ignored ();
uint32_t vk_remaining_array_layers ();
uint32_t vk_remaining_mip_levels ();
uint32_t vk_true ();
uint32_t vk_uuid_size ();
int vk_version_1_0 ();
int vk_version_1_1 ();
int vk_version_1_2 ();
int vk_version_1_3 ();
int vk_version_major(uint32_t version);
int vk_version_minor(uint32_t version);
int vk_version_patch(uint32_t version);
uint64_t vk_whole_size ();

int read_file(const char *n, uint32_t *b, size_t s);
int write_file(const char *n, uint32_t *b, size_t s);
void *pointer_add(void *p, int v);
void *pointer(uint64_t v);
void *memcpy(void *dest, const void *src, size_t n);
void *memset(void *s, int c, size_t n);
