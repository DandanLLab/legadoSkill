
# 网络请求相关

- **ajax**
  - **用途**：访问网络，返回字符串响应体。
  - **使用方法**：`ajax(url)`，其中`url`可以是字符串或包含字符串的列表，表示请求的网址。
  - **参数说明**：
    - `url`：请求网址，若为列表则取第一个元素作为网址。

- **ajaxAll**
  - **用途**：并发访问多个网络地址。
  - **使用方法**：`ajaxAll(urlList)`，`urlList`为网址字符串数组。
  - **参数说明**：
    - `urlList`：包含多个网址字符串的数组。

- **connect**
  - **用途**：访问网络，返回`StrResponse`对象。
  - **使用方法**：
    - `connect(urlStr)`：仅传入网址字符串。
    - `connect(urlStr, header)`：传入网址字符串和请求头字符串（需为JSON格式）。
  - **参数说明**：
    - `urlStr`：请求网址。
    - `header`：请求头，需转换为`Map<String, String>`类型。

- **webView**
  - **用途**：使用`webView`访问网络，可执行js语句获取指定内容。
  - **使用方法**：`webView(html, url, js)`，`html`为载入的html内容，`url`为html资源基础网址，`js`为获取内容的js语句。
  - **参数说明**：
    - `html`：载入的html内容，可为空。
    - `url`：html资源基础网址，可为空。
    - `js`：获取内容的js语句，可为空，若为空则返回整个源代码。

- **webViewGetSource、webViewGetOverrideUrl**
  - **用途**：分别用于使用`webView`获取资源url和跳转url。
  - **使用方法与`webView`类似**，只是多了`sourceRegex`和`overrideUrlRegex`参数，用于匹配资源url和跳转url。
  - **参数说明**：
    - `sourceRegex`：匹配资源url的正则表达式。
    - `overrideUrlRegex`：匹配跳转url的正则表达式。

- **get、head、post**
  - **用途**：分别实现网络访问的get、head、post方法，可进行重定向拦截。
  - **使用方法**：
    - `get(urlStr, headers)`：get请求。
    - `head(urlStr, headers)`：head请求。
    - `post(urlStr, body, headers)`：post请求。
  - **参数说明**：
    - `urlStr`：请求网址。
    - `headers`：请求头`Map`。
    - `body`：post请求的请求体。

# 文件操作相关

- **importScript**
  - **用途**：从网络、本地文件等导入JavaScript脚本。
  - **使用方法**：`importScript(path)`，`path`为脚本路径，可为网络链接、本地文件路径等。
  - **参数说明**：
    - `path`：脚本路径。

- **cacheFile**
  - **用途**：缓存以文本方式保存的文件，如.js、.txt等。
  - **使用方法**：
    - `cacheFile(urlStr)`：不指定缓存时间。
    - `cacheFile(urlStr, saveTime)`：指定缓存时间（秒）。
  - **参数说明**：
    - `urlStr`：文件链接。
    - `saveTime`：缓存时间，单位秒。

- **downloadFile**
  - **用途**：下载文件。
  - **使用方法**：`downloadFile(url)`，`url`为下载地址。
  - **参数说明**：
    - `url`：下载地址，可带参数`type`。

- **getFile、readFile、readTxtFile、deleteFile**
  - **用途**：分别用于获取本地文件对象、读取文件字节、读取文本文件内容、删除本地文件。
  - **使用方法**：
    - `getFile(path)`：获取文件对象。
    - `readFile(path)`：读取文件字节。
    - `readTxtFile(path)`：读取文本文件内容，可指定编码。
    - `deleteFile(path)`：删除文件。
  - **参数说明**：
    - `path`：文件相对路径。
    - `charsetName`：编码格式，可选参数。

- **unzipFile、un7zFile、unrarFile、unArchiveFile**
  - **用途**：分别用于解压zip、7z、rar压缩文件，`unArchiveFile`为通用解压方法。
  - **使用方法**：传入压缩文件相对路径即可。
  - **参数说明**：
    - `zipPath`：压缩文件相对路径。

