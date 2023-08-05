#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import logging
import re
import fosslight_util.constant as constant
import mmap
from ._license_matched import MatchedLicense
from ._scan_item import ScanItem
from ._scan_item import is_exclude_dir
from ._scan_item import is_exclude_file
from ._scan_item import replace_word

logger = logging.getLogger(constant.LOGGER_NAME)
_exclude_directory = ["test", "tests", "doc", "docs"]
_exclude_directory = [os.path.sep + dir_name +
                      os.path.sep for dir_name in _exclude_directory]
_exclude_directory.append("/.")
remove_license = ["warranty-disclaimer"]


def get_error_from_header(header_item):
    has_error = False
    str_error = ""
    key_error = "errors"

    try:
        for header in header_item:
            if key_error in header:
                errors = header[key_error]
                error_cnt = len(errors)
                if error_cnt > 0:
                    has_error = True
                    str_error = '{}...({})'.format(errors[0], error_cnt)
                    break
    except Exception as ex:
        logger.debug(f"Error_parsing_header: {ex}")
    return has_error, str_error


def parsing_file_item(scancode_file_list, has_error, path_to_scan, need_matched_license=False):

    rc = True
    scancode_file_item = []
    license_list = {}  # Key :[license]+[matched_text], value: MatchedLicense()
    msg = []

    prev_dir = ""
    prev_dir_value = False
    regex = re.compile(r'licenseref-(\S+)', re.IGNORECASE)
    find_word = re.compile(rb"SPDX-PackageDownloadLocation\s*:\s*(\S+)", re.IGNORECASE)

    if scancode_file_list:
        for file in scancode_file_list:
            try:
                is_dir = False
                file_path = file.get("path", "")
                if not file_path:
                    continue
                is_binary = file.get("is_binary", False)
                if "type" in file:
                    is_dir = file["type"] == "directory"
                    if is_dir:
                        prev_dir_value = is_exclude_dir(file_path)
                        prev_dir = file_path

                if not is_binary and not is_dir:
                    licenses = file.get("licenses", [])
                    copyright_list = file.get("copyrights", [])

                    result_item = ScanItem(file_path)

                    fullpath = os.path.join(path_to_scan, file_path)

                    urls = file.get("urls", [])
                    url_list = []

                    if urls:
                        with open(fullpath, "r") as f:
                            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmap_obj:
                                for word in find_word.findall(mmap_obj):
                                    url_list.append(word.decode('utf-8'))
                    result_item.download_location = url_list

                    if has_error and "scan_errors" in file:
                        error_msg = file.get("scan_errors", [])
                        if len(error_msg) > 0:
                            result_item.comment = ",".join(error_msg)
                            scancode_file_item.append(result_item)
                            continue
                    copyright_value_list = []
                    for x in copyright_list:
                        latest_key_data = x.get("copyright", "")
                        if latest_key_data:
                            copyright_data = latest_key_data
                        else:
                            copyright_data = x.get("value", "")
                        if copyright_data:
                            try:
                                copyright_data = re.sub(r'SPDX-License-Identifier\s*[\S]+', '', copyright_data, flags=re.I)
                                copyright_data = re.sub(r'DownloadLocation\s*[\S]+', '', copyright_data, flags=re.I).strip()
                            except Exception:
                                pass
                            copyright_value_list.append(copyright_data)

                    result_item.copyright = copyright_value_list

                    # Set the license value
                    license_detected = []
                    if licenses is None or licenses == "":
                        continue

                    license_expression_list = file.get("license_expressions", {})
                    if len(license_expression_list) > 0:
                        license_expression_list = [
                            x.lower() for x in license_expression_list
                            if x is not None]

                    for lic_item in licenses:
                        license_value = ""
                        key = lic_item.get("key", "")
                        if key in remove_license:
                            if key in license_expression_list:
                                license_expression_list.remove(key)
                            continue
                        spdx = lic_item.get("spdx_license_key", "")
                        # logger.debug("LICENSE_KEY:"+str(key)+",SPDX:"+str(spdx))

                        if key is not None and key != "":
                            key = key.lower()
                            license_value = key
                            if key in license_expression_list:
                                license_expression_list.remove(key)
                        if spdx is not None and spdx != "":
                            # Print SPDX instead of Key.
                            license_value = spdx.lower()

                        if license_value != "":
                            if key == "unknown-spdx":
                                try:
                                    matched_txt = lic_item.get("matched_text", "")
                                    matched = regex.search(matched_txt)
                                    if matched:
                                        license_value = str(matched.group())
                                except Exception:
                                    pass

                            for word in replace_word:
                                if word in license_value:
                                    license_value = license_value.replace(word, "")
                            license_detected.append(license_value)

                            # Add matched licenses
                            if need_matched_license and "category" in lic_item:
                                lic_category = lic_item["category"]
                                if "matched_text" in lic_item:
                                    lic_matched_text = lic_item["matched_text"]
                                    lic_matched_key = license_value + lic_matched_text
                                    if lic_matched_key in license_list:
                                        license_list[lic_matched_key].set_files(file_path)
                                    else:
                                        lic_info = MatchedLicense(license_value, lic_category, lic_matched_text, file_path)
                                        license_list[lic_matched_key] = lic_info

                        matched_rule = lic_item.get("matched_rule", {})
                        result_item.is_license_text = matched_rule.get("is_license_text", False)

                    if len(license_detected) > 0:
                        result_item.licenses = license_detected

                        if len(license_expression_list) > 0:
                            license_expression_list = list(
                                set(license_expression_list))
                            result_item.comment = ','.join(license_expression_list)

                        if is_exclude_file(file_path, prev_dir, prev_dir_value):
                            result_item.exclude = True
                        scancode_file_item.append(result_item)
            except Exception as ex:
                msg.append(f"Error Parsing item: {ex}")
                rc = False
    msg = list(set(msg))
    return rc, scancode_file_item, msg, license_list
