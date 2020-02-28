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

from abc import abstractmethod

from bean.case import CaseInfo
from bean.step import Step


class BaseExporter(object):
    """
    Export SoloPi case to file
    """

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """
        Get name for this exporter
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Get File Extension for this type
        :return:
        """
        pass

    def export_head(self, case_info: CaseInfo) -> str:
        """
        Export file head, you can export some universal method in this part
        """
        return ""

    @abstractmethod
    def export_step(self, step: Step, index: int, case_info: CaseInfo) -> str:
        """
        Export every step
        """
        pass

    def export_tail(self, case_info: CaseInfo) -> str:
        """
        Export file tail, for driver stop
        """
        return ""