- **getTxtInFolder**
  - **用途**：读取文件夹内所有文本文件内容，并换行连接。
  - **使用方法**：`getTxtInFolder(path)`，`path`为文件夹相对路径。
  - **参数说明**：
    - `path`：文件夹相对路径。

- **getZipStringContent、getRarStringContent、get7zStringContent**
  - **用途**：分别用于获取zip、rar、7z压缩文件内指定文件的字符串内容。
  - **使用方法**：
    - `getZipStringContent(url, path)`：获取zip文件内容，可指定编码。
    - `getRarStringContent(url, path)`：获取rar文件内容，可指定编码。
    - `get7zStringContent(url, path)`：获取7z文件内容，可指定编码。
  - **参数说明**：
    - `url`：压缩文件链接或十六进制字符串。
    - `path`：所需获取文件在压缩文件内的路径。
    - `charsetName`：编码格式，可选参数。

- **getZipByteArrayContent、getRarByteArrayContent、get7zByteArrayContent**
  - **用途**：分别用于获取zip、rar、7z压缩文件内指定文件的字节数组内容。
  - **使用方法**：传入压缩文件链接或十六进制字符串，以及文件在压缩文件内的路径。
  - **参数说明**：
    - `url`：压缩文件链接或十六进制字符串。
    - `path`：所需获取文件在压缩文件内的路径。

# 编码解码相关

- **strToBytes、bytesToStr**
  - **用途**：分别用于将字符串转换为字节数组、将字节数组转换为字符串。
  - **使用方法**：
    - `strToBytes(str)`、`strToBytes(str, charset)`：字符串转字节数组，可指定编码。
    - `bytesToStr(bytes)`、`bytesToStr(bytes, charset)`：字节数组转字符串，可指定编码。
  - **参数说明**：
    - `str`：待转换字符串。
    - `bytes`：待转换字节数组。
    - `charset`：编码格式。

- **base64Decode、base64Encode**
  - **用途**：分别用于base64解码和编码。
  - **使用方法**：
    - `base64Decode(str)`、`base64Decode(str, charset)`、`base64Decode(str, flags)`：base64解码，可指定编码和标志。
    - `base64Encode(str)`、`base64Encode(str, flags)`：base64编码，可指定标志。
  - **参数说明**：
    - `str`：待解码或编码的字符串。
    - `charset`：编码格式。
    - `flags`：编码或解码标志。

- **base64DecodeToByteArray、base64DecodeToByteArray**
  - **用途**：分别用于base64解码为字节数组。
  - **使用方法**：
    - `base64DecodeToByteArray(str)`、`base64DecodeToByteArray(str, flags)`：base64解码为字节数组，可指定标志。
  - **参数说明**：
    - `str`：待解码的字符串。
    - `flags`：解码标志。

- **hexDecodeToByteArray、hexDecodeToString、hexEncodeToString**
  - **用途**：分别用于十六进制字符串解码为字节数组、解码为utf8字符串、编码为十六进制字符串。
  - **使用方法**：
    - `hexDecodeToByteArray(hex)`：十六进制字符串解码为字节数组。
    - `hexDecodeToString(hex)`：十六进制字符串解码为utf8字符串。
    - `hexEncodeToString(utf8)`：utf8字符串编码为十六进制字符串。
  - **参数说明**：
    - `hex`：待解码的十六进制字符串。
    - `utf8`：待编码的utf8字符串。

- **utf8ToGbk**
  - **用途**：将utf8编码的字符串转换为gbk编码的字符串。
  - **使用方法**：`utf8ToGbk(str)`，传入utf8编码的字符串即可。
  - **参数说明**：
    - `str`：utf8编码的字符串。

- **encodeURI**
  - **用途**：对字符串进行URI编码。
  - **使用方法**：
    - `encodeURI(str)`：使用UTF-8编码。
    - `encodeURI(str, enc)`：可指定编码格式。
  - **参数说明**：
    - `str`：待编码的字符串。
    - `enc`：编码格式。

