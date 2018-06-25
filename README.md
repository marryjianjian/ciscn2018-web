# 题目说明

能正常添加购物车并且结算, 也得单独购买, 秒杀实现物品秒杀, 每位用户限制只能秒杀一次, vip用户除外, vip用户可得到flag

弃用了tornado框架的自带安全hash, 使用了自己定义的hash验证实现用户登录, 使用hash扩展长度攻击实现'vip'用户登录

## flag更新命令

`python update_flag.py`

## hint
1. 秒杀

2. cookie

3. 'vip'用户登录

## checker修改说明

在shopcar_pay_test中添加了id参数


## exp使用的第三方库

- hashpumpy
- pyquery
- requests
