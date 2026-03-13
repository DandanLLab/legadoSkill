### AnalyzeUrl 构造函数

- **用途**：初始化`AnalyzeUrl`对象。
- **使用方法**：
  ```kotlin
  AnalyzeUrl(
      mUrl: String,
      key: String? = null,
      page: Int? = null,
      speakText: String? = null,
      speakSpeed: Int? = null,
      baseUrl: String = "",
      source: BaseSource? = null,
      ruleData: RuleDataInterface? = null,
      chapter: BookChapter? = null,
      readTimeout: Long? = null,
      coroutineContext: CoroutineContext = EmptyCoroutineContext,
      headerMapF: Map<String, String>? = null,
  )
  ```
- **参数说明**：
  - `mUrl`：基础 URL。
  - `key`：关键字。
  - `page`：页数。
  - `speakText`：说话文本。
  - `speakSpeed`：说话速度。
  - `baseUrl`：基础 URL。
  - `source`：书源对象。
  - `ruleData`：规则数据接口对象。
  - `chapter`：章节对象。
  - `readTimeout`：读取超时时间。
  - `coroutineContext`：协程上下文。
  - `headerMapF`：请求头映射。

## 主要方法

- **initUrl**
  - **用途**：处理 URL，包括执行 JavaScript、替换关键字和页数、解析 URL。
  - **使用方法**：内部调用，无需外部调用。
- **analyzeJs**
  - **用途**：执行 URL 中的 JavaScript 代码。
  - **使用方法**：内部调用，无需外部调用。
- **replaceKeyPageJs**
  - **用途**：替换 URL 中的关键字、页数和 JavaScript 代码。
  - **使用方法**：内部调用，无需外部调用。
- **analyzeUrl**
  - **用途**：解析 URL，包括处理查询参数、设置请求方法、请求头、请求体等。
  - **使用方法**：内部调用，无需外部调用。
- **analyzeFields**
  - **用途**：解析查询参数，生成字段映射。
  - **使用方法**：内部调用，无需外部调用。
- **evalJS**
  - **用途**：执行 JavaScript 代码。
  - **使用方法**：
    ```kotlin
    evalJS(jsStr: String, result: Any? = null): Any?
    ```
  - **参数说明**：
    - `jsStr`：JavaScript 代码。
    - `result`：执行结果的初始值。
- **put**
  - **用途**：将变量存储到章节或规则数据中。
  - **使用方法**：
    ```kotlin
    put(key: String, value: String): String
    ```
  - **参数说明**：
    - `key`：变量键。
    - `value`：变量值。
- **get**
  - **用途**：从章节或规则数据中获取变量。
  - **使用方法**：
    ```kotlin
    get(key: String): String
    ```
  - **参数说明**：
    - `key`：变量键。
- **fetchStart**
  - **用途**：开始访问，进行并发控制。
  - **使用方法**：内部调用，无需外部调用。
- **fetchEnd**
  - **用途**：访问结束，释放并发控制。
  - **使用方法**：内部调用，无需外部调用。
- **getConcurrentRecord**
  - **用途**：获取并发记录，若处于并发限制状态下则会等待。
  - **使用方法**：
    ```kotlin
    suspend fun getConcurrentRecord(): ConcurrentRecord?
    ```
- **getStrResponseAwait**
  - **用途**：访问网站，返回`StrResponse`对象。
  - **使用方法**：
    ```kotlin
    suspend fun getStrResponseAwait(
        jsStr: String? = null,
        sourceRegex: String? = null,
        useWebView: Boolean = true,
    ): StrResponse
    ```
  - **参数说明**：
    - `jsStr`：JavaScript 代码。
    - `sourceRegex`：源正则表达式。
    - `useWebView`：是否使用 WebView。
- **getStrResponse**
  - **用途**：同步版本的`getStrResponseAwait`。
  - **使用方法**：
    ```kotlin
    fun getStrResponse(
        jsStr: String? = null,
        sourceRegex: String? = null,
        useWebView: Boolean = true,
    ): StrResponse
    ```
- **getResponseAwait**
  - **用途**：访问网站，返回`Response`对象。
  - **使用方法**：
    ```kotlin
    suspend fun getResponseAwait(): Response
    ```
- **getResponse**
  - **用途**：同步版本的`getResponseAwait`。
  - **使用方法**：
    ```kotlin
    fun getResponse(): Response
    ```
- **getByteArrayAwait**
  - **用途**：访问网站，返回字节数组。
  - **使用方法**：
    ```kotlin
    suspend fun getByteArrayAwait(): ByteArray
    ```
- **getByteArray**
  - **用途**：同步版本的`getByteArrayAwait`。
  - **使用方法**：
    ```kotlin
    fun getByteArray(): ByteArray
    ```
- **getInputStreamAwait**
  - **用途**：访问网站，返回输入流。
  - **使用方法**：
    ```kotlin
    suspend fun getInputStreamAwait(): InputStream
    ```
- **getInputStream**
  - **用途**：同步版本的`getInputStreamAwait`。
  - **使用方法**：
    ```kotlin
    fun getInputStream(): InputStream
    ```
