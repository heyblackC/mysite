# oldBook API

|简述|URI与操作|备注|
|-|-|-|
|登陆|`POST /login`|使用波板糖的用户系统（教务验证）登陆|
|个人信息|`Resource: /me`|允许 `GET, PATCH`|
|获取用于七牛上传的token|`GET /token`|需要登陆状态，`token` 有效期 1800 秒|
|统一微信OAuth回调|`GET /wx_oauth/{redirect}`|请仔细阅读详细说明|

## 用户对象
* 波板糖原数据库内的 `sex` 字段和其他字段根本就没有存到有意义的值，因此此处暂时移除
```js
{
    "id": id,                   // [NoWrite]
    "account": "201xxx..",      // [Required]
    "password": "blabla",       // [Required, Hidden]
    "nick": "nick name",        // [Required]
    "name": "real name",        // [Required]
    "sex": 0,                   // [Optional]  0: 未知, 1: 男, 2: 女
    "grade": 2016,              // [Optional]
    "college": "",              // [Optional]
    "phone": "",                // [Optional]
    "dormitory": "",            // [Optional]
    "qq": "",                   // [Optional]
    "created_at": timestamp,    // [NoWrite]
    "updated_at": timestamp     // [NoWrite]
    // 其他字段待定
}
```

---

## 表示当前登陆的用户资源 /me
* 关于资源 `uri` 上能够进行的操作以及默认的请求与回复见文档 [readme.md](./readme.md)
### 允许的操作
* PATCH
* GET
### 回复
* 如果用户未处于登陆状态，则返回状态码 `401` 并按标准错误格式返回提示信息。
* 如果用户处于登录状态，则返回当前登陆**用户资源对象**


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


