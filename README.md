# kumori - 更自由地调用腾讯云API

腾讯云的python sdk又长又臭，而且更新还不及时，用着不是很巴适，所以包装了一下腾讯云的API的调用方式。

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
