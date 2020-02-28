# SoloPi-Converter

## Introduction (简介)

SoloPi 用例转化工具，支持将 SoloPi JSON 用例转化为其他自动化脚本语言，目前支持转化为 Appium 和 Macaca 脚本。

## Features (功能)

* 支持自定义控件查找方式

* 多种类型转化格式

* 便于扩展其他转换类型

## Discuss (讨论群)

面向行业测试相关从业人员，对工具有什么意见或者建议的话也欢迎 Issue 、 PR 或加群讨论。

- 钉钉群：

## Limitation (限制)

- Python 3.6+
- Pillow

## Getting Started （必看）

1. 执行入口 `python3 handler.py`
2. 输入 SoloPi 脚本地址
3. 选择转化类型（目前支持 Appium 和 Macaca ）
3. 选择输出目录
4. 每一步单独选择查找方式
5. 导出完成，可以在对应目录查看导出的用例脚本，导出的脚本文件会被命名为 main.xxx 。

## 代码导读

- bean: 用例格式定义。
- decoder.py: 解析 SoloPi 原始用例
- exporter: 实际导出用例的 module ，已实现 Appium 和 Macaca 导出，其他语言可以通过扩展 BaseExporter 的形式来实现。
- handler.py: 主流程执行器
- shell.py: 用于处理用户输入、选择
- util: 常用功能

## Related projects (相关的项目)

[SoloPi 自动化测试工具](https://github.com/alipay/SoloPi)

[版权声明](NOTICE.md)

## Contribution (参与贡献)

   独乐乐不如众乐乐，开源的核心还是在于技术的分享交流，当你对开源项目产生了一些想法时，有时还会有更加Smart的表达方式，比如(Thanks to uiautomator2)：

   - 我们的业务需要这项功能 ==> 我加了个功能，可以在很多场景用到，已经提交MR了。

   - 这块儿功能有更详细的文档吗？ ==> 这块内容我改了一下，更方便使用了，帮忙合并一下。

   - 我在XXX上怎么用不了啊？ ==> 在XXX手机上功能有点问题，我已经修复了。

   - 我刚用了XXX功能，怎么和文档上不一样啊？ ==> 我根据文档试用了一下，碰到了一些坑，这是我在ATA、Lark发的踩坑贴，有些内容可以补充一下。

   - 这个是不是一直维护啊？ ==> 我能做些什么？

   当然，Star、Fork、Merge Request、Issue等功能也随时欢迎大家使用哈！

   如果你有什么好的想法，也可以与我们直接联系，进行更加深入的讨论，我们希望将这套移动端的测试工具框架进行更好的推广，欢迎大家多多宣传。

## License (协议)

This project is under the Apache 2.0 License. See the [LICENSE](LICENSE) file for the full license text.

```text
Copyright (C) 2015-present, Ant Financial Services Group

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Disclaimer (免责声明)

[免责声明](Disclaimer.md)