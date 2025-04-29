# kumori - 更自由地调用腾讯云API

[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-368/) [![](https://img.shields.io/pypi/v/kumori
)](https://pypi.org/project/kumori/)

腾讯云的python sdk很冗长，而且更新不及时，甚至有些API不会出现在sdk里，用着不是很巴适。因此包装了一下腾讯云的API的调用方式，以实现调用更多API的目的。

## Installation

```bash
pip install kumori
```

## Usage

```python
import os
from kumori.qcloud import User
# 创建一个用户
user = User(os.getenv('QCLOUD_SID'), os.getenv('QCLOUD_SKEY'), 'ap-guangzhou')
# 调用 API
resp = user.cvm.DescribeInstances(Limit=20, Offset=0)
print(resp)
```

默认情况下，如果API返回Error、代码将会抛出Exception。可以通过 `console.suppress_errors()` 屏蔽掉

```python
from kumori.qcloud import console

with console.suppress_errors():
    # 不会抛出异常
    resp = user.cvm.DescribeInstances(Unknown="Key")
# 这里会抛出异常
user.cvm.DescribeInstances(Unknown="Key")
```

## Advanced

kumori 内置了 [cvm 在内的若干个产品的调用](./src/kumori/qcloud/core.py#L142)。如果你想要调用的产品在这里没出现，可以手动添加：

```python
from kumori.qcloud import console, User

console.add_service('abc', '2025-04-29')

user = User(
  # sid=...
  # skey=...
)

user.abc.DescribeYourPPT(Limit=10, Offset=2)
```

## TODO
- [ ] v3 signature
- [ ] cos