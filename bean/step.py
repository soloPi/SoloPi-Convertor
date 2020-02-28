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

from bean import Rect


class Node(object):
    def __init__(self, node_type: str, text: str, xpath: str,
                 description: str, res_id: str, class_name: str, bound: Rect, capture: bytearray):
        self.node_type = node_type
        self.text = text
        self.xpath = xpath
        self.description = description
        self.res_id = res_id
        self.class_name = class_name
        self.bound = bound
        self.capture = capture

    def has_capture(self) -> bool:
        return self.capture is not None

    def export_capture(self, file: str) -> bool:
        """
        Export capture to file
        :param file: target file
        """
        if not self.has_capture():
            return False
        with open(file, "wb") as f:
            f.write(self.capture)
            return True


class Method(object):
    def __init__(self, method: str, param: dict):
        self.method = method
        self.param = dict(param)

    def get_param(self, key: str, default=None):
        val = self.param.get(key)
        if val is None:
            return default
        return val


class Step(object):
    """
    SoloPi Step Item
    """

    def __init__(self, node: Node, method: Method) -> None:
        super().__init__()
        self.node = node
        self.method = method