# 字符串处理相关

- **timeFormatUTC**
  - **用途**：按照指定格式和时区格式化时间戳为字符串。
  - **使用方法**：`timeFormatUTC(time, format, sh)`，`time`为时间戳，`format`为时间格式，`sh`为时区偏移量。
  - **参数说明**：
    - `time`：时间戳，单位为毫秒。
    - `format`：时间格式，如`yyyy-MM-dd HH:mm:ss`。
    - `sh`：时区偏移量，单位为毫秒。

- **timeFormat**
  - **用途**：按照默认格式格式化时间戳为字符串。
  - **使用方法**：`timeFormat(time)`，传入时间戳即可。
  - **参数说明**：
    - `time`：时间戳，单位为毫秒。

- **htmlFormat**
  - **用途**：对html字符串进行格式化，保留图片。
  - **使用方法**：`htmlFormat(str)`，传入html字符串即可。
  - **参数说明**：
    - `str`：待格式化的html字符串。

- **t2s、s2t**
  - **用途**：繁体中文与简体中文相互转换。
  - **使用方法**：
    - `t2s(text)`：繁体转简体。
    - `s2t(text)`：简体转繁体。
  - **参数说明**：
    - `text`：待转换的文本。

# 字体处理相关

- **queryBase64TTF、queryTTF**
  - **用途**：解析字体数据，返回字体解析类。
  - **使用方法**：
    - `queryBase64TTF(data)`：已过时，使用`queryTTF`替代。
    - `queryTTF(data)`：自动判断数据类型并解析，可开启缓存。
    - `queryTTF(data, useCache)`：可手动指定是否开启缓存。
  - **参数说明**：
    - `data`：字体数据，可以是url、本地文件路径、base64字符串或字节数组。
    - `useCache`：是否开启缓存，`true`为开启，默认开启。

- **replaceFont**
  - **用途**：替换文本中的错误字体。
  - **使用方法**：
    - `replaceFont(text, errorQueryTTF, correctQueryTTF)`：不进行过滤。
    - `replaceFont(text, errorQueryTTF, correctQueryTTF, filter)`：可指定是否过滤错误字体中不存在的字符。
  - **参数说明**：
    - `text`：包含错误字体的文本。
    - `errorQueryTTF`：错误的字体解析类。
    - `correctQueryTTF`：正确的字体解析类。
    - `filter`：是否过滤错误字体中不存在的字符，`true`为过滤。

# 其他

- **getSource**
  - **用途**：获取当前的`BaseSource`对象。
  - **使用方法**：直接调用`getSource()`即可。

- **toNumChapter**
  - **用途**：将章节数转换为数字形式。
  - **使用方法**：`toNumChapter(s)`，传入章节字符串即可。
  - **参数说明**：
    - `s`：章节字符串。

- **toURL**
  - **用途**：创建`JsURL`对象。
  - **使用方法**：
    - `toURL(urlStr)`：仅传入网址字符串。
    - `toURL(url, baseUrl)`：传入网址字符串和基础网址。
  - **参数说明**：
    - `urlStr`：网址字符串。
    - `url`：网址字符串。
    - `baseUrl`：基础网址，可选参数。

- **toast、longToast**
  - **用途**：分别用于显示短时和长时的弹窗提示。
  - **使用方法**：
    - `toast(msg)`：短时提示。
    - `longToast(msg)`：长时提示。
  - **参数说明**：
    - `msg`：提示内容，可以是任意类型，将转换为字符串显示。

- **log、logType**
  - **用途**：分别用于输出调试日志和对象类型。
  - **使用方法**：
    - `log(msg)`：输出调试日志。
    - `logType(any)`：输出对象类型。
  - **参数说明**：
    - `msg`：待输出的调试信息。
    - `any`：待输出类型的对象。

- **randomUUID**
  - **用途**：生成UUID。
  - **使用方法**：直接调用`randomUUID()`即可。

- **androidId**
  - **用途**：获取Android设备ID。
  - **使用方法**：直接调用`androidId()`即可。
