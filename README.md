####1、 变更记录
v0.0.8 


1. 增加consumer_tag 功能, 以便在rabit web 页面显示消费者
2. 增加发送日志至日志中心功能
```python
from ys_service import *


@ys_host.register("YS.机票.国内.退票.wiken.DEBUG", prefetch=1, consumer_tag="wiken")
def refund(context):
    print("bigin:", context.text)
    re = context.send_log_to_center(
        context=context,
        project="wikenTest",
        module="test1",
        user="7921",
        level="error",
        return_msg="log_center_test",
        field1="111111",
        field2="自愿",
        field3="国内",
    )

    print("result:", re)
    context.ack()    


with ys_host:
    ys_host.start()
```
