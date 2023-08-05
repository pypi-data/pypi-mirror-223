# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import hashlib
import json
import logging
import os
from abc import abstractmethod
from pathlib import Path
from uuid import UUID

from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.model import obj
from majormode.perseus.model.date import ISO8601DateTime
from majormode.perseus.utils import cast

from bootloader.ue.constant.ue_asset import ASSET_CLASS_NAME_MAPPING
from bootloader.ue.constant.ue_asset import UnrealEngineAssetClass


class UnrealEngineAsset:
    # The path prefix of Unreal Engine standard classes.
    UNREAL_ENGINE_STANDARD_CLASS_PATH_PREFIX = '/Script/Engine/'

    def __eq__(self, other: UnrealEngineAsset):
        """
        Check whether this asset is the same as another asset.

        Two assets are equivalent if they have the same name, the same class,
        and the same package name.


        :param other: Another asset.


        :return: ``True`` if the two assets are the same; ``False`` otherwise.
        """
        return other is not None \
            and self.__asset_class_path == other.asset_class_path \
            and self.__asset_name == other.asset_name \
            and self.__package_name == other.package_name

    def __init__(
            self,
            asset_name: str,
            asset_class_path: str,
            package_name: str,
            dependencies: list[str] or None,
            asset_id: UUID = None,
            object_status: ObjectStatus = None,
            references: list[str] or None = None,
            tags: list[str] or None = None,
            update_time: ISO8601DateTime or None = None,
            version_code: int or None = None):
        """
        Build a new {@link UAsset}.


        :param asset_name: The name of the asset without the package.

        :param asset_class_path: The path name of the asset’s class.

        :param package_name: The name of the package in which the asset is
            found.

        :param dependencies: The list of names of the packages that the asset
            depends on.

        :param asset_id: The identification of the asset, when already
            registered to the back-end platform.

        :param object_status: The current status of the asset.

        :param references: The list of pacakge names of the asset that depend
            on this asset.

        :param tags: The list of tags associated with the asset.

        :param update_time: The time of the most recent modification of some
            mutable attributes of the asset, such as its status, its list of
            tags, and its picture.

        :param version_code: A positive integer used as an internal version
            number.  This number helps determine whether one version is more
            recent than another, with higher numbers indicating more recent
            versions.
        """
        self.__asset_id = asset_id
        self.__asset_name = asset_name
        self.__asset_class_path = asset_class_path
        self.__package_name = package_name
        self.__dependencies = dependencies
        self.__references = references
        self.__tags = tags
        self.__object_status = object_status
        self.__update_time = update_time
        self.__version_code = version_code

    def __str__(self):
        """
        Return the string representation of this asset.


        :return: Return a stringified JSON expression of this asset.
        """
        return json.dumps(obj.stringify(self.to_json(), trimmable=True))

    @property
    def asset_class(self) -> UnrealEngineAssetClass:
        """
        Return the asset's class.

        For example, the class of a `/Script/Engine/SkeletalMesh` asset is
        `AssetClass.SkeletalMesh`


        :return: The class of the asset, or `None` if the class is not defined
            (i.e., a user-defined class).
        """
        class_name = self.__asset_class_path.split('/')[-1]
        try:
            asset_class = cast.string_to_enum(class_name, UnrealEngineAssetClass)
            return asset_class
        except ValueError as error:
            logging.exception(error)

    @property
    def asset_class_name(self) -> str:
        """
        Return the humanly readable name of the asset's class.

        For example, the humanly readable name of the class
        `/Script/Engine/SkeletalMesh` is `Skeletal Mesh`.


        :return: The humanly readable name of the asset's class, or ``None``
            if the asset's class doesn't correspond to an Unreal Engine
            standard class.
        """
        asset_class_name = ASSET_CLASS_NAME_MAPPING.get(self.asset_class)
        if asset_class_name is None and not self.has_standard_class():
            logging.warning(
                f"The Unreal Engine class {self.asset_class} might not be properly"
                f"declared in the enumeration 'UnrealEngineAssetClass'"
            )
        return asset_class_name

    @property
    def asset_class_path(self) -> str:
        """
        Return the path name of the asset's class.

        Examples:

        ```text
        /Script/Engine/SkeletalMesh
        /Script/Engine/Skeleton
        /Script/Engine/Texture2D
        ```

        :return: The path name of the asset's class.
        """
        return self.__asset_class_path

    @property
    def asset_id(self) -> UUID:
        if self.__asset_id is None:
            raise ValueError(f"No identification defined for the asset {self.__package_name}")

        return self.__asset_id

    @asset_id.setter
    def asset_id(self, asset_id: UUID):
        if self.__asset_id is not None:
            raise ValueError(f"The asset {self.__asset_name} has already an identification ({self.__asset_id})")

        self.__asset_id = asset_id

    @property
    def asset_name(self) -> str:
        """
        Return the name of the asset.


        :return: The name of the asset without the package.
        """
        return self.__asset_name

    @asset_name.setter
    def asset_name(self, asset_name):
        """
        Change the name of the asset.


        :param asset_name: The new name of the asset without the package.
        """
        logging.debug(f"Changing the name of the asset {self.__asset_name} with {asset_name}")
        self.__asset_name = asset_name

    @property
    def dependencies(self) -> list[str] or None:
        """
        Return the list of names of the packages that the asset depends on.


        :return: The list of names of the packages that the asset depends on.
        """
        return self.__dependencies

    @staticmethod
    def from_json(payload: any):
        if isinstance(payload, str):
            payload = json.loads(payload)

        # @todo: Check data consistency (type, path, list of strings, etc.)
        return UnrealEngineAsset(
            payload['asset_name'],
            payload['asset_class_path'],
            payload['package_name'],
            payload['dependencies']
        )

    def has_standard_class(self):
        """
        Indicate whether this asset has a standard Unreal Engine class.

        Developers can create their own Unreal Engine classes such as
        ``/Script/ControlRigDeveloper/ControlRigBlueprint``, or even more
        specific to their game, such as ``/Game/Scooby/D_ARSessionConfig``.

        Unreal Engine classes are prefixed with ``/Script/Engine/``.


        :return: ``True`` if this asset has a standard Unreal Engine class;
            ``False`` if this asset has a custom class.
        """
        return self.asset_class_path.startswith(self.UNREAL_ENGINE_STANDARD_CLASS_PATH_PREFIX)

    @property
    def object_status(self) -> ObjectStatus or None:
        """
        Return The current status of the asset.


        :return: The current status of the asset.
        """
        return self.__object_status

    @property
    def package_name(self) -> str:
        """
        Return the name of the package in which the asset is found.


        :return: The name of the package in which the asset is found.
        """
        return self.__package_name

    @package_name.setter
    def package_name(self, package_name: str):
        """
        Change the package name of the asset.


        :param package_name: The new name of the asset's package.
        """
        logging.debug(f"Changing the package name of the asset {self.__asset_name} with {package_name}")
        self.__package_name = package_name

    @property
    def references(self) -> list[str] or None:
        """
        Return the list of names of the packages of the assets that reference
        this asset.


        :return: The list of names of the packages of the assets that
            reference this asset.
        """
        return self.__references

    @property
    def tags(self) -> list[str] or None:
        """
        Return the list of tags associated to the asset.


        :return: The list of tags associated with the asset.
        """
        return self.__tags

    def to_json(self) -> any:
        """
        Serialize the asset's information to a JSON expression.


        :return: A JSON expression representing the asset's information.
        """
        return {
            'asset_id': self.__asset_id,
            'asset_name': self.__asset_name,
            'asset_class_path': self.__asset_class_path,
            'dependencies': self.__dependencies,
            'object_status': self.__object_status,
            'package_name': self.__package_name,
            'references': self.__references,
            'tags': self.__tags,
            'update_time': self.__update_time,
            'version_code': self.__version_code,
        }

    @property
    def update_time(self) -> ISO8601DateTime or None:
        """
        Return the time of the most recent modification of some mutable
        attributes of the asset.

        The mutable attributes of the asset are its status, the list of
        its tags, and its picture.


        :return: The time of the most recent modification of some mutable
            attributes of the asset.
        """
        return self.__update_time

    @property
    def version_code(self) -> int or None:
        """
        Return a positive integer used as an internal version number.

        This number helps determine whether one version is more recent than
        another, with higher numbers indicating more recent versions.


        :return: A positive integer used as an internal version number.
        """
        return self.__version_code


