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

from bean.case import CaseInfo
from bean.step import Step, Node, Method
from exporter import BaseExporter
from shell import require_selection
from util import *


class AppiumExporter(BaseExporter):
    """
    Appium Export
    """

    STEP_INDEX_MAP = {
        "Text": lambda x: "driver.find_element_by_name(%s)" % unquotation(x.text),
        "Description": lambda x: "driver.find_element_by_accessibility_id(%s)" % unquotation(x.description),
        "Xpath": lambda x: "driver.find_element_by_xpath(%s)" % unquotation(x.xpath),
        "ResourceId": lambda x: "driver.find_element_by_id(%s)" % unquotation(x.res_id),
        "ClassName": lambda x: "driver.find_element_by_tag_name(\"%s\")" % x.class_name,
        "Capture": lambda x: "driver.find_element_by_image(\"%s\")" % x
    }
    HEAD_INFO = '''from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from PIL import Image
import re
import os
import time

def load_x_y(rect, percent):
    try:
        xs, ys = percent.split(',', 1)
        x = int(rect.left + float(xs) * rect.width())
        y = int(rect.top + float(ys) * rect.height())
        return x, y
    except:
        return rect.center_x(), rect.center_y()

def swipe(driver, rect, from_percent, to_percent, duration):
    fx, fy = load_x_y(rect, from_percent)
    tx, ty = load_x_y(rect, to_percent)
    driver.swipe(fx, fy, tx, ty, duration)
    
def wait_node(get_node, max_time):
    n = None
    start = time.time()
    while time.time() - start < max_time:
        try:
            n = get_node()
            if n is not None:
                break
        except:
            pass
    return n is not None


class WrapTouchAction:
    def __init__(self, driver, rect=None, percent=None, x=None, y=None) -> None:
        touch = TouchAction(driver)
        if x is None or y is None:
            if percent is None or ',' not in percent:
                x = rect.center_x()
                y = rect.center_y()
            else:
                x, y = load_x_y(rect, percent)
        touch.press(x=x, y=y)
        self.touch = touch

    def move_to(self, rect=None, percent=None, x=None, y=None, time=500):
        if x is None or y is None:
            if percent is None or ',' not in percent:
                x = rect.center_x()
                y = rect.center_y()
            else:
                x, y = load_x_y(rect, percent)
        self.touch.move_to(x=x, y=y).wait(time)
        return self

    def perform(self):
        self.touch.release().perform()

PLATFORM = '%s'
PACKAGE = '%s'
ACTIVITY = ''

desired_caps = {}
desired_caps['platformName'] = PLATFORM
desired_caps['platformVersion'] = ''
desired_caps['deviceName'] = ''
desired_caps['appPackage'] = PACKAGE
desired_caps['appActivity'] = ACTIVITY

driver = webdriver.Remote('', desired_caps)

# Take Screenshot to get real screen size
assert driver.get_screenshot_as_file("/tmp/_solo_test.png")
screen = Image.open('/tmp/_solo_test.png')
width, height = screen.size
screen.close()
os.remove('/tmp/_solo_test.png')
SCREEN = {'x': 0, 'y': 0, 'height': height, 'width': width}
'''

    TAIL_INFO = '\ndriver.quit()'

    SELECT_NODE_ATTR_INFO = '''Please select an attribute below for node location'''

    @staticmethod
    def get_name() -> str:
        return "Appium(Python)"

    def get_file_extension(self) -> str:
        return "py"

    def export_head(self, case_info: CaseInfo) -> str:
        return self.HEAD_INFO % (case_info.platform, case_info.target_app_package)

    def export_tail(self, case_info: CaseInfo) -> str:
        return self.TAIL_INFO

    def export_step(self, step: Step, index: int, case_info: CaseInfo) -> str:
        if step.node is not None:
            return self.export_node_step(step.node, step.method, index, case_info)
        else:
            return self.export_global_step(step.method, index, case_info)

    def export_node_step(self, node: Node, method: Method, index: int, case_info: CaseInfo) -> str:
        node_location = self.read_node_locate_way(node, index, case_info.img_root, case_info.root)
        return export_node_action(node_location, method)

    def export_global_step(self, method: Method, index: int, case_info: CaseInfo) -> str:
        return export_method_action(method)

    def read_node_locate_way(self, node: Node, index: int, img_root: str, root: str) -> str:
        selections = []
        display = []
        if not is_empty(node.text):
            selections.append("Text")
            display.append("Text: " + node.text)

        if not is_empty(node.description):
            selections.append("Description")
            display.append("Description: " + node.text)

        if not is_empty(node.res_id):
            selections.append("ResourceId")
            display.append("ResourceId: " + node.res_id)

        if not is_empty(node.class_name):
            selections.append("ClassName")
            display.append("ClassName: " + node.class_name)

        if not is_empty(node.xpath):
            selections.append("Xpath")
            display.append("Xpath: " + node.xpath)

        target_location = None
        if img_root is not None and node.capture is not None:
            node.export_capture("/tmp/tmp.jpg")
            target_location = os.path.join(img_root, '%d.png' % (index + 1))
            export_png("/tmp/tmp.jpg", target_location)

            selections.append("Capture")
            display.append("Capture: " + target_location)

        selection = require_selection(self.SELECT_NODE_ATTR_INFO, display)
        if selection < 0:
            return ""

        # Get location way
        select_type = selections[selection]
        if select_type == 'Capture':
            return self.STEP_INDEX_MAP[select_type](target_location.replace(root + '/', ''))
        else:
            return self.STEP_INDEX_MAP[select_type](node)