- **upload**
  - **用途**：上传文件。
  - **使用方法**：
    ```kotlin
    suspend fun upload(fileName: String, file: Any, contentType: String): StrResponse
    ```
  - **参数说明**：
    - `fileName`：文件名。
    - `file`：文件内容。
    - `contentType`：内容类型。
- **setCookie**
  - **用途**：设置 Cookie。
  - **使用方法**：内部调用，无需外部调用。
- **saveCookie**
  - **用途**：保存 Cookie。
  - **使用方法**：内部调用，无需外部调用。
- **getGlideUrl**
  - **用途**：获取处理过阅读定义的 URL 选项和 Cookie 的`GlideUrl`。
  - **使用方法**：
    ```kotlin
    fun getGlideUrl(): GlideUrl
    ```
- **getMediaItem**
  - **用途**：获取媒体项。
  - **使用方法**：
    ```kotlin
    fun getMediaItem(): MediaItem
    ```
- **getUserAgent**
  - **用途**：获取用户代理。
  - **使用方法**：
    ```kotlin
    fun getUserAgent(): String
    ```
- **isPost**
  - **用途**：判断请求方法是否为 POST。
  - **使用方法**：
    ```kotlin
    fun isPost(): Boolean
    ```

## 内部类

### UrlOption

- **用途**：表示 URL 选项。
- **主要方法**：
  - `setMethod(value: String?)`：设置请求方法。
  - `getMethod(): String?`：获取请求方法。
  - `setCharset(value: String?)`：设置字符集。
  - `getCharset(): String?`：获取字符集。
  - `setOrigin(value: String?)`：设置源 URL。
  - `getOrigin(): String?`：获取源 URL。
  - `setRetry(value: String?)`：设置重试次数。
  - `getRetry(): Int`：获取重试次数。
  - `setType(value: String?)`：设置类型。
  - `getType(): String?`：获取类型。
  - `useWebView(): Boolean`：是否使用 WebView。
  - `useWebView(boolean: Boolean)`：设置是否使用 WebView。
  - `setHeaders(value: String?)`：设置请求头。
  - `getHeaderMap(): Map<*, *>?`：获取请求头映射。
  - `setBody(value: String?)`：设置请求体。
  - `getBody(): String?`：获取请求体。
  - `setWebJs(value: String?)`：设置 WebView 中执行的 JavaScript 代码。
  - `getWebJs(): String?`：获取 WebView 中执行的 JavaScript 代码。
  - `setJs(value: String?)`：设置解析完 URL 参数时执行的 JavaScript 代码。
  - `getJs(): String?`：获取解析完 URL 参数时执行的 JavaScript 代码。
  - `setServerID(value: String?)`：设置服务器 ID。
  - `getServerID(): Long?`：获取服务器 ID。
  - `setWebViewDelayTime(value: String?)`：设置 WebView 延迟时间。
  - `getWebViewDelayTime(): Long?`：获取 WebView 延迟时间。

### ConcurrentRecord

- **用途**：表示并发记录。
- **主要方法**：
  - `ConcurrentRecord(isConcurrent: Boolean, time: Long, frequency: Int)`：构造函数，初始化并发记录。
  - `isConcurrent`：是否按频率控制并发。
  - `time`：开始访问时间。
  - `frequency`：正在访问的个数。

## 示例用法

### 创建`AnalyzeUrl`对象

```kotlin
val analyzeUrl = AnalyzeUrl(
    mUrl = "https://example.com/api/data",
    key = "searchKey",
    page = 1,
    speakText = "Hello, World!",
    speakSpeed = 100,
    baseUrl = "https://example.com",
    source = baseSource, // 假设 baseSource 已经定义
    ruleData = ruleData, // 假设 ruleData 已经定义
    chapter = bookChapter, // 假设 bookChapter 已经定义
    readTimeout = 30000L,
    coroutineContext = EmptyCoroutineContext,
    headerMapF = mapOf("User-Agent" to "MyApp/1.0")
)
```

### 执行网络请求并获取响应

```kotlin
runBlocking {
    val response = analyzeUrl.getStrResponseAwait(
        jsStr = "console.log('Hello, World!'); return 'result';",
        sourceRegex = "<data>(.*?)</data>",
        useWebView = true
    )
    println(response.body)
}
```

### 上传文件

```kotlin
runBlocking {
    val response = analyzeUrl.upload(
        fileName = "example.txt",
        file = "This is the file content.".toByteArray(),
        contentType = "text/plain"
    )
    println(response.body)
}
```

## 注意事项

- **并发控制**：`AnalyzeUrl`类内部会进行并发控制，确保在指定的并发率下不会超过最大并发数。如果并发率限制被触发，会抛出`ConcurrentException`。
- **JavaScript 执行**：`evalJS`方法可以执行 JavaScript 代码，支持在代码中使用`java`、`baseUrl`、`cookie`等变量。
- **Cookie 管理**：`setCookie`和`saveCookie`方法用于管理 Cookie，确保请求中包含正确的 Cookie 信息。
- **请求方法**：支持 GET 和 POST 请求方法，可以通过`method`参数指定。
- **请求头和请求体**：可以通过`headerMap`和`body`参数设置请求头和请求体。

