# oldBook API

|简述|URI与操作|备注|
|-|-|-|
|项目根URL|http://www.oldBook.heyblack.top|项目的根URL，其他路径均相对于根URL而言|
|旧书籍信息|`Resource: /book`|允许`GET, POST, PATCH, DELETE`|
|用户信息|`Resource: /me`|允许 `GET, PATCH`|

---
## 旧书籍对象
```js
{
    "id": id,					     // [NoWrite]
    "page_view": 102,                 // [NoWrite]
    "created_at": timestamp           // [NoWrite]
    "title": "数字信号处理",		  // [Required]
    "author": "Sanjit K. Mitra",      // [Required]
    "publisher": "电子工业出版社",    // [Required]
    "description": "这是一本...",     // [Optional]
    "expires": "2016-12-11 17:17:10", // [Required]
    "wear_degree": "0",			   // [Required] "0": 较好, "1": 一般, "2": 严重
    "contact": "15521377055",         // [Required]
    "contact_type": "0",			  // [Required] "0": 手机, "1": 微信, "2": qq
    
    // 注意：
    // Required字段都不能为空；
    // Optional字段可以不传，也可以为空
    // 时间格式为：%Y-%m-%d %H:%M:%S
}
```

---

## 对旧书籍资源进行操作 /book

### 允许的操作
* GET
* POST
* PATCH
* DELETE

### 部分请求示例
#### POST - 发布一个新的旧书籍信息
```json
{
	"form-TOTAL_FORMS": "2",		  // 0-3范围内的一个值，具体看有多少张图片要传；这里假设2张照片要传
	"form-INITIAL_FORMS": "0",		// 初始化的FORMS个数，固定为"0"就好
	"form-MIN_NUM_FORMS": "0",		// 固定就好
	"form-MAX_NUM_FORMS": "3",		// 最大上传的照片数，为3，固定
    // ------------
    "form-0-image": 图片文件1,		// 图片文件file
    "form-1-image": 图片文件2,		// 命名规则：form-<id>-image，<id>最大为2
    // ------------
	"author": "Sanjit K. Mitra",
	"title": "数字信号处理",
	"publisher": "电子工业出版社",
	"expires": "2016-12-11 17:17:10", //信息过期时间，必须在未来
	"description": "这是一本电信学子普遍很...",
	"wear_degree": "0",
	"contact": "15521377055",
	"contact_type": "0"
}
```

### 响应
#### POST - 发布成功
会返回新建书籍信息的id、图片url及其他基本信息
```json
{
    "author": "sadqweqwewqe",
    "expires": "2019-12-11 17:17:10",
    "page_view": 0,
    "image_set": [
        "http://www.oldBook.heyblack.top/images/30/4f4975b8cfd794e11fb8ff487e1199c1.jpg",
        "http://www.oldBook.heyblack.top/images/30/a42c73071a0f1fc74c9442d64d07450f.jpg"
    ],
    "created_at": "2018-11-18 08:18:33",
    "id": 30,
    "publisher": "0",
    "description": "",
    "wear_degree": 0,
    "contact": "15521377055",
    "title": "asdadasdasdasda",
    "contact_type": 0
}
```

---


## 注册
* 不存在的，在用户调用登陆接口时，后台根据教务情况去教务判断用户凭证，如果从教务登陆成功则记录到数据库，否则返回认证错误。

## 登陆
* 注意，用户不存在时后台根据教务情况自动判断并且完成认证，认证失败按登陆失败算
* 也有其他情况导致登陆失败，例如密码过期（可能由于教务的情况发生变化等等），这些情况在返回时也按登陆失败来算，具体信息在 `message` 字段中提示。
**请求**
```http
POST /login HTTP/1.1
Content-Type: application/json

{
    "account": "201xxxxxxxxx"，
    "password": "blabla"
}
```
**回复**
```http
============登陆失败============
HTTP/1.1 401 Unauthorized
Content-Type: application/json

/* 标准错误信息 */
{
    "status": "error",
    "message": "用户名与密码不匹配!"
}

============登陆成功============
HTTP/1.1 200 OK
Content-Type: application/json

/* 当前用户资源对象 */
```

## 七牛上传token
**文档待补充**


### 微信网页通常授权过程
1. 用户打开业务页
2. 跳转微信授权链接
3. 微信确认授权后跳转回调页
4. 服务端拉取用户信息