def load_x_y(percent):
    try:
        xs, ys = percent.split(',', 1)
        return float(xs), float(ys)
    except:
        return 0.5, 0.5


def export_node_action(node_location: str, method: Method) -> str:
    me = method.method
    px, py = load_x_y(method.get_param("localClickPos", "0.5,0.5"))
    text = method.get_param("text")
    if me == 'CLICK' or me == 'CLICK_QUICK':
        return "%s.click()" % node_location
    elif me == 'CLICK_IF_EXISTS':
        return '''try:
    %s.click()
except NoSuchElementException: 
    pass''' % node_location
    elif me == 'LONG_CLICK':
        return '''action = TouchAction(driver)
action.long_press(%s, duration=%s)
action.perform()''' % (node_location, method.get_param("text", "2000"))
    elif me == 'SCROLL_TO_BOTTOM':
        text = un_empty(text, "100")
        ty = py + int(text) / 100
        return '''rect = %s.rect
swipe(rect, '%s,%s', '%s,%s', 300)''' % (node_location, px, py, px, ty)
    elif me == 'SCROLL_TO_TOP':
        text = un_empty(text, "100")
        ty = py - int(text) / 100
        return '''rect = %s.rect
swipe(rect, '%s,%s', '%s,%s', 300)''' % (node_location, px, py, px, ty)
    elif me == 'SCROLL_TO_RIGHT':
        text = un_empty(text, "100")
        tx = px + int(text) / 100
        return '''rect = %s.rect
swipe(rect, '%s,%s', '%s,%s', 300)''' % (node_location, px, py, tx, py)
    elif me == 'SCROLL_TO_LEFT':
        text = un_empty(text, "100")
        tx = px - int(text) / 100
        return '''rect = %s.rect
swipe(rect, '%s,%s', '%s,%s', 300)''' % (node_location, px, py, tx, py)
    elif me == 'INPUT' or me == 'SAFETY_INPUT':
        text = un_empty(text, "")
        return '''%s.send_keys(%s)
driver.execute_script("mobile: hideKeyboard")''' % (node_location, unquotation(text))
    elif me == 'INPUT_SEARCH':
        text = un_empty(text, "")
        return '''ele = %s
ele.send_keys(%s)
driver.execute_script("mobile:performEditorAction", {"action": "done"})''' % (node_location, unquotation(text))
    elif me == 'ASSERT':
        assert_mode = method.get_param('assertMode')
        assert_content = method.get_param('assertInputContent')
        if assert_mode == 'assert_accurate':
            return "assert %s.text == %s" % (node_location, unquotation(assert_content))
        elif assert_mode == 'assert_contain':
            return "assert %s in %s.text" % (unquotation(assert_content), node_location)
        elif assert_mode == 'assert_regular':
            return "assert re.match(r%s, %s.text) is not None" % (unquotation('^' + assert_content + '$'), node_location)
        elif assert_mode == 'assert_dayu':
            return "assert float(%s.text) > float('%s')" % (node_location, assert_content)
        elif assert_mode == 'assert_dayuAndEqual':
            return "assert float(%s.text) >= float('%s')" % (node_location, assert_content)
        elif assert_mode == 'assert_equal':
            return "assert float(%s.text) == float('%s')" % (node_location, assert_content)
        elif assert_mode == 'assert_xiaoyu':
            return "assert float(%s.text) < float('%s')" % (node_location, assert_content)
        elif assert_mode == 'assert_xiaoyuAndEqual':
            return "assert float(%s.text) <= float('%s')" % (node_location, assert_content)
        else:
            return ""
    elif me == 'GESTURE':
        points_str = method.get_param('gesturePath')
        ges_filter = int(method.get_param('gestureFilter'))
        points = json.loads(points_str)
        action = 'rect = %s.rect\nWrapTouchAction(driver, rect, "%s,%s")' % \
                 (node_location, points[0]['x'], points[0]['y'])
        for i in range(1, len(points)):
            point = points[i]
            action += '.move_to(rect, "%s,%s", time=%s)' % (point.get('x'), point.get('y'), ges_filter)

        return action + '.perform()'
    elif me == 'SLEEP_UNTIL':
        max_time = int(text) / 1000
        return 'assert wait_node(lambda: %s, %s)' % (node_location, max_time)
    else:
        return ""