class UnrealEngineAbstractAssetFile:
    def __eq__(self, other: UnrealEngineAbstractAssetFile):
        """
        Check whether this asset is the same as another asset.

        Two assets are equivalent if they have the same name, the same class,
        the same package name, and the same file's checksum.


        :param other: Another asset.


        :return: ``True`` if the two assets are the same; ``False`` otherwise.
        """
        return other is not None \
            and self.file_checksum == other.file_checksum \
            and self.__asset == other.asset

    def __init__(
            self,
            asset: UnrealEngineAsset):
        """
        Build a new {@link UAsset}.
        """
        self.__asset = asset

    def __str__(self):
        """
        Return the string representation of this asset file.


        :return: Return a stringified JSON expression of this asset file.
        """
        return json.dumps(obj.stringify(self.to_json(), trimmable=True))

    @property
    def asset(self) -> UnrealEngineAsset:
        """
        Return the information of the asset contained in this file.


        :return: An asset.
        """
        return self.__asset

    @property
    @abstractmethod
    def file_checksum(self) -> str:
        """
        Return the SHA256 message digest of the binary data of the asset file.


        :return: The SHA256 message digest of the binary data of the asset
            file.
        """
        pass

    @property
    @abstractmethod
    def file_size(self) -> int:
        """
        Return the size of the asset file.


        :return: The size in bytes of the asset file.
        """
        pass

    def to_json(self) -> any:
        """
        Serialize the asset file's information to a JSON expression.


        :return: A JSON expression representing the asset file's information.
        """
        payload = self.__asset.to_json()
        payload['file_size'] = self.file_size
        payload['file_checksum'] = self.file_checksum
        return payload


