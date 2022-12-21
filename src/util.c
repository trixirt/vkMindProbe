#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <vulkan/vulkan_core.h>
uint32_t vk_make_api_version(uint32_t variant, uint32_t major, uint32_t minor, uint32_t patch) {
	return VK_MAKE_API_VERSION(variant, major, minor, patch);
}
/* from gendefines.sh */
int vk_api_version_1_0 () { return VK_API_VERSION_1_0; }
int vk_api_version_1_1 () { return VK_API_VERSION_1_1; }
int vk_api_version_1_2 () { return VK_API_VERSION_1_2; }
int vk_api_version_1_3 () { return VK_API_VERSION_1_3; }
int vk_api_version_major(uint32_t version)  { return VK_API_VERSION_MAJOR(version); }
int vk_api_version_minor(uint32_t version)  { return VK_API_VERSION_MINOR(version); }
int vk_api_version_patch(uint32_t version)  { return VK_API_VERSION_PATCH(version); }
int vk_api_version_variant(uint32_t version) { return VK_API_VERSION_VARIANT(version); }
uint32_t vk_attachment_unused () { return VK_ATTACHMENT_UNUSED; }
uint32_t vk_false () { return VK_FALSE; }
int vk_header_version () { return VK_HEADER_VERSION; }
int vk_header_version_complete () { return VK_HEADER_VERSION_COMPLETE; }
int vk_lod_clamp_none () { return VK_LOD_CLAMP_NONE; }
uint32_t vk_luid_size () { return VK_LUID_SIZE; }
uint32_t vk_max_description_size () { return VK_MAX_DESCRIPTION_SIZE; }
uint32_t vk_max_device_group_size () { return VK_MAX_DEVICE_GROUP_SIZE; }
uint32_t vk_max_driver_info_size () { return VK_MAX_DRIVER_INFO_SIZE; }
uint32_t vk_max_driver_name_size () { return VK_MAX_DRIVER_NAME_SIZE; }
uint32_t vk_max_memory_heaps () { return VK_MAX_MEMORY_HEAPS; }
uint32_t vk_max_memory_types () { return VK_MAX_MEMORY_TYPES; }
uint32_t vk_max_physical_device_name_size () { return VK_MAX_PHYSICAL_DEVICE_NAME_SIZE; }
uint32_t vk_queue_family_ignored () { return VK_QUEUE_FAMILY_IGNORED; }
uint32_t vk_remaining_array_layers () { return VK_REMAINING_ARRAY_LAYERS; }
uint32_t vk_remaining_mip_levels () { return VK_REMAINING_MIP_LEVELS; }
uint32_t vk_true () { return VK_TRUE; }
uint32_t vk_uuid_size () { return VK_UUID_SIZE; }
int vk_version_1_0 () { return VK_VERSION_1_0; }
int vk_version_1_1 () { return VK_VERSION_1_1; }
int vk_version_1_2 () { return VK_VERSION_1_2; }
int vk_version_1_3 () { return VK_VERSION_1_3; }
int vk_version_major(uint32_t version) { return VK_VERSION_MAJOR(version); }
int vk_version_minor(uint32_t version) { return VK_VERSION_MINOR(version); }
int vk_version_patch(uint32_t version) { return VK_VERSION_PATCH(version); }
uint64_t vk_whole_size () { return VK_WHOLE_SIZE; }

int read_file(const char *n, uint32_t *b, size_t s) {
	int ret = -1;
	int fd = open(n, O_RDONLY);
	if (fd >= 0) {
		if (b) {
			ret = read(fd, b, s);
		} else {
			struct stat buf;
			if (!fstat(fd, &buf))
				ret = buf.st_size;
		}
		close(fd);
	}
	return ret;
}

int write_file(const char *n, uint32_t *b, size_t s) {
	int ret = -1;
	int fd = open(n, O_WRONLY | O_CREAT);
	if (fd >= 0) {
		if (b)
			ret = write(fd, b, s);
		else
			ret = 0;
		close(fd);
	}
	return ret;
}

void * pointer_add(void *p, int v) {
	return p + v;
}
void * pointer(uint64_t v) {
	return (void *)v;
}
