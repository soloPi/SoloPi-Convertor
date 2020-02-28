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

from datetime import datetime


class CaseInfo(object):

    def __init__(self, case_name: str, case_desc: str, target_app_label: str, target_app_package: str,
                 create_time: datetime, modify_time: datetime, platform: str, step_count: int = None, root: str = None,
                 img_root: str = None):
        self.img_root = img_root
        self.root = root
        self.case_name = case_name
        self.case_desc = case_desc
        self.target_app_label = target_app_label
        self.target_app_package = target_app_package
        self.create_time = create_time
        self.modify_time = modify_time
        self.platform = platform
        self.step_count = step_count


class Case(object):
    def __init__(self, case_info: CaseInfo, case_list: list):
        self.case_info = case_info
        self.case_list = case_list