class UnrealEngineRecordAssetFile(UnrealEngineAbstractAssetFile):
    """
    Represent the information of an asset as registered in a database.
    """
    def __init__(
            self,
            asset: UnrealEngineAsset,
            file_size: int,
            file_checksum: str):
        """
        :param asset:

        :param file_checksum: The SHA256 message digest of the binary data of
            the asset file.

        """
        super().__init__(asset)
        self.__file_checksum = file_checksum
        self.__file_size = file_size

    @property
    def file_checksum(self) -> str:
        """
        Return the SHA256 message digest of the binary data of the asset file.


        :return: The SHA256 message digest of the binary data of the asset
            file.
        """
        return self.__file_checksum

    @file_checksum.setter
    def file_checksum(self, file_checksum: str):
        """
        Set the SHA256 message digest of the binary data of the asset file
        when its content has changed.


        :param file_checksum: The SHA256 message digest of the binary data of
            the asset file.
        """
        logging.debug(
            f"The checksum of the asset file {self.asset.asset_name} has changed "
            f"from the value {self.__file_checksum} to the value {file_checksum}"
        )
        self.__file_checksum = file_checksum

    @property
    def file_size(self) -> int:
        """
        Return the size of the asset file.


        :return: The size in bytes of the asset file.
        """
        return self.__file_size

    @file_size.setter
    def file_size(self, file_size: int):
        """
        Set the size of the asset file when its content has changed.


        :param file_size: The size in bytes of the asset file.
        """
        logging.debug(
            f"The size of the asset file {self.asset.asset_name} has changed "
            f"from the value {self.__file_size} to the value {file_size}"
        )
        self.__file_size = file_size

    @staticmethod
    def from_json(payload: any) -> UnrealEngineRecordAssetFile:
        """
        Return an asset as stored in a database record.

        :param payload: The JSON data of the asset.


        :return: An asset.
        """
        asset = UnrealEngineAsset.from_json(payload)
        return UnrealEngineRecordAssetFile(
            asset,
            payload['file_size'],
            payload['file_checksum']
        )


class UnrealEngineRealAssetFile(UnrealEngineAbstractAssetFile):
    """
    Represent the file of an asset stored on the file system.
    """
    FILE_READ_BLOCK_SIZE = 4096

    def __init__(
            self,
            asset: UnrealEngineAsset,
            file_path_name: Path):
        super().__init__(asset)

        if not os.path.exists(file_path_name):
            error_message = f"The file {file_path_name} of the asset {asset.asset_name} doesn't exist"
            logging.error(error_message)
            raise FileNotFoundError(error_message)

        file_status = Path.stat(file_path_name)
        self.__file_size = file_status.st_size

        self.__asset = asset
        self.__file_path_name = file_path_name
        self.__file_checksum = None  # This attribute is lazy loaded (cf. property `file_checksum`)

    def __calculate_file_checksum(self) -> str:
        """
        Calculate the SHA256 message digest of the binary data of the asset
        file.


        :return: The SHA256 message digest of the binary data of the asset
            file.
        """
        sha256_hash = hashlib.sha256()

        with open(self.__file_path_name, 'rb') as fd:
            # Read and update hash string value in blocks of bytes.
            for byte_block in iter(lambda: fd.read(self.FILE_READ_BLOCK_SIZE), b''):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    @property
    def file_checksum(self) -> str:
        """
        Return the SHA256 message digest of the binary data of the asset file.


        :return: The SHA256 message digest of the binary data of the asset
            file.
        """
        if self.__file_checksum is None:
            self.__file_checksum = self.__calculate_file_checksum()

        return self.__file_checksum

    @property
    def file_path_name(self) -> Path:
        """
        Return the path and name of the asset's file.


        :return: The path and name of the asset's file.
        """
        return self.__file_path_name

    @property
    def file_size(self) -> int:
        """
        Return the size of the asset file.


        :return: The size in bytes of the asset file.
        """
        return self.__file_size
