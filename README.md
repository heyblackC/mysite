﻿# mysite
## 旧书籍系统后台项目代码
这是我和同学合作进行的大作业项目，后期希望能够投入到学院内实际使用。

## 须知
想要调用接口的话，请先阅读docs/下的**common.md**、**book.md**和**user.md**等文件，里面有接口规范和调用规则说明。

---

## 未完成
1. [x] 支持PATCH和DELETE请求，完善restful API
2. [x] /book的GET请求可以指定begin和take
3. [x] 更换后端为MySQL
4. [x] 部署至服务器上
5. [x] webhook搭建
6. [ ] image、avatar使用cdn或者对象存储，并且提供缩略图
7. [x] 全部接口使用session维持对话
8. [ ] page_view计数
9. [ ] 后台逻辑完善，比如expires过期时间必须为未来，并编写自动化测试单元
10. [ ] 将form替换为serializer，支持json数据
11. [ ] 考虑index页面和detail页面的区别，对数据进行部分返回
12. [ ] 敏感字段，如contact和password，应该采用加密传输方式

---

## 工程手札
2018/11/22 14:53

完成了webhook搭建，使用的是github+jenkins

---

2018/11/23 03:00

完成了user资源对象的创建，接口使用session进行认证。

另外，sessionid的过期日期有问题，待修复；

form的validate仅支持form-data，不支持json数据，极其不友好，应改为serializer。

---


