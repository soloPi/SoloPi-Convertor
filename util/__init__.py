# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import base64

from PIL import Image


def unquotation(content: str) -> str:
    """
    remove quotation
    :param content:
    :return:
    """
    return json.dumps(content, ensure_ascii=False)


def export_png(source: str, target: str):
    """
    export image to png
    :param source:
    :param target:
    :return:
    """
    img = Image.open(source)
    img = img.convert('RGB')
    img.save(target)


def is_empty(content: str):
    """
    :param content:
    :return: is empty
    """
    if content is None or len(content.strip()) == 0:
        return True
    return False


def un_empty(content: str, default: str):
    """
    Ensure not empty
    :param content:
    :param default:
    :return:
    """
    if is_empty(content):
        return default
    return content


def decode_base64(content: str) -> bytearray:
    """
    decode base64 string to bytearray
    :param content:
    :return:
    """
    base64_info = content.encode('ascii')
    return bytearray(base64.b64decode(base64_info))
