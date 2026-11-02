# 浏览器从输入 URL 到页面加载完成发生了什么？

## 1. 用户输入 URL

当用户在浏览器地址栏中输入一个 URL，例如：

`https://www.example.com/index.html`

浏览器首先会判断输入内容是一个网址还是搜索关键词。如果判断为 URL，就会开始访问该网站。

URL 一般包含协议、域名、端口、路径、查询参数等部分，例如：

- `https`：使用的通信协议
- `www.example.com`：域名
- `/index.html`：访问的资源路径

---

## 2. 浏览器解析 URL

浏览器会对 URL 进行解析，确定需要使用什么协议、访问哪个服务器以及请求哪个资源。

例如：

`https://www.example.com/index.html`

浏览器可以得到：

- 协议：HTTPS
- 域名：`www.example.com`
- 默认端口：443
- 请求路径：`/index.html`

如果使用 HTTP 协议，默认端口一般为 80；如果使用 HTTPS 协议，默认端口一般为 443。

浏览器随后需要根据域名找到目标服务器的 IP 地址。

---

## 3. DNS 域名解析

网络通信实际上依赖 IP 地址，而用户通常输入的是容易记忆的域名，因此浏览器需要通过 DNS 将域名转换为对应的 IP 地址。

浏览器通常会按照一定顺序查找 DNS 信息：

1. 浏览器 DNS 缓存
2. 操作系统 DNS 缓存
3. 本地 hosts 文件
4. 本地 DNS 服务器
5. 根域名服务器、顶级域名服务器和权威 DNS 服务器

如果缓存中已经存在结果，就可以直接使用，从而减少查询时间。

得到 IP 地址之后，浏览器就知道应该与哪台服务器建立连接。

---

## 4. 建立网络连接

获得服务器 IP 地址后，浏览器需要与服务器建立网络连接。

对于普通 HTTP 网站，通常会先建立 TCP 连接。

TCP 建立连接时需要进行“三次握手”：

1. 客户端向服务器发送连接请求 SYN
2. 服务器返回 SYN + ACK
3. 客户端再发送 ACK

三次握手完成后，TCP 连接建立成功。

如果访问的是 HTTPS 网站，还需要在 TCP 连接建立之后进行 TLS 握手。

TLS 握手的主要作用包括：

- 验证服务器身份
- 协商加密算法
- 建立加密通信所需的密钥

完成这些步骤后，浏览器和服务器之间就可以开始安全地传输 HTTP 数据。

---

## 5. 发送 HTTP 请求

网络连接建立完成后，浏览器会向服务器发送 HTTP 请求。

一个 HTTP 请求通常包括：

- 请求方法，例如 `GET`、`POST`
- 请求的资源路径
- 请求头 Header
- 请求体 Body（部分请求才有）

例如：

```text
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Chrome
```

其中：

- `GET` 表示请求获取资源
- `/index.html` 表示访问的资源路径
- `Host` 表示目标网站
- `User-Agent` 用来说明浏览器类型等信息

---

## 6. 服务器处理并返回 HTTP 响应

服务器收到 HTTP 请求后，会根据请求内容进行处理。

服务器可能执行：

1. 判断资源是否存在
2. 读取静态文件
3. 查询数据库
4. 执行后端程序
5. 生成网页内容

处理完成后，服务器向浏览器返回 HTTP 响应。

HTTP 响应一般包含：

- 状态码
- 响应头
- 响应体

常见状态码包括：

- `200 OK`：请求成功
- `301 / 302`：页面重定向
- `404 Not Found`：资源不存在
- `500 Internal Server Error`：服务器内部错误

---

## 7. 浏览器解析 HTML

浏览器收到服务器返回的 HTML 后，会从上到下解析 HTML 内容。

例如：

```html
<html>
  <body>
    <h1>Hello</h1>
    <p>这是一个网页</p>
  </body>
</html>
```

浏览器会将 HTML 标签解析成树状结构，称为 **DOM（Document Object Model，文档对象模型）**。

例如：

```text
html
└── body
    ├── h1
    └── p
```

DOM 是浏览器后续进行页面显示以及 JavaScript 操作的重要基础。

---

## 8. 加载 CSS、JavaScript、图片等资源

浏览器在解析 HTML 时，如果发现页面还引用了其他资源，就会继续发送新的网络请求。

例如：

