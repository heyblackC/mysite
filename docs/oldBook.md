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
    "id": id,                           // [NoWrite]
    "page_view": 102,                   // [NoWrite]
    "created_at": timestamp,            // [NoWrite]
    "title": "数字信号处理",             // [Required]
    "author": "Sanjit K. Mitra",        // [Required]
    "publisher": "电子工业出版社",       // [Required]
    "description": "这是一本...",       // [Optional]
    "expires": "2016-12-11 17:17:10",  // [Required]
    "wear_degree": "0",                // [Required] "0": 较好, "1": 一般, "2": 严重
    "contact": "15521377055",          // [Required]
    "contact_type": "0",               // [Required] "0": 手机, "1": 微信, "2": qq

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

---

### 部分请求示例
#### POST - 发布一个新的旧书籍信息
POST /book HTTP/1.1

Content-Type: multipart/form-data
```js
{
	"form-TOTAL_FORMS": "2",      // 0-3范围内的一个值，具体看有多少张图片要传；这里假设2张照片要传
	"form-INITIAL_FORMS": "0",    // 初始化的FORMS个数，固定为"0"就好
	"form-MIN_NUM_FORMS": "0",    // 固定就好
	"form-MAX_NUM_FORMS": "3",    // 最大上传的照片数，为3，固定
  	// ------------
  	"form-0-image": 图片文件1,     // 图片文件file
  	"form-1-image": 图片文件2,     // 命名规则：form-<id>-image，<id>最大为2
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

---

### 响应
#### POST - 发布成功
会返回新建书籍信息的id、图片url及其他基本信息

HTTP/1.1 200 OK

Content-Type: application/json
```js
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
