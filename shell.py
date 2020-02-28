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


def require_selection(info: str, selection: list) -> int:
    """
    Read User Selection
    :param info:
    :param selection:
    :return:
    """
    if selection is None or len(selection) == 0:
        # no selection provided
        return -1

    print(info)
    for i in range(len(selection)):
        print("[%d] %s" % (i + 1, selection[i]))

    i = 0
    while i < 3:
        raw_input = input("Please select[%d-%d]:" % (1, len(selection)))
        try:
            select = int(raw_input)
            if len(selection) >= select > 0:
                return select - 1
        except:
            print("Invalid input: %s" % raw_input)
        i += 1
    return -1


def read(info: str) -> str:
    return input(info)


def log(tag: str, info: str):
    print('[%s] %s' % (tag, info))
