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

from bean.case import CaseInfo, Case
from datetime import datetime

from bean.step import *
from util import *


class Decoder(object):
    """
    SoloPi Case Decoder
    """

    def decode(self, content: str) -> Case:
        case = json.loads(content)
        if case is None or type(case) is not dict:
            return None

        advance = json.loads(case.get('advanceSettings'))
        platform = un_empty(advance.get('platform'), 'Android')
        case_info = CaseInfo(case.get('caseName'), case.get('caseDesc'), case.get('targetAppLabel'),
                             case.get('targetAppPackage'), datetime.fromtimestamp(case.get('gmtCreate') / 1000),
                             datetime.fromtimestamp(case.get('gmtModify') / 1000), platform)

        case_wrap = json.loads(case.get('operationLog'))
        case_list = case_wrap.get('steps')

        real_step_list = []
        for case in case_list:
            step = self.decode_step(case)
            if step is not None:
                real_step_list.append(step)

        case_info.step_count = len(real_step_list)
        return Case(case_info, real_step_list)

    def decode_step(self, case) -> Step:
        node_map = case.get('operationNode')
        method_map = case.get('operationMethod')
        if method_map is None:
            return None

        target_node = None
        if node_map is not None:
            target_node = self.decode_node(node_map)

        target_method = Method(method_map.get('actionEnum'), method_map.get('operationParam'))
        return Step(target_node, target_method)

    def decode_node(self, node):
        rect_map = node.get('nodeBound')
        rect = Rect(rect_map.get('left'), rect_map.get('top'), rect_map.get('right'), rect_map.get('bottom'))
        extra = node.get('extra')
        capture = None
        if extra is not None:
            capture_str = extra.get('captureImage')
            if capture_str is not None and not is_empty(capture_str):
                capture = decode_base64(capture_str)
        return Node(node.get('nodeType'), node.get('text'), node.get('xpath'), node.get('description'),
                    node.get('resourceId'), node.get('className'), rect, capture)