def export_method_action(method: Method) -> str:
    me = method.method
    text = method.get_param("text")
    if me == 'BACK':
        return 'driver.back()'
    elif me == 'MENU':
        return 'driver.keyevent(1)'
    elif me == 'KEYCODE_GLOBAL':
        return 'driver.press_keycode(%s)' % text
    elif me == 'HANDLE_ALERT':
        return '''try :
    alert = driver.switchTo().alert()
    alert.accpet()
except:
    pass'''
    elif me == 'JUMP_TO_PAGE':
        return '''driver.execute_script('mobile: shell', {
    'command': 'am',
    'args': ['start', '\'%s\''],
    'includeStderr': True,
    'timeout': 5000
})''' % method.get_param('scheme')
    elif me == 'GLOBAL_GESTURE':
        points_str = method.get_param('gesturePath')
        ges_filter = int(method.get_param('gestureFilter'))
        points = json.loads(points_str)
        action = 'WrapTouchAction(driver, SCREEN, "%s,%s")' % \
                 (points[0]['x'], points[0]['y'])
        for i in range(1, len(points)):
            point = points[i]
            action += '.move_to(SCREEN, "%s,%s", time=%s)' % (point.get('x'), point.get('y'), ges_filter)

        return action + '.perform()'
    elif me == 'HOME':
        return 'driver.keyevent(3)'
    elif me == 'EXECUTE_SHELL':
        if text.startswith('adb shell '):
            text = text[10:]
        split = text.split(' ')
        return '''driver.execute_script('mobile: shell', {
    'command': %s,
    'args': %s,
    'includeStderr': True,
    'timeout': 5000
})''' % (unquotation(split[0]), unquotation(split[1:]))
    elif me == 'GLOBAL_SCROLL_TO_BOTTOM':
        distance = method.get_param('scrollDistance')
        time = method.get_param('ScrollTime')
        distance = int(un_empty(distance, '40')) / 100
        distance = max(min(distance, 0.9), 0.1)
        time = un_empty(time, '300')
        return 'swipe(SCREEN, \'%s,%s\', \'%s,%s\', %s)' % (0.5, 0.5 - distance / 2, 0.5, 0.5 + distance / 2, time)
    elif me == 'GLOBAL_SCROLL_TO_TOP':
        distance = method.get_param('scrollDistance')
        time = method.get_param('ScrollTime')
        distance = int(un_empty(distance, '40')) / 100
        distance = max(min(distance, 0.9), 0.1)
        time = un_empty(time, '300')
        return 'swipe(SCREEN, \'%s,%s\', \'%s,%s\', %s)' % (0.5, 0.5 + distance / 2, 0.5, 0.5 - distance / 2, time)
    elif me == 'GLOBAL_SCROLL_TO_RIGHT':
        distance = method.get_param('scrollDistance')
        time = method.get_param('ScrollTime')
        distance = int(un_empty(distance, '40')) / 100
        distance = max(min(distance, 0.9), 0.1)
        time = un_empty(time, '300')
        return 'swipe(SCREEN, \'%s,%s\', \'%s,%s\', %s)' % (0.5 - distance / 2, 0.5, 0.5 + distance / 2, 0.5, time)
    elif me == 'GLOBAL_SCROLL_TO_LEFT':
        distance = method.get_param('scrollDistance')
        time = method.get_param('ScrollTime')
        distance = int(un_empty(distance, '40')) / 100
        distance = max(min(distance, 0.9), 0.1)
        time = un_empty(time, '300')
        return 'swipe(SCREEN, \'%s,%s\', \'%s,%s\', %s)' % (0.5 + distance / 2, 0.5, 0.5 - distance / 2, 0.5, time)
    elif me == 'SLEEP':
        return 'time.sleep(%s)' % (int(text) / 1000)
    elif me == 'RESTART_APP' or me == 'GOTO_INDEX':
        return '''driver.close_app()
time.sleep(1000)
driver.start_activity(PACKAGE, ACTIVITY)
'''
    elif me == 'SCREENSHOT':
        return 'driver.save_screenshot(\'%s.png\')' % text
    elif me == 'KILL_PROCESS':
        return 'driver.close_app()'
    else:
        return ""
