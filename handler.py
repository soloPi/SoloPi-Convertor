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

import os

from decoder import Decoder
from exporter import BaseExporter
from exporter.appium import AppiumExporter
from exporter.macaca import MacacaExporter
from shell import *
from util import is_empty

EXPORTERS = {
    AppiumExporter.get_name(): AppiumExporter,
    MacacaExporter.get_name(): MacacaExporter
}

TAG = "main"


def main():
    path = read("Please input SoloPi case path:")
    content = None
    with open(path) as f:
        content = f.read()

    if is_empty(content):
        log(TAG, "Path %s is invalid" % path)
        return

    case = Decoder().decode(content)
    if case is None:
        log(TAG, "Path %s is invalid" % path)
        return

    selections = []
    for key in EXPORTERS:
        selections.append(key)

    # config export folder
    select = require_selection("Please select transform format", selections)
    handler: BaseExporter = EXPORTERS[selections[select]]()

    folder = read("Please input export folder:")
    os.mkdir(folder)

    main_file = os.path.join(folder, 'main.' + handler.get_file_extension())
    img_folder = os.path.join(folder, 'screenshots')
    os.mkdir(img_folder)

    case_info = case.case_info
    case_info.root = folder
    case_info.img_root = img_folder

    case_list = case.case_list

    # export to main file
    with open(main_file, 'w') as f:
        f.write(handler.export_head(case_info))
        f.write('\n')
        for i in range(len(case_list)):
            f.write(handler.export_step(case_list[i], i + 1, case_info))
            f.write('\n')
        f.write(handler.export_tail(case_info))

    log(TAG, "Export finished")


if __name__ == '__main__':
    main()
