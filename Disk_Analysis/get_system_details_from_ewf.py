#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   http://hiddenillusion.blogspot.com
#       @hiddenillusion
# Date: 2016-04-07
# (while at FireEye)

import os
import sys
import time
import json
try:
    import pyewf
except ImportError:
    print("pyewf required: https://github.com/libyal/libewf/tree/master/pyewf")

try:
    import pytsk3
except ImportError:
    print("pytsk3 required: https://github.com/py4n6/pytsk/")

try:
    from Registry import Registry
except ImportError:
    print("python-registry required: https://github.com/williballenthin/python-registry")

# source: https://raw.githubusercontent.com/dlcowen/dfirwizard/master/dfirwizard-v5.py
class ewf_img_info(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_img_info, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()

class LinuxInfo(object):
    def __init__(self, filesystem_obj):
        self._filesystem_obj = filesystem_obj

    def get_linux_details(self):
        result = {}
        paths = {}
        paths['hostname'] = "/etc/hostname"
        paths['version'] = "/etc/lsb-release"

        for path_type, path_location in paths.iteritems():
            try:
                file_obj = self._filesystem_obj.open(path_location)
                file_data = get_file_data(file_obj)
            except IOError as err: #Path no found
                return

            parts = []
            small_parts = {}
            for line in file_data.split('\n'):
                line = line.replace('"', '')
                if line:
                    if '=' in line:
                        k, v = line.split('=')
                        small_parts[k] = v
                    else:
                        parts.append(line)
            result[path_type] = parts + [small_parts]

        return result

class RegistryInfo(object):
    def __init__(self, filesystem_obj):
        self._filesystem_obj = filesystem_obj
        self._system_hive = ''
        self._software_hive = ''

    def get_control_set(self):
        """
        Determines which Control Set the system was using
        @system_hive: An instance of registry
        @return : int(single digit)
        """
        key = self._system_hive.open("Select")
        for v in key.values():
            if v.name() == "Current":
                return v.value()

    def get_registry_details(self):
        """
        @filesystem_obj: pytsk3.FS_Info()
        @return: a dictionary
        """
        result = {}
        hives = {}
        hives['system_hive'] = "/Windows/System32/Config/SYSTEM"
        hives['software_hive'] = "/Windows/System32/Config/SOFTWARE"

        for hive_type, hive_path in hives.iteritems():
            try:
                file_obj = self._filesystem_obj.open(hive_path)
                # if this fails, refer to https://github.com/williballenthin/python-registry/issues/59
                registry = Registry.Registry(get_file_data(file_obj))
            except IOError as err: #Path no found
                return

            if hive_type == "system_hive":
                self._system_hive = registry
                results.append(self.get_system_name())
            if hive_type == "software_hive":
                self._software_hive = registry
                results.append(self.get_os_settings())

            for d in results:
                for k, v in d.iteritems():
                    result[k] = v

        return result

    def get_system_name(self):
        """
        Retrieves computer/hostname values
        @return: A dictionary
        """
        name_dict = {}
        key = self._system_hive.open("ControlSet00{0}\\Control\\ComputerName\\ComputerName".format(self.get_control_set()))
        for v in key.values():
            if v.name() == "ComputerName":
                name_dict[v.name()] = v.value()

            key2 = self._system_hive.open("ControlSet00{0}\\Services\\Tcpip\\Parameters".format(self.get_control_set()))
            for v in key.values():
                if v.name() == "Hostname":
                    name_dict[v.name()] = v.value()

        return name_dict

    def get_os_settings(self):
        """
        Displays Operating System information
        @return: A dictionary
        """
        os_dict = {}
        key = self._software_hive.open("Microsoft\\Windows NT\\CurrentVersion")
        for v in key.values():
            if v.name() == "ProductName":
                os_dict['ProductName'] = v.value()
            if v.name() == "ProductId":
                os_dict['ProductId'] = v.value()
            if v.name() == "CSDVersion":
                os_dict['CSDVersion'] = v.value()
            if v.name() == "PathName":
                os_dict['PathName'] = v.value()
            if v.name() == "InstallDate":
                os_dict['InstallDate (UTC)'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(v.value()))
            if v.name() == "RegisteredOrganization":
                os_dict['RegisteredOrganization'] = v.value()
            if v.name() == "RegisteredOwner":
                os_dict['RegisteredOwner'] = v.value()

        return os_dict

def get_file_data(file_obj):
    """
    @file_obj: filesystem_obj.open()
    """
    return file_obj.read_random(0,file_obj.info.meta.size)

def get_file_info(file_obj):
    """
    @file_obj: filesystem_obj.open()
    """
    file_dict = {}
    file_dict['modified_time'] = file_obj.info.meta.mtime
    file_dict['accessed_time'] = file_obj.info.meta.atime
    file_dict['created_time'] = file_obj.info.meta.crtime
    file_dict['changed_time'] = file_obj.info.meta.ctime
    file_dict['flags'] = file_obj.info.meta.flags
    file_dict['gid'] = file_obj.info.meta.gid
    file_dict['uid'] = file_obj.info.meta.uid
    file_dict['meta_tag'] = file_obj.info.meta.tag
    file_dict['info_type'] = file_obj.info.meta.type
    file_dict['flags'] = file_obj.info.name.flags
    file_dict['filename'] = file_obj.info.name.name
    file_dict['name_tag'] = file_obj.info.name.tag
    file_dict['name_type'] = file_obj.info.name.type

    return file_dict

def recurse_path(path):
    if os.path.idsir(path):
        for root, dirs, files in os.walk(path):
            dirs.sort()
            for name in sorted(files):
                fname = os.path.join(root, name)
                    yield fname
    else:
        yield path

if __name__ == "__main__":
        import argparse
        parser = argparse.ArgumentParser(description='Grabs basic system info from EnCase EWF (E01) files')
        parser.add_argument('-i', '--input', action='store', help='Path to evidence file(s)', required=True)
        parser.add_argument('-s', '--sector_size', action='store', help='Sector size of image (Default is 512)', type=int, default=512)
        args = vars(parser.parse_args())

        #for filepath in recurse_path(args['input']):
        filenames = pyewf.glob(args['input'])
        evidence_files = {}
        evidence_files['evidence_files'] = filenames
        ewf_handle = pyewf.handle()
        ewf_handle.open(filenames)
        image_handle = ewf_img_info(ewf_handle)
        partition_table = pytsk3.Volume_Info(image_handle)

        result = []
        sector_size = args['sector_size']
        for partition in partition_table:
                partition_dict = {}
                partition_dict['partition_slot'] = '{0}'.format(partition.slot_num)
                partition_dict['partition_address'] = '{0}'.format(partition.addr)
                partition_dict['partition_description'] = '{0}'.format(partition.desc)
                partition_dict['partition_start'] = '{0}'.format(partition.start)
                partition_mount_start = partition.start * sector_size
                partition_dict['partition_mount_start'] = '{0}'.format(partition_mount_start)
                partition_dict['partition_length'] = '{0}'.format(partition.len)
                try:
                    filesystem_obj = pytsk3.FS_Info(image_handle, offset=(partition_mount_start))
                    partition_dict['partition_filesystem'] = '{0}'.format(filesystem_obj.info.ftype)
                except Exception as err:
                    partition_dict['partition_filesystem'] = "UNSUPPORTED"
                    continue

                if "{0}".format(filesystem_obj.info.ftype) == "TSK_FS_TYPE_NTFS_DETECT":
                    try:
                        windir = filesystem_obj.open_dir("/Windows")
                        reg_info = RegistryInfo(filesystem_obj)
                        partition_dict['system_details'] = reg_info.get_registry_details()
                    except Exception as err:
                        continue
                elif "{0}".format(filesystem_obj.info.ftype) in ["TSK_FS_TYPE_EXT2", "TSK_FS_TYPE_EXT3", "TSK_FS_TYPE_EXT4"]:
                    try:
                        nix_info = LinuxInfo(filesystem_obj)
                        partition_dict['system_details'] = nix_info.get_linux_details()
                    except Exception as err:
                        continue

                result.append(partition_dict)
        result.append([evidence_files])
        print(json.dumps(result, indent=4))
