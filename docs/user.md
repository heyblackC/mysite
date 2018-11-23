# user API

|简述|URI与操作|备注|
|-|-|-|
|项目根URL|http://oldBook.heyblack.top|项目的根URL，其他路径均相对于根URL而言|
|新建用户|`Resource: /user/create`|仅允许`POST`|
|登陆验证|`Resource: /user/authenticate`|仅允许 `POST`|
|登出|`Resource: /user/logout`|仅允许 `GET`|
|授权说明|`create`和`authenticate`会设置`session`；`logout`会删除`session`|访问`logout`时，必须处于授权（已登陆）状态|

---

## session和cookie授权说明
成功访问`/user/create`和`/user/authenticate`后，

服务器会在客户端设置key为`sessionid`的cookie，用于标识用户；

且在服务器端设置键值为`user_id: user.id`的session，以持久化用户已登录状态；

`book.md`中的部分接口需要先进行用户验证，详见`book.md`；

Max-Age为15*60，即15min后session过期

---

## 用户对象
```js
{
    "id": 1,                       // [Hidden]
    "username": "heyblack",        // [Required], Unique
    "password": "123123"           // [Required]
    "avatar": "http://..."         // [Optional]
}
```

---

## 部分请求及响应示例

### 创建新用户

> 注意：
用户名必须唯一，
avatar为可选字段

#### 请求

POST /user/create HTTP/1.1

Request URL: http://oldBook.heyblack.top/user/create

Content-Type: multipart/form-data, application/json

```js
{
    "username": "heyblack",
    "password": "123123",
    "avatar": "http://xxx"
}
```

#### 响应

HTTP/1.1 200 OK

Content-Type: application/json

```js
{
    "id": 1,
    "username": "heyblack",
    "avatar": "http://xxx"
}
```

---

### 用户登出

> 注意：
必须先登陆

#### 请求

GET /user/logout HTTP/1.1

Request URL: http://oldBook.heyblack.top/user/logout

#### 响应

HTTP/1.1 200 OK

Content-Type: application/json

```js
{
    "status": "success",
    "message": "you logout now."
}
```

---