```html
<link rel="stylesheet" href="style.css" />
<script src="main.js"></script>
<img src="photo.jpg" />
```

浏览器会分别请求：

- `style.css`
- `main.js`
- `photo.jpg`

因此，一个网页的加载通常不只是一次 HTTP 请求，而是会产生多个网络请求。

CSS 主要负责页面的样式和布局，JavaScript 主要负责页面的行为和交互。

---

## 9. 构建 DOM 树和 CSSOM 树

浏览器解析 HTML 时，会构建 **DOM 树**。

与此同时，浏览器解析 CSS 文件和 `<style>` 标签中的样式规则，并构建 **CSSOM（CSS Object Model，CSS 对象模型）树**。

可以简单理解为：

```text
HTML → DOM
CSS  → CSSOM
```

DOM 描述网页中“有什么内容”，CSSOM 描述这些内容“应该以什么样式显示”。

随后，浏览器会结合 DOM 和 CSSOM，生成用于页面显示的 **渲染树（Render Tree）**。

渲染树主要包含实际需要在页面中显示的元素。

因此可以简单概括为：

```text
HTML → DOM
          \
           → Render Tree
          /
CSS → CSSOM
```

---

## 10. 页面布局与绘制

生成渲染树之后，浏览器需要计算每个元素在屏幕上的实际位置和大小，这个过程称为 **Layout（布局）**。

例如浏览器需要计算：

- 一个标题距离页面左侧多少像素
- 一张图片宽度和高度是多少
- 一个按钮应该出现在什么位置

完成布局后，浏览器进入 **Paint（绘制）** 阶段。

在绘制阶段，浏览器会把：

- 文字
- 背景
- 边框
- 图片
- 阴影

等内容绘制到屏幕上。

复杂网页还可能被分成多个图层，最后由浏览器进行合成（Composite），最终形成用户看到的页面。

因此网页显示过程可以简单概括为：

```text
DOM + CSSOM
    ↓
Render Tree
    ↓
Layout
    ↓
Paint
    ↓
Composite
    ↓
页面显示
```

---

## 11. JavaScript 执行与页面交互

浏览器加载网页时，还会执行页面中的 JavaScript 程序。

JavaScript 可以读取和修改 DOM，例如：

```javascript
document.querySelector("h1").innerText = "新的标题";
```

执行这段代码后，页面上的标题内容会发生变化。

JavaScript 还可以完成：

- 按钮点击事件
- 表单提交
- 页面动画
- 动态修改 HTML
- 向服务器发送新的网络请求
- 根据服务器返回的数据更新页面

例如很多网页打开后，商品列表、评论、用户头像等内容可能不是一开始就写在 HTML 中，而是通过 JavaScript 再向服务器请求数据，然后动态显示。

因此，现代网页通常不是一次加载完后就完全不变，而是可以持续与服务器进行通信。

---

## 12. 页面加载完成

当浏览器完成主要 HTML 文档的解析，并加载页面所需资源后，页面就逐渐进入可使用状态。

浏览器中有两个比较常见的事件：

### DOMContentLoaded

表示 HTML 已经解析完成，DOM 树已经建立。

但此时图片等部分资源可能仍然没有完全加载完成。

### load

表示页面及其依赖资源，例如图片、CSS 等已经基本加载完成。

因此，通常可以把浏览器加载网页的整个过程概括为：

```text
输入 URL
   ↓
解析 URL
   ↓
DNS 查询
   ↓
建立 TCP / TLS 连接
   ↓
发送 HTTP 请求
   ↓
服务器返回 HTTP 响应
   ↓
解析 HTML
   ↓
加载 CSS / JavaScript / 图片
   ↓
构建 DOM 和 CSSOM
   ↓
生成 Render Tree
   ↓
Layout
   ↓
Paint / Composite
   ↓
执行 JavaScript
   ↓
页面加载并呈现给用户
```

## 总结

浏览器从输入 URL 到看到页面，并不是简单地“下载一个网页”，而是涉及 DNS、TCP、HTTPS、HTTP、HTML、CSS、JavaScript 和浏览器渲染等多个过程。

从网络角度来看，主要经历：

**DNS → 建立连接 → HTTP 请求与响应**

从浏览器角度来看，主要经历：

**HTML/CSS 解析 → DOM/CSSOM → 渲染树 → 布局 → 绘制**

最终这些步骤共同完成一个网页从服务器传输到用户屏幕的整个过程。
