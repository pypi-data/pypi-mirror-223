# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: SystemInfo (experimental)

from __future__ import annotations

import enum
import typing
from dataclasses import dataclass

from .util import T_JSON_DICT


@dataclass
class GPUDevice:
    '''
    Describes a single graphics processor (GPU).
    '''
    #: PCI ID of the GPU vendor, if available; 0 otherwise.
    vendor_id: float

    #: PCI ID of the GPU device, if available; 0 otherwise.
    device_id: float

    #: String description of the GPU vendor, if the PCI ID is not available.
    vendor_string: str

    #: String description of the GPU device, if the PCI ID is not available.
    device_string: str

    #: String description of the GPU driver vendor.
    driver_vendor: str

    #: String description of the GPU driver version.
    driver_version: str

    #: Sub sys ID of the GPU, only available on Windows.
    sub_sys_id: typing.Optional[float] = None

    #: Revision of the GPU, only available on Windows.
    revision: typing.Optional[float] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['vendorId'] = self.vendor_id
        json['deviceId'] = self.device_id
        json['vendorString'] = self.vendor_string
        json['deviceString'] = self.device_string
        json['driverVendor'] = self.driver_vendor
        json['driverVersion'] = self.driver_version
        if self.sub_sys_id is not None:
            json['subSysId'] = self.sub_sys_id
        if self.revision is not None:
            json['revision'] = self.revision
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUDevice:
        return cls(
            vendor_id=float(json['vendorId']),
            device_id=float(json['deviceId']),
            vendor_string=str(json['vendorString']),
            device_string=str(json['deviceString']),
            driver_vendor=str(json['driverVendor']),
            driver_version=str(json['driverVersion']),
            sub_sys_id=float(json['subSysId']) if json.get('subSysId', None) is not None else None,
            revision=float(json['revision']) if json.get('revision', None) is not None else None,
        )


@dataclass
class Size:
    '''
    Describes the width and height dimensions of an entity.
    '''
    #: Width in pixels.
    width: int

    #: Height in pixels.
    height: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['width'] = self.width
        json['height'] = self.height
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Size:
        return cls(
            width=int(json['width']),
            height=int(json['height']),
        )


@dataclass
class VideoDecodeAcceleratorCapability:
    '''
    Describes a supported video decoding profile with its associated minimum and
    maximum resolutions.
    '''
    #: Video codec profile that is supported, e.g. VP9 Profile 2.
    profile: str

    #: Maximum video dimensions in pixels supported for this ``profile``.
    max_resolution: Size

    #: Minimum video dimensions in pixels supported for this ``profile``.
    min_resolution: Size

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['profile'] = self.profile
        json['maxResolution'] = self.max_resolution.to_json()
        json['minResolution'] = self.min_resolution.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoDecodeAcceleratorCapability:
        return cls(
            profile=str(json['profile']),
            max_resolution=Size.from_json(json['maxResolution']),
            min_resolution=Size.from_json(json['minResolution']),
        )


@dataclass
class VideoEncodeAcceleratorCapability:
    '''
    Describes a supported video encoding profile with its associated maximum
    resolution and maximum framerate.
    '''
    #: Video codec profile that is supported, e.g H264 Main.
    profile: str

    #: Maximum video dimensions in pixels supported for this ``profile``.
    max_resolution: Size

    #: Maximum encoding framerate in frames per second supported for this
    #: ``profile``, as fraction's numerator and denominator, e.g. 24/1 fps,
    #: 24000/1001 fps, etc.
    max_framerate_numerator: int

    max_framerate_denominator: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['profile'] = self.profile
        json['maxResolution'] = self.max_resolution.to_json()
        json['maxFramerateNumerator'] = self.max_framerate_numerator
        json['maxFramerateDenominator'] = self.max_framerate_denominator
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> VideoEncodeAcceleratorCapability:
        return cls(
            profile=str(json['profile']),
            max_resolution=Size.from_json(json['maxResolution']),
            max_framerate_numerator=int(json['maxFramerateNumerator']),
            max_framerate_denominator=int(json['maxFramerateDenominator']),
        )


class SubsamplingFormat(enum.Enum):
    '''
    YUV subsampling type of the pixels of a given image.
    '''
    YUV420 = "yuv420"
    YUV422 = "yuv422"
    YUV444 = "yuv444"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> SubsamplingFormat:
        return cls(json)


class ImageType(enum.Enum):
    '''
    Image format of a given image.
    '''
    JPEG = "jpeg"
    WEBP = "webp"
    UNKNOWN = "unknown"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> ImageType:
        return cls(json)


