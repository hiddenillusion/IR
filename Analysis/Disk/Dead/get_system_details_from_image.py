#!/usr/bin/env python

# created by Glenn P. Edwards Jr.
#   https://hiddenillusion.github.io
#       @hiddenillusion
# Date: 2016-04-07
# (while at FireEye)

'''
$ mmls /mnt/evidence/vmdk1

DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0039845887   0039843840   Linux (0x83)
003:  -------   0039845888   0039847935   0000002048   Unallocated
004:  Meta      0039847934   0041940991   0002093058   DOS Extended (0x05)
005:  Meta      0039847934   0039847934   0000000001   Extended Table (#1)
006:  001:000   0039847936   0041940991   0002093056   Linux Swap / Solaris x86 (0x82)
007:  -------   0041940992   0041943039   0000002048   Unallocated

$ python get_system_details_from_image.py -i /mnt/evidence/vmdk1

{
    "image_size": {
        "bytes": "21474836480",
        "gb": "20.0",
        "mb": "20480.0"
    },
    "partition_details": {
        "block_size": "512",
        "offset": "0",
        "part_count": "8",
        "type": "TSK_VS_TYPE_DOS"
    },
    "partition_table": [
        {
            "description": "Primary Table (#0)",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_META",
            "length": "1",
            "mount_start": "0",
            "partition_number": "0",
            "size": {
                "bytes": "512",
                "gb": "4.76837158203e-07",
                "mb": "0.00048828125"
            },
            "slot": "-1",
            "start": "0",
            "table_number": "-1"
        },
        {
            "description": "Unallocated",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_UNALLOC",
            "length": "2048",
            "mount_start": "0",
            "partition_number": "1",
            "size": {
                "bytes": "1048576",
                "gb": "0.0009765625",
                "mb": "1.0"
            },
            "slot": "-1",
            "start": "0",
            "table_number": "-1"
        },
        {
            "description": "Linux (0x83)",
            "filesystem": "TSK_FS_TYPE_EXT4",
            "flags": "TSK_VS_PART_FLAG_ALLOC",
            "length": "39843840",
            "mount_start": "1048576",
            "partition_number": "2",
            "size": {
                "bytes": "20400046080",
                "gb": "18.9990234375",
                "mb": "19455.0"
            },
            "slot": "0",
            "start": "2048",
            "system_details": {
                "hostname": [
                    {
                        "/etc/hostname": [
                            "user-vm-ubuntu"
                        ]
                    }
                ],
                "version": [
                    {
                        "/etc/lsb-release": [
                            {
                                "DISTRIB_CODENAME": "precise",
                                "DISTRIB_DESCRIPTION": "Ubuntu 12.04.4 LTS",
                                "DISTRIB_ID": "Ubuntu",
                                "DISTRIB_RELEASE": "12.04"
                            }
                        ]
                    }
                ]
            },
            "table_number": "0"
        },
        {
            "description": "Unallocated",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_UNALLOC",
            "length": "2048",
            "mount_start": "20401094656",
            "partition_number": "3",
            "size": {
                "bytes": "1048576",
                "gb": "0.0009765625",
                "mb": "1.0"
            },
            "slot": "-1",
            "start": "39845888",
            "table_number": "-1"
        },
        {
            "description": "DOS Extended (0x05)",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_META",
            "length": "2093058",
            "mount_start": "20402142208",
            "partition_number": "4",
            "size": {
                "bytes": "1071645696",
                "gb": "0.998047828674",
                "mb": "1022.00097656"
            },
            "slot": "1",
            "start": "39847934",
            "table_number": "0"
        },
        {
            "description": "Extended Table (#1)",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_META",
            "length": "1",
            "mount_start": "20402142208",
            "partition_number": "5",
            "size": {
                "bytes": "512",
                "gb": "4.76837158203e-07",
                "mb": "0.00048828125"
            },
            "slot": "-1",
            "start": "39847934",
            "table_number": "1"
        },
        {
            "description": "Linux Swap / Solaris x86 (0x82)",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_ALLOC",
            "length": "2093056",
            "mount_start": "20402143232",
            "partition_number": "6",
            "size": {
                "bytes": "1071644672",
                "gb": "0.998046875",
                "mb": "1022.0"
            },
            "slot": "0",
            "start": "39847936",
            "table_number": "1"
        },
        {
            "description": "Unallocated",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_UNALLOC",
            "length": "2048",
            "mount_start": "21473787904",
            "partition_number": "7",
            "size": {
                "bytes": "1048576",
                "gb": "0.0009765625",
                "mb": "1.0"
            },
            "slot": "-1",
            "start": "41940992",
            "table_number": "-1"
        },
        [
            {
                "evidence_files": [
                    "/mnt/evidence/vmdk1"
                ]
            }
        ]
    ]
}

$ get_system_details_from_image.py -t ewf -i /mnt/evidence.E01
{
    "image_size": {
        "bytes": "250000000000",
        "gb": "232.830643654",
        "mb": "238418.579102"
    },
    "partition_details": {
        "block_size": "512",
        "offset": "0",
        "part_count": "4",
        "type": "TSK_VS_TYPE_DOS"
    },
    "partition_table": [
        {
            "description": "Primary Table (#0)",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_META",
            "length": "1",
            "mount_start": "0",
            "partition_number": "0",
            "size": {
                "bytes": "512",
                "gb": "4.76837158203e-07",
                "mb": "0.00048828125"
            },
            "slot": "-1",
            "start": "0",
            "table_number": "-1"
        },
        {
            "description": "Unallocated",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_UNALLOC",
            "length": "63",
            "mount_start": "0",
            "partition_number": "1",
            "size": {
                "bytes": "32256",
                "gb": "3.00407409668e-05",
                "mb": "0.03076171875"
            },
            "slot": "-1",
            "start": "0",
            "table_number": "-1"
        },
        {
            "description": "NTFS / exFAT (0x07)",
            "filesystem": "TSK_FS_TYPE_NTFS_DETECT",
            "flags": "TSK_VS_PART_FLAG_ALLOC",
            "length": "488263482",
            "mount_start": "32256",
            "partition_number": "2",
            "size": {
                "bytes": "249990902784",
                "gb": "232.822171211",
                "mb": "238409.90332"
            },
            "slot": "0",
            "start": "63",
            "system_details": {
                "CSDVersion": "Service Pack 3",
                "ComputerName": "TEST-PC",
                "InstallDate (UTC)": "2013-07-12 02:11:00",
                "PathName": "C:\\WINDOWS",
                "ProductId": "74587-OEM-003344-25345",
                "ProductName": "Microsoft Windows XP",
                "RegisteredOrganization": "Some Company",
                "RegisteredOwner": "Owner"
            },
            "table_number": "0"
        },
        {
            "description": "Unallocated",
            "filesystem": "UNSUPPORTED",
            "flags": "TSK_VS_PART_FLAG_UNALLOC",
            "length": "17705",
            "mount_start": "249990935040",
            "partition_number": "3",
            "size": {
                "bytes": "9064960",
                "gb": "0.00844240188599",
                "mb": "8.64501953125"
            },
            "slot": "-1",
            "start": "488263545",
            "table_number": "-1"
        },
        [
            {
                "evidence_files": [
                    "/mnt/evidence.E01",
                    "/mnt/evidence.E02",
                    "/mnt/evidence.E03",
                    "/mnt/evidence.E04",
                    "/mnt/evidence.E05",
                    "/mnt/evidence.E06",
                    "/mnt/evidence.E07",
                    "/mnt/evidence.E08",
                    "/mnt/evidence.E09",
                    "/mnt/evidence.E10",
                    "/mnt/evidence.E11",
                    "/mnt/evidence.E12",
                    "/mnt/evidence.E13",
                    "/mnt/evidence.E14",
                    "/mnt/evidence.E15",
                    "/mnt/evidence.E16",
                    "/mnt/evidence.E17",
                    "/mnt/evidence.E18",
                    "/mnt/evidence.E19",
                    "/mnt/evidence.E20",
                    "/mnt/evidence.E21",
                    "/mnt/evidence.E22",
                    "/mnt/evidence.E23",
                    "/mnt/evidence.E24",
                    "/mnt/evidence.E25",
                    "/mnt/evidence.E26",
                    "/mnt/evidence.E27",
                    "/mnt/evidence.E28",
                    "/mnt/evidence.E29",
                    "/mnt/evidence.E30",
                    "/mnt/evidence.E31",
                    "/mnt/evidence.E32",
                    "/mnt/evidence.E33",
                    "/mnt/evidence.E34",
                    "/mnt/evidence.E35",
                    "/mnt/evidence.E36",
                    "/mnt/evidence.E37",
                    "/mnt/evidence.E38",
                    "/mnt/evidence.E39",
                    "/mnt/evidence.E40",
                    "/mnt/evidence.E41",
                    "/mnt/evidence.E42"
                ]
            }
        ]
    ]
}

'''