@dataclass
class ImageDecodeAcceleratorCapability:
    '''
    Describes a supported image decoding profile with its associated minimum and
    maximum resolutions and subsampling.
    '''
    #: Image coded, e.g. Jpeg.
    image_type: ImageType

    #: Maximum supported dimensions of the image in pixels.
    max_dimensions: Size

    #: Minimum supported dimensions of the image in pixels.
    min_dimensions: Size

    #: Optional array of supported subsampling formats, e.g. 4:2:0, if known.
    subsamplings: typing.List[SubsamplingFormat]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['imageType'] = self.image_type.to_json()
        json['maxDimensions'] = self.max_dimensions.to_json()
        json['minDimensions'] = self.min_dimensions.to_json()
        json['subsamplings'] = [i.to_json() for i in self.subsamplings]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ImageDecodeAcceleratorCapability:
        return cls(
            image_type=ImageType.from_json(json['imageType']),
            max_dimensions=Size.from_json(json['maxDimensions']),
            min_dimensions=Size.from_json(json['minDimensions']),
            subsamplings=[SubsamplingFormat.from_json(i) for i in json['subsamplings']],
        )


@dataclass
class GPUInfo:
    '''
    Provides information about the GPU(s) on the system.
    '''
    #: The graphics devices on the system. Element 0 is the primary GPU.
    devices: typing.List[GPUDevice]

    #: An optional array of GPU driver bug workarounds.
    driver_bug_workarounds: typing.List[str]

    #: Supported accelerated video decoding capabilities.
    video_decoding: typing.List[VideoDecodeAcceleratorCapability]

    #: Supported accelerated video encoding capabilities.
    video_encoding: typing.List[VideoEncodeAcceleratorCapability]

    #: Supported accelerated image decoding capabilities.
    image_decoding: typing.List[ImageDecodeAcceleratorCapability]

    #: An optional dictionary of additional GPU related attributes.
    aux_attributes: typing.Optional[dict] = None

    #: An optional dictionary of graphics features and their status.
    feature_status: typing.Optional[dict] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['devices'] = [i.to_json() for i in self.devices]
        json['driverBugWorkarounds'] = [i for i in self.driver_bug_workarounds]
        json['videoDecoding'] = [i.to_json() for i in self.video_decoding]
        json['videoEncoding'] = [i.to_json() for i in self.video_encoding]
        json['imageDecoding'] = [i.to_json() for i in self.image_decoding]
        if self.aux_attributes is not None:
            json['auxAttributes'] = self.aux_attributes
        if self.feature_status is not None:
            json['featureStatus'] = self.feature_status
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> GPUInfo:
        return cls(
            devices=[GPUDevice.from_json(i) for i in json['devices']],
            driver_bug_workarounds=[str(i) for i in json['driverBugWorkarounds']],
            video_decoding=[VideoDecodeAcceleratorCapability.from_json(i) for i in json['videoDecoding']],
            video_encoding=[VideoEncodeAcceleratorCapability.from_json(i) for i in json['videoEncoding']],
            image_decoding=[ImageDecodeAcceleratorCapability.from_json(i) for i in json['imageDecoding']],
            aux_attributes=dict(json['auxAttributes']) if json.get('auxAttributes', None) is not None else None,
            feature_status=dict(json['featureStatus']) if json.get('featureStatus', None) is not None else None,
        )


@dataclass
class ProcessInfo:
    '''
    Represents process info.
    '''
    #: Specifies process type.
    type_: str

    #: Specifies process id.
    id_: int

    #: Specifies cumulative CPU usage in seconds across all threads of the
    #: process since the process start.
    cpu_time: float

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['type'] = self.type_
        json['id'] = self.id_
        json['cpuTime'] = self.cpu_time
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ProcessInfo:
        return cls(
            type_=str(json['type']),
            id_=int(json['id']),
            cpu_time=float(json['cpuTime']),
        )


def get_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.Tuple[GPUInfo, str, str, str]]:
    '''
    Returns information about the system.

    :returns: A tuple with the following items:

        0. **gpu** - Information about the GPUs on the system.
        1. **modelName** - A platform-dependent description of the model of the machine. On Mac OS, this is, for example, 'MacBookPro'. Will be the empty string if not supported.
        2. **modelVersion** - A platform-dependent description of the version of the machine. On Mac OS, this is, for example, '10.1'. Will be the empty string if not supported.
        3. **commandLine** - The command line string used to launch the browser. Will be the empty string if not supported.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'SystemInfo.getInfo',
    }
    json = yield cmd_dict
    return (
        GPUInfo.from_json(json['gpu']),
        str(json['modelName']),
        str(json['modelVersion']),
        str(json['commandLine'])
    )


def get_feature_state(
        feature_state: str
) -> typing.Generator[T_JSON_DICT, T_JSON_DICT, bool]:
    '''
    Returns information about the feature state.

    :param feature_state:
    :returns: 
    '''
    params: T_JSON_DICT = dict()
    params['featureState'] = feature_state
    cmd_dict: T_JSON_DICT = {
        'method': 'SystemInfo.getFeatureState',
        'params': params,
    }
    json = yield cmd_dict
    return bool(json['featureEnabled'])


def get_process_info() -> typing.Generator[T_JSON_DICT, T_JSON_DICT, typing.List[ProcessInfo]]:
    '''
    Returns information about all running processes.

    :returns: An array of process info blocks.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'SystemInfo.getProcessInfo',
    }
    json = yield cmd_dict
    return [ProcessInfo.from_json(i) for i in json['processInfo']]