import os
import sys
import time
import json
from collections import defaultdict
from StringIO import StringIO

try:
    import pyewf
except ImportError:
    print("pyewf required: https://github.com/libyal/libewf/tree/master/pyewf")
    sys.exit(1)

try:
    import pytsk3
except ImportError:
    print("pytsk3 required: https://github.com/py4n6/pytsk/")
    sys.exit(1)

try:
    from Registry import Registry
except ImportError:
    print("python-registry required: https://github.com/williballenthin/python-registry")
    sys.exit(1)

# https://gist.github.com/shawnbutts/3906915
def convert_bytes(bytes, to, bsize=1024):
    a = {'kb' : 1, 'mb': 2, 'gb' : 3, 'tb' : 4, 'pb' : 5, 'eb' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

# sources:
#   - https://raw.githubusercontent.com/dlcowen/dfirwizard/master/dfirwizard-v5.py
#   - https://github.com/libyal/libewf/wiki/Development#combining-pyewf-with-pytsk3
class EwfImageInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EwfImageInfo, self).__init__(
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
        paths = {}
        paths['hostname'] = ['/etc/hostname']
        paths['version'] = [
                            '/etc/centos-release',
                            '/etc/lsb-release',
                            '/etc/redhat-release',
                            '/proc/version'
                            ]

        path_type_dict = defaultdict(list)
        for path_type, path_locations in paths.iteritems():
            for path_location in path_locations:
                try:
                    file_obj = self._filesystem_obj.open(path_location)
                    file_data = get_file_data(file_obj)
                    path_type_dict[path_type].append({path_location : self.parse_lines(file_data)})
                except IOError as err: #Path not found
                    pass

        return path_type_dict

    def parse_lines(self, file_data):
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

        return (parts + [small_parts] if small_parts else parts)

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
        results = []
        hives = {}
        hives['system_hive'] = "/Windows/System32/Config/SYSTEM"
        hives['software_hive'] = "/Windows/System32/Config/SOFTWARE"

        for hive_type, hive_path in hives.iteritems():
            try:
                file_obj = self._filesystem_obj.open(hive_path)
                file_data = file_obj.read_random(0,file_obj.info.meta.size)
                # if this fails, refer to https://github.com/williballenthin/python-registry/issues/59
                #registry = Registry.Registry(get_file_data(contents))
                contents = StringIO()
                contents.write(file_data)
                contents.seek(0)
                registry = Registry.Registry(contents)
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

# https://github.com/py4n6/pytsk/blob/master/examples/images.py#L71
# To-Do: This has not been tested
class SplitImage(pytsk3.Img_Info):
    """Virtualize access to split images.
    Note that unlike other tools (e.g. affuse) we do not assume that the images
    are the same size.
    """

    def __init__(self, *files):
        self.fds = []
        self.offsets = [0]
        offset = 0

        for fd in files:
            # Support either a filename or file like objects
            if not hasattr(fd, "read"):
                fd = open(fd, "rb")

            fd.seek(0,2)

            offset += fd.tell()
            self.offsets.append(offset)
            self.fds.append(fd)

        self.size = offset

        # Make sure to call the original base constructor.
        pytsk3.Img_Info.__init__(self, "")

    def get_size(self):
        return self.size

    def read(self, offset, length):
        """Read a buffer from the split image set.
        Handles the buffer straddling images.
        """
        result = ""

        # The total available size in the file
        length = int(length)
        length = min(length, long(self.size) - offset)

        while length > 0:
            data = self._ReadPartial(offset, length)
            if not data: break

            length -= len(data)
            result += data
            offset += len(data)

        return result

    def _ReadPartial(self, offset, length):
        """Read as much as we can from the current image."""
        # The part we need to read from.
        idx = bisect.bisect_right(self.offsets, offset + 1) - 1
        fd = self.fds[idx]

        # The offset this part is in the overall image
        img_offset = self.offsets[idx]
        fd.seek(offset - img_offset)

        # This can return less than length
        return fd.read(length)

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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Grabs basic system info from EnCase EWF (E01) & RAW DD images.')
    parser.add_argument('-i', '--input', metavar="IMAGE", action='store', help='Path to evidence file (First part of segmented/split image)', required=True)
    parser.add_argument('-s', '--sector_size', metavar="SECTORS", action='store', help='Sector size of image (Default is taken from mmls)', type=int)
    parser.add_argument('-t', '--image_type', metavar="TYPE", action='store', choices=['ewf', 'raw'], help='Image type (Default is raw)', default='raw')
    args = vars(parser.parse_args())

    image_type = args['image_type']

    if image_type == "ewf":
        filenames = pyewf.glob(args['input'])
        ewf_handle = pyewf.handle()
        ewf_handle.open(filenames)
        image_handle = EwfImageInfo(ewf_handle)
    else:
        filenames = args['input']
        if not os.path.isdir(filenames):
        #if len(filenames) == 1:
            #image_handle = pytsk3.Img_Info(filenames[0])
            image_handle = pytsk3.Img_Info(filenames)
        else:
            #image_handle = SplitImage(*filenames)
            print("[!] Currently not supporting Split images")
            sys.exit(1)

    evidence_files = {}
    evidence_files['evidence_files'] = filenames
    partition_table = pytsk3.Volume_Info(image_handle)
    partitions = []
    vs_dict = {} #volume system?
    '''
    vs == Volume System?, displays information
    from the top portion of mmls output:

    $ mmls /mnt/evidence/vmdk1
    DOS Partition Table
    Offset Sector: 0
    Units are in 512-byte sectors
    '''

    vs_dict['offset'] = '{0}'.format(partition_table.info.offset) #"Offset Sector: 0"
    vs_dict['block_size'] = '{0}'.format(partition_table.info.block_size) #"Units are in 512-byte sectors"
    vs_dict['part_count'] = '{0}'.format(partition_table.info.part_count) #The total number of partitions on the disk
    #vs_dict['tag'] = '{0}'.format(partition_table.info.tag)
    vs_dict['type'] = '{0}'.format(partition_table.info.vstype) #"DOS Partition Table"

    sector_size = (partition_table.info.block_size if not args['sector_size'] else args['sector_size'])

    result = {
                'image_size': {
                                'bytes': '{0}'.format(image_handle.get_size()),
                                'mb': '{0}'.format(convert_bytes(image_handle.get_size(), 'mb')),
                                'gb': '{0}'.format(convert_bytes(image_handle.get_size(), 'gb')),
                            },
                'partition_details': vs_dict,
                'partition_table': partitions,
            }

    for partition in partition_table:
        partition_dict = {}
        partition_dict['partition_number'] = '{0}'.format(partition.addr)
        partition_dict['slot'] = '{0}'.format(partition.slot_num)
        partition_dict['start'] = '{0}'.format(partition.start)
        partition_mount_start = partition.start * sector_size
        partition_dict['mount_start'] = '{0}'.format(partition_mount_start)
        partition_dict['length'] = '{0}'.format(partition.len)
        partition_dict['size'] = {
                                    'bytes': '{0}'.format(partition.len * sector_size),
                                    'mb': '{0}'.format(convert_bytes(bytes=(partition.len * sector_size), to='mb')),
                                    'gb': '{0}'.format(convert_bytes(bytes=(partition.len * sector_size), to='gb')),
                                }
        partition_dict['description'] = '{0}'.format(partition.desc)
        partition_dict['table_number'] = '{0}'.format(partition.table_num)
        partition_dict['flags'] = '{0}'.format(partition.flags)

        try:
            filesystem_obj = pytsk3.FS_Info(image_handle, offset=(partition_mount_start))
            partition_dict['filesystem'] = '{0}'.format(filesystem_obj.info.ftype)
        except Exception as err:
            partition_dict['filesystem'] = "UNSUPPORTED"
            filesystem_obj = None

        if filesystem_obj:
            # https://github.com/sleuthkit/sleuthkit/blob/develop/tsk/fs/tsk_fs.h#L766
            if "{0}".format(filesystem_obj.info.ftype) in ["TSK_FS_TYPE_NTFS", "TSK_FS_TYPE_NTFS_DETECT"]:
                try:
                    windir = filesystem_obj.open_dir("/Windows")
                    reg_info = RegistryInfo(filesystem_obj)
                    partition_dict['system_details'] = reg_info.get_registry_details()
                except Exception as err:
                    partition_dict['system_details'] = ''
            elif "{0}".format(filesystem_obj.info.ftype) in \
                ["TSK_FS_TYPE_EXT_DETECT", "TSK_FS_TYPE_EXT2", "TSK_FS_TYPE_EXT3", "TSK_FS_TYPE_EXT4"]:
                try:
                    nix_info = LinuxInfo(filesystem_obj)
                    partition_dict['system_details'] = nix_info.get_linux_details()
                except Exception as err:
                    partition_dict['system_details'] = ''

        partitions.append(partition_dict)
    partitions.append([evidence_files])


    print(json.dumps(result, indent=4, sort_keys=True))
