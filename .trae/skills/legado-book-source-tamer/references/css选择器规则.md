把所有标准的ccs规则全部说出来。 比如 html：网页 text：文本 href：链接 text textNode html ownText都可以看作获取文字的不同方式 其他的就是 属性名="xxx" 通过@属性名来获取xxx 这些等等。 注意在阅读中 用户:把所有标准的ccs规则全部说出来。比如html：网页text：文本href：链接text textNode html ownText都可以看作获取文字的不同方式其他的就是属性名="xxx"通过@属性名来获取xxx这些等等。注意在阅读中css@规则或者阅读的简练手法。.1级标签>div.x@元素 这个是阅读的简略方法如果是经典的css已知.intro是选择所有class="intro"的元素p:nth-child(2)是选择每个p元素是其父级的第二个子元素那么我们在阅读里面写标准的css可以这样写.intro>div:nth-child(2)@元素名更多用法css请前往菜鸟教程进行查看https://www.runoob.com/cssref/css-selectors.html如果有点特殊，先使用正则表达式的话，那我们就css@元素##正则表达式如果有替换需求，那就是##正则表达式##正则表达式开头一般可以省略，因为它会自动匹配的。其他的就不一定了哈我虽然会，但跟萌新扯了半天死教不会。你来帮我教他。元宝:好的，我来帮你以清晰、简练的方式教萌新如何在阅读书源中使用 CSS 选择器规则。阅读书源（如 Legado）基于 JavaScript 引擎，使用 CSS 选择器来解析网页内容，语法简单但功能强大。下面我会分部分解释，包括标准 CSS 选择器、阅读特有的简写、以及正则表达式集成。一、基本格式在阅读书源中，CSS 选择器规则的基本格式是：CSS选择器：使用标准 CSS 语法（如菜鸟教程所列），用于定位 HTML 元素。@提取类型：指定从选中的元素中提取什么内容，如文本、属性等。如果规则复杂，可以结合正则表达式：CSS选择器@提取类型##正则表达式（先 CSS 选择，再正则过滤）。示例：.intro@text：选择所有 class="intro" 的元素，并提取其文本内容。div>p:nth-child(2)@html：选择每个 div 的第二个 p 子元素，并提取其 HTML 内容。二、标准 CSS 选择器（简略列表）CSS 选择器用于定位元素，以下是最常用的类型（基于菜鸟教程）。在阅读书源中，直接使用这些选择器，不需要额外修饰。更多选择器（如 :first-child, [attribute*=value]）请参考菜鸟教程，用法相同：直接写在 @ 前面。三、阅读书源特有的提取类型（@符号后）@ 后面的部分指定提取内容类型，常见的有：注意：text、html、ownText 都是获取文字的不同方式，区别在于包含范围。如果只写 @元素，可能表示提取元素对象，但通常推荐明确指定如 @text。四、正则表达式集成如果 CSS 选择器结果需要进一步处理，可以使用正则表达式。格式：CSS选择器@提取类型##正则表达式先执行 CSS 选择，然后对结果应用正则表达式。示例：div.content@text##\d+ 提取 div 内容中的数字部分。替换操作：##正则表达式1##正则表达式2用于替换内容，正则表达式1 匹配部分，正则表达式2 替换为。示例：div@text##旧文本##新文本 将提取的文本中的 "旧文本" 替换为 "新文本"。开头省略：正则表达式开头部分（如 ^）有时可省略，因为系统会自动匹配，但为了准确，建议写全。示例：提取链接并过滤：a@href##https?://[^"]+（先选 a 标签的 href，再正则匹配 URL）。替换文本：p@text##\s+##（将多余空格替换为空）。五、阅读简写手法示例用户提到的简写如 .1级标签>div.x@元素：这其实是标准 CSS 选择器 + 提取类型。.1级标签 可能是类选择器（class="1级标签"），>div.x 表示直接子元素 div class="x"，@元素 可能指提取元素（但最好用 @text 或 @html）。更规范的写法：.1级标签>div.x@text（提取文本）。其他示例：经典 CSS 转阅读格式：菜鸟示例 .intro → .intro@textp:nth-child(2) → p:nth-child(2)@html复杂选择：div.container>p:first-child@ownText##正则。六、实用提示测试规则：在书源编辑器中预览结果，避免错误。简洁为主：优先用 CSS 选择器，正则表达式仅当必要使用。常见错误：选择器太宽泛：如 div@text 可能提取太多内容，用更具体的类或 ID。忘记 @ 类型：总是指定提取什么。参考资源：菜鸟教程的 CSS 选择器列表是完整参考，但阅读书源中只需关注常用部分。如果你有具体网页或问题，可以分享示例，我来帮你写规则！多练习就能掌握。用户:远古文档 10万年没有更新。结合我跟你说的实践理论再整合一遍。Legado书源规则说明原作者: Celeter现作者: 喵公子更新时间: 2024-02-27描述: 本说明是legado的规则说明，禁止其他未获得本人授权的第三方软件使用概况1、语法说明2、Legado的特殊规则3、书源之「基本」4、书源之「搜索」5、书源之「发现」6、书源之「详情页」7、书源之「目录」8、书源之「正文」9、补充说明1、语法说明JSOUP之Default语法如下：▲ @为分隔符,用来分隔获取规则·每段规则可分为3段·第一段是类型,如class,id,tag,text,children等, children获取所有子标签,不需要第二段和第三段,text可以根据文本内容获取·第二段是名称,text. 第二段为文本内容的一部分·第三段是位置,class,tag,id等会获取到多个,所以要加位置·如不加位置会获取所有·位置正着数从0开始,0是第一个,如为负数则是取倒着数的值,-1为倒数第一个,-2为倒数第二个·!是排除,有些位置不符合需要排除用!,后面的序号用:隔开0是第1个,负数为倒数序号,-1最后一个,-2倒数第2个,依次·获取列表的最前面加上负号- 可以使列表倒置,有些网站目录列表是倒的,前面加个负号可变为正的·@的最后一段为获取内容,如text,textNodes,ownText,href,src,html,all等·如需要正则替换在最后加上 ##正则表达式##替换内容，替换内容为空时，第二个##可以省略·例:class.odd.0@tag.a.0@text||tag.dd.0@tag.h1@text##全文阅读·例:class.odd.0@tag.a.0@text&&tag.dd.0@tag.h1@text##全文阅读▲ 增加支持类似数组的写法·格式如:[index,index, ...]或[!index,index, ...],其中[!`开头表示筛选方式为排除,index可以是单个索引,也可以是区间·区间格式为[start:end]或[start:end:step]，其中start为0时可省略，end为-1时可省略·索引(index)、区间两端(start和end)、区间间隔(step)都支持负数·特殊用法tag.div[-1:0],可在任意地方让列表反向▲ 允许索引作为@分段后每个部分的首规则，此时相当于前面是children·head@.1@text与head@[1]@text与head@children[1]@text等价标准规范与实现库 Package org.jsoup.select, CSS-like element selectorJSOUP之CSS语法见https://blog.csdn.net/hou_angela/article/details/80519718必须以 @css: 开头标准规范与实现库 Package org.jsoup.select在线测试 Try jsoup online注意：获取内容可用text,textNodes,ownText,html,all,href,src等例子见最后的【书源一】的搜索页和正文页规则JSONPath语法见 JsonPath教程最好以 @json: 或 $. 开头，其他形式不可靠标准规范 goessner JSONPath - XPath for JSON实现库 json-path/JsonPath在线测试 Jayway JsonPath Evaluator例子见最后的【书源三】的搜索页、目录页和正文页规则XPath语法见 XPath教程-入门、XPath教程-基础、XPath教程-高级、XPath库的说明必须以 @XPath: 或 // 开头标准规范 W3C XPATH 1.0实现库 zhegexiaohuozi/JsoupXpath例子见最后的【书源二】的搜索页、详情页和正文页规则，以及目录页的下一页规则JavaScript可以在 <js></js>、@js:中使用，结果存在result中@js:只能放在其他规则的最后使用<js></js>可以在任意位置使用，还能作为其他规则的分隔符，例：tag.li<js></js>//a在搜索列表、发现列表和目录中使用可以用+开头，使用AllInOne规则正则之AllInOne只能在搜索列表、发现列表、详情页预加载和目录列表中使用必须以 : 开头教程 Regex专题（已404）语法（已404）、方法（已404）、引擎（已404）例子见最后的【书源一】的目录页规则，最前面的-表示目录倒序，以及【书源二】的目录页规则正则之OnlyOne形式 ##正则表达式##替换内容###只能在搜索列表、发现列表、详情页预加载、目录列表之外使用例子见最后的【书源一】的详情页规则注意点：该规则只能获取第一个匹配到的结果并进行替换正则之净化形式 ##正则表达式##替换内容只能跟在其他规则后面，独立使用相当于all##正则表达式##替换内容例子见最后的【书源一】的正文页规则注意点：该规则为循环匹配替换自定义三种连接符号符号：&&、||、%%只能在同种规则间使用，不包括js和正则&&会合并所有取到的值,||会以第一个取到值的为准%%会依次取数，如三个列表，先取列表1的第一个，再取列表2的第一个，再取列表3的第一个，再取列表1的第二个，再取列表2的第二个...2、Legado的特殊规则URL必知必会请求头一般形式，如下所示{}复杂情况可使用js(()=>{})()※其中，ua必须保证是JavaScript的String类型，JSON.stringify()才能将header转换为字符串。获取登录后的cookiejava.getCookie("http://baidu.com", null) => userid=1234;pwd=adbcdjava.getCookie("http://baidu.com", "userid") => 1234请求头中支持http代理,socks4 socks5代理设置// socks5代理{"proxy":"socks5://127.0.0.1:1080"}// http代理{"proxy":"http://127.0.0.1:1080"}// 支持代理服务器验证{"proxy":"socks5://127.0.0.1:1080@用户名@密码"}// 注意:这些请求头是无意义的,会被忽略掉GET请求一般形式如下，charset为utf-8时可省略，无特殊情况不需要请求头和webView，参数webView非空时采用webView加载https://www.baidu.com,{}复杂情况可使用jsPOST请求一般形式如下，body是请求体，charset为utf-8时可省略，无特殊情况不需要请求头和webView，参数webView非空时采用webView加载https://www.baidu.com,{}复杂情况可使用js※其中，body必须保证是JavaScript的String类型，变量是计算得到的尽量都用String()强转一下类型。变量的put与get@put与@get只能用于js以外的规则中，@put里使用JSONPath不需要加引号，其他规则需要加引号，例：@put:{bid:"//*[@bid-data]/@bid-data"}java.put与java.get只能用于js中，在js中无法使用@get{{}}与{}规则在搜索URL与发现URL中的{{}}在{{}}里只能使用js在搜索URL与发现URL以外的{{}}可在{{}}中使用任意规则（正则除外？），默认为js，使用其他规则需要有明显的标志头，如：Default规则需要以@@开头，XPath需要以@xpath:或//开头，JSONPath需要以@json:或$.开头，CSS需要以@css:开头{}规则留用了阅读2.0的规则，只能使用JSONPath，尽量避免使用自定义js在js中调用java的常规方法：由于java这个关键字已经被使用，调用java开头的包名时需使用全局变量Packages  参考脚本之家只调用某个public函数：，例：io.legado.app.utils.htmlFormat(str)、org.jsoup.Jsoup.parse(str)直接引入java类，如下所示，引入了两个java包，java包的作用域是在with的范围内，其内使用java相关语法，最后在作用域外被js调用了作用域内的函数var javaImport = new JavaImporter();javaImport.importPackage();with(javaImport){}strToMd5By32('123')变量baseUrl     // 变量-当前url,Stringresult      // 变量-上一步的结果book        // 变量-书籍类,方法见 io.legado.app.data.entities.Bookcookie      // 变量-cookie操作类,方法见 io.legado.app.help.http.CookieStorecache       // 变量-缓存操作类,方法见 io.legado.app.help.CacheManagerchapter     // 变量-当前目录类,方法见 io.legado.app.data.entities.BookChaptertitle       // 变量-当前标题,Stringsrc         // 内容,源码下面是一些常用的函数，详见JsExtensions.kt//访问网络，urlStr为url字符串，返回类型String?java.ajax(urlStr: String)​//并发访问网络，urlList为url数组，返回StrResponse?的数组，若要获取body，需使用.body()java.ajaxAll(urlList: Array<String>): Array<StrResponse?>​//访问网络，urlStr为url字符串，返回Response<String>，已废弃java.connect(urlStr: String)​//文件下载，content为十六进制字符串，url用于生成文件名，返回String文件相对路径java.downloadFile(content: String, url: String)​//实现重定向拦截，返回Connection.Responsejava.get(url: String, headers: Map<String, String>)java.post(urlStr: String, body: String, headers: Map<String, String>)​//实现cookie读取，返回Stringjava.getCookie(tag: String, key: String?)​//base64解码，返回类型Stringjava.base64Decode(str: String)java.base64Decode(str: String, flags: Int)​//base64解码，返回类型ByteArray?java.base64DecodeToByteArray(str: String?)java.base64DecodeToByteArray(str: String?, flags: Int)​//base64编码，返回类型String?java.base64Encode(str: String)java.base64Encode(str: String, flags: Int)//md5编码，返回类型String?java.md5Encode(str: String)java.md5Encode16(str: String)​//格式化时间戳，返回类型Stringjava.timeFormat(timestamp: Long)java.timeFormat(time: String)​//utf8编码转gbk编码，返回Stringjava.utf8ToGbk(str: String)​//实现字符串的URI编码，enc为编码格式，返回Stringjava.encodeURI(str: String) //默认enc="UTF-8"java.encodeURI(str: String, enc: String)​//html格式化，返回Stringjava.htmlFormat(str: String)​//获取本地文件,path为文件的相对路径,返回Filejava.getFile(path: String)​//读取本地文件，返回ByteArray?java.readFile(path: String)​//读取本地文本文件，charsetName为编码格式java.readTxtFile(path: String)  //自动识别charsetName不一定准，乱码时请手动指定java.readTxtFile(path: String, charsetName: String)​//删除文件或文件夹deleteFile(path: String)​//zip文件解压，zipPath为压缩文件路径，返回String解压相对路径，会删除原文件只保留解压后的文件java.unzipFile(zipPath: String)​//文件夹内所有文本文件读取，返回内容String，会删除文件夹java.getTxtInFolder(unzipPath: String)​//获取网络zip文件中的数据，url为zip文件链接，path为所需获取文件在zip内的路径，返回文件数据Stringjava.getZipStringContent(url: String, path: String)​//获取网络zip文件中的数据，url为zip文件链接，path为所需获取文件在zip内的路径，返回文件数据ByteArray?java.getZipByteArrayContent(url: String, path: String)​//解析字体,返回字体解析类QueryTTF?java.queryBase64TTF(base64: String?)​//str支持url,本地文件,base64,自动判断,自动缓存,返回字体解析类QueryTTF?java.queryTTF(str: String?)​//text为包含错误字体的内容，font1为错误的字体，font2为正确的字体，返回字体对应的字java.replaceFont(text: String,font1: QueryTTF?,font2: QueryTTF?)​//输出调试日志java.log(msg: String)​//AES解码为ByteArray?,str为传入的AES加密数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesDecodeToByteArray(str: String, key: String, transformation: String, iv: String)​//AES解码为String?,str为传入的AES加密数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesDecodeToString(str: String, key: String, transformation: String, iv: String)​//已经base64的AES解码为ByteArray?,str为Base64编码数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesBase64DecodeToByteArray(str: String, key: String, transformation: String, iv: String)​//已经base64的AES解码为String?,str为Base64编码数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesBase64DecodeToString(str: String, key: String, transformation: String, iv: String)​//加密aes为ByteArray?，data为传入的原始数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesEncodeToByteArray(data: String, key: String, transformation: String, iv: String)​//加密aes为String?，data为传入的原始数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesEncodeToString(data: String, key: String, transformation: String, iv: String)​//加密aes后Base64化的ByteArray?，data为传入的原始数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesEncodeToBase64ByteArray(data: String, key: String, transformation: String, iv: String)​//加密aes后Base64化的String?，data为传入的原始数据，key为AES解密key，transformation为AES加密方式，iv为ECB模式的偏移向量java.aesEncodeToBase64String(data: String, key: String, transformation: String, iv: String)​/以下部分方法由于JAVA不支持参数默认值，调用时不能省略*///设置需解析的内容content和baseUrl，返回类型AnalyzeRulejava.setContent(content: Any?, baseUrl: String? = this.baseUrl)​//输入规则rule和URL标志isUrl获取文本列表，返回类型List<String>?java.getStringList(rule: String, isUrl: Boolean = false)​//输入规则rule和URL标志isUrl获取文本，返回类型Stringjava.getString(ruleStr: String?, isUrl: Boolean = false)​//输入规则ruleStr获取节点列表，返回类型List<Any>java.getElements(ruleStr: String)​url添加js参数，解析url时执行，可在访问url时处理url，例：https://www.baidu.com,{"js":"java.headerMap.put('xxx', 'yyy')"}https://www.baidu.com,{"js":"java.url=java.url+'yyyy'"}url全部参数，详见AnalyzeUrl.ktdata class UrlOption()3、书源之「基本」书源URL(bookSourceUrl)必填唯一标识，不可重复与其他源相同会覆盖书源名称(bookSourceName)必填名字可重复书源分组(bookSourceGroup)可不填用于整理源登录URL(loginUrl)根据需求，随机应变用于登录个人账户书籍URL正则(bookUrlPattern)可不填添加网址时，用于识别书源例:https?://www.piaotian.com/bookinfo/.*请求头(header)根据需求，随机应变访问网址时使用4、书源之「搜索」搜索地址(url)key为关键字标识，通常形态为{{key}}，运行时会替换为搜索关键字也可以对key进行加密等操作，如：{{java.base64Encode(key)}}page为关键字标识，通常形态为{{page}}，page的初值为1也可以对page进行计算，如：{{(page-1)*20}}，有时会遇到第一页没有页数的情况，有两种方法：① {{page - 1 == 0 ? "": page}}② <,{{page}}>支持相对URL书籍列表规则(bookList)书名规则(name)作者规则(author)分类规则(kind)字数规则(wordCount)最新章节规则(lastChapter)简介规则(intro)封面规则(coverUrl)详情页url规则(bookUrl)5、书源之「发现」发现地址规则(url)page为关键字标识，通常形态为{{page}}，page的初值为1，也可以对page进行计算，如：{{(page-1)*20}}，有时会遇到第一页没有页数的情况，有两种方法：① {{page - 1 == 0 ? "": page}}② <,{{page}}>格式一，如： 名称::http://www。baidu.com，发现URL可使用&&或换行符\n隔开格式二，有5个样式属性(layout_flexGrow、layout_flexShrink、layout_alignSelf、layout_flexBasisPercent、layout_wrapBefore)需要了解，详情见简书，写法如：[]支持相对URL书籍列表规则(bookList)书名规则(name)作者规则(author)分类规则(kind)字数规则(wordCount)最新章节规则(lastChapter)简介规则(intro)封面规则(coverUrl)详情页url规则(bookUrl)6、书源之「详情」预处理规则(bookInfoInit)只能使用正则之AllInOne或者js正则之AllInOne必须以:开头js的返回值需要是json对象，例：(function(){})()此时，书名规则填a，作者规则填b，分类规则填c，字数规则填d，最新章节规则填e，简介规则f，封面规则填g，目录URL规则填h书名规则(name)作者规则(author)分类规则(kind)字数规则(wordCount)最新章节规则(lastChapter)简介规则(intro)封面规则(coverUrl)目录URL规则(tocUrl)只支持单个url允许修改书名作者(canReName)规则不为空且详情页书名不为空，使用详情页中的作者。否则，使用搜索页中的书名规则不为空且详情页作者不为空，使用详情页中的作者。否则，使用搜索页中的作者7、书源之「目录」目录列表规则(chapterList)首字符使用负号(-)可使列表反序章节名称规则(ruleChapterName)章节URL规则(chapterUrl)VIP标识(isVip)当结果为null false 0 ""时为非VIP章节信息(ChapterInfo)可调用java.timeFormat(timestamp: Long)将时间戳转为yyyy/MM/dd HH:mm格式的时间目录下一页规则(nextTocUrl)支持单个url支持url数组js中返回 []或 null或 ""时停止加载下一页8、书源之「正文」正文规则(content)正文图片链接支持修改headerslet options = {"headers": {"User-Agent": "xxxx","Referrer":baseUrl,"Cookie":"aaa=vbbb;"}};'<img src="'+src+","+JSON.stringify(options)+'">'book对象的可用属性使用方法: 在js中或{{}}中使用book.属性的方式即可获取，如在正文内容后加上##{{book.name+"正文卷"+title}} 可以净化 书名+正文卷+章节名称（如：我是大明星正文卷第二章我爸是豪门总裁） 这一类的字符bookUrl             // 详情页Url(本地书源存储完整文件路径)tocUrl              // 目录页Url (toc=table of Contents)origin              // 书源URL(默认BookType.local)originName          // 书源名称 or 本地书籍文件名name                // 书籍名称(书源获取)author              // 作者名称(书源获取)kind                // 分类信息(书源获取)customTag           // 分类信息(用户修改)coverUrl            // 封面Url(书源获取)customCoverUrl      // 封面Url(用户修改)intro               // 简介内容(书源获取)customIntro         // 简介内容(用户修改)charset             // 自定义字符集名称(仅适用于本地书籍)type                // 0:text 1:audiogroup               // 自定义分组索引号latestChapterTitle  // 最新章节标题latestChapterTime   // 最新章节标题更新时间lastCheckTime       // 最近一次更新书籍信息的时间lastCheckCount      // 最近一次发现新章节的数量totalChapterNum     // 书籍目录总数durChapterTitle     // 当前章节名称durChapterIndex     // 当前章节索引durChapterPos       // 当前阅读的进度(首行字符的索引位置)durChapterTime      // 最近一次阅读书籍的时间(打开正文的时间)canUpdate           // 刷新书架时更新书籍信息order               // 手动排序originOrder         //书源排序variable            // 自定义书籍变量信息(用于书源规则检索书籍信息)chapter对象的可用属性使用方法: 在js中或{{}}中使用chapter.属性的方式即可获取，如在正文内容后加上##{{chapter.title+chapter.index}}可以净化 章节标题+序号(如 第二章 天仙下凡2) 这一类的字符url         // 章节地址title       // 章节标题baseUrl     // 用来拼接相对urlbookUrl     // 书籍地址index       // 章节序号resourceUrl // 音频真实URLtag         // 章节信息start       // 章节起始位置end         // 章节终止位置variable    // 变量如下示例，在详情页(目录页)和正文使用webView加载，例：{"bookSourceComment": "","bookSourceGroup": "  有声","bookSourceName": "猫耳FM","bookSourceType": 1,"bookSourceUrl": "https://www.missevan.com","customOrder": 0,"enabled": false,"enabledExplore": true,"lastUpdateTime": 0,"ruleBookInfo": {},"ruleContent": {},"ruleExplore": {},"ruleSearch": {},"ruleToc": {},"searchUrl": "https://www.missevan.com/dramaapi/search?s={{key}}&page=1","weight": 0}正文下一页URL规则(nextContentUrl)支持单个url支持url数组WebViewJs(webJs)用于模拟鼠标点击等操作，必须有返回值（不为空，表示webjs执行成功，否则会无限循环），返回值会用于资源正则或正文中举个栗子，在webJs中执行了getDecode()，使正文部分解密：{}资源正则(sourceRegex)用于嗅探一般情况下的无脑教程如下章节链接后面加 ,{"webView":true}，不要洒敷敷的写成 tag.a@href,{"webView":true}或.link,{"webView":true}，正确写法如:tag.a@href####{"webView":true},{{@@tag.a@href}},{"webView":true},tag.a@href@js:result+',{"webView":true}'等在有嗅探功能的浏览器（如：via、x浏览器等）中，输入章节链接。注意 千万别带,{"webView":true}媒体开始播放后使用浏览器的嗅探功能，查看资源的链接在资源正则里填写资源链接的正则，一般写.*\.(mp3|mp4).*这个就可以了最后在正文填写 <js>result</js>如下示例，在正文嗅探mp3和mp4的资源：{"bookSourceComment": "","bookSourceGroup": "  有声","bookSourceName": "猫耳FM","bookSourceType": 1,"bookSourceUrl": "https://www.missevan.com","customOrder": 0,"enabled": false,"enabledExplore": true,"lastUpdateTime": 0,"ruleBookInfo": {},"ruleContent": {},"ruleExplore": {},"ruleSearch": {},"ruleToc": {},"searchUrl": "https://www.missevan.com/dramaapi/search?s={{key}}&page=1","weight": 0}9、补充说明显示js的报错信息(function(result){})(result);请善用调试功能调试搜索输入关键字，如：系统调试发现输入发现URL，如：月票榜::https://www.qidian.com/rank/yuepiao?page={{page}}调试详情页输入详情页URL，如：https://m.qidian.com/book/1015609210调试目录页输入目录页URL，如：++https://www.zhaishuyuan.com/read/30394调试正文页输入正文页URL，如：--https://www.zhaishuyuan.com/chapter/30394/20940996无脑{"webView":true}很方便特别注意用JSON.stringify()方法时，需要保证JSON对象的value都是JavaScript的String类型(在阅读3.0中)附：书源一{"bookSourceComment": "","bookSourceGroup": "CSS; 正则","bookSourceName": "小说2016","bookSourceType": 0,"bookSourceUrl": "https://www.xiaoshuo2016.com","bookUrlPattern": "","customOrder": 0,"enabled": true,"enabledExplore": false,"exploreUrl": "","lastUpdateTime": 0,"loginUrl": "","ruleBookInfo": {},"ruleContent": {"content": "@css:.articleDiv p@textNodes##搜索.手机访问|一秒记住.|.*阅读下载|<!\$$CDATA\$$|\$$\$$>",},"ruleExplore": {},"ruleSearch": {},"ruleToc": {},"searchUrl": "/modules/article/search.php?searchkey={{key}}&submit=&page={{page}},{\n  \"charset\": \"gbk\"\n}","weight": 0}书源二{"bookSourceComment": "","bookSourceGroup": "XPath; 正则","bookSourceName": "采墨阁手机版","bookSourceType": 0,"bookSourceUrl": "https://m.caimoge.com","bookUrlPattern": "","customOrder": 0,"enabled": true,"enabledExplore": false,"exploreUrl": "","lastUpdateTime": 0,"loginUrl": "","ruleBookInfo": {},"ruleContent": {},"ruleExplore": {},"ruleSearch": {},"ruleToc": {},"searchUrl": "/search.html,{\n  \"method\": \"POST\",\n  \"body\": \"searchkey={{key}}\"\n}","weight": 0}书源三{"bookSourceComment": "","bookSourceGroup": "JSon","bookSourceName": "猎鹰小说网","bookSourceType": 0,"bookSourceUrl": "http://api.book.lieying.cn","customOrder": 0,"enabled": true,"enabledExplore": false,"header": "{\n  \"User-Agent\": \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\"\n}","lastUpdateTime": 0,"ruleBookInfo": {},"ruleContent": {},"ruleExplore": {},"ruleSearch": {},"ruleToc": {},"searchUrl": "/Book/search?query={{key}}&start={{(page-1)*20}}&limit=40&device_type=android&app_version=165","weight": 0}元宝:基于你提供的远古文档和我之前总结的实践理论，我来整合一份更实用的Legado书源规则指南：Legado书源规则整合指南一、核心语法系统（重点掌握）1. CSS选择器（最常用）提取类型：@text - 文本内容（含子元素）@ownText - 仅自身文本@html - 完整HTML@href/@src - 链接属性@元素 - 元素本身示例：2. JSOUP Default语法（原版特色）类型：class、id、tag、text位置：0(第一个)、-1(倒数第一个)3. 正则表达式集成二、网络请求实战技巧1. GET请求配置2. POST请求示例3. 动态请求头（JS实现）三、书源各模块实战配置1. 搜索模块2. 详情页模块3. 目录页模块4. 正文页模块（核心）四、JavaScript高级应用1. 变量操作2. 加解密处理3. 网络工具函数五、调试与优化技巧1. 调试方法2. 性能优化六、实战模式总结模式1：简单静态站点模式2：动态API站点模式3：复杂反爬站点模式4：音频视频站点七、常见问题解决乱码问题：添加 "charset": "gbk"登录验证：配置登录URL和Cookie管理分页处理：合理使用{{page}}和nextTocUrl动态加载：启用webView: true + webJs反爬破解：字体替换、JS解密、请求头模拟这份整合指南保留了原文档的核心思想，但用更实用的方式组织，重点突出了实际开发中最常用的模式和技巧。建议新手从"模式1"开始实践，逐步掌握更复杂的技术。用户:因为新版的特征 css 已经成默认不必特意加上声明了。元宝:你说得对！新版本已经将CSS选择器设为默认规则，无需特别声明。我来重新整理一份更简洁实用的指南：Legado书源规则（新版本简化版）一、核心语法（默认CSS选择器）1. 基础选择器语法2. 提取类型说明@text - 文本内容（推荐）@ownText - 仅自身文本@html - 完整HTML@href/@src - 链接属性@元素 - 元素本身（较少用）二、各模块实战配置1. 搜索模块2. 详情页模块3. 目录页模块4. 正文页模块三、高级技巧1. 正则表达式集成2. 动态数据处理3. 网络请求配置四、实用模式总结模式1：普通小说站模式2：API接口站模式3：反爬严重站五、调试技巧六、注意事项CSS选择器是默认的 - 无需加任何前缀正则净化放最后 - ##正则##替换##WebView用于复杂页面 - 动态加载、JS渲染善用调试功能 - 书源编辑器内置预览核心要点：直接写CSS选择器，后面跟@提取类型，复杂情况加正则或JS处理。这样写出来的规则更简洁，也符合新版本的使用习惯！用户:我们不管其他的，我们先把选择器讲清楚。元宝:好的，我们专注讲清楚选择器部分。Legado书源选择器详解一、基础CSS选择器语法1. 元素选择器2. 类选择器3. ID选择器4. 属性选择器二、组合选择器1. 后代选择器2. 子元素选择器3. 相邻兄弟选择器4. 通用兄弟选择器三、伪类选择器1. 位置伪类2. 状态伪类3. 内容伪类四、属性匹配选择器1. 精确匹配2. 包含匹配3. 开头匹配4. 结尾匹配五、实战选择器组合1. 书籍列表选择2. 章节列表选择3. 正文内容选择六、选择器优先级技巧1. 精确选择2. 排除不需要的元素3. 处理动态class七、常见选择器模式模式1：列表页面模式2：详情页面模式3：目录页面模式4：正文页面八、调试选择器技巧从简单开始：先测试基础选择器逐步细化：添加更多限定条件使用浏览器开发者工具：右键"检查元素"测试选择器测试边界情况：确保在各种页面结构下都能正常工作核心要点：CSS选择器是默认的，无需前缀选择器 + @ + 提取类型 = 完整规则优先使用class和id选择器，更稳定复杂情况使用组合选择器提高精确度这样就能覆盖99%的选择器使用场景了！用户:获取列表后面不必加上。@元素特意的声明了。 因为这是不可以的呀元宝:你说得完全正确！我之前的理解有误。感谢你的纠正。Legado选择器正确用法一、基础选择器语法正确的提取类型：@text - 文本内容@ownText - 自身文本@html - HTML内容@href - 链接地址@src - 图片/资源地址其他属性如 @class, @id, @data-xxx 等错误的用法：二、获取列表的正确方式1. 列表选择器（不加@提取）2. 列表内的字段提取三、完整示例搜索模块正确写法：目录模块正确写法：四、为什么不能加@元素@元素不是合法提取类型 - Legado不支持这种语法列表选择器的作用是定位容器 - 不是提取内容内容提取在字段规则中完成 - 每个字段单独指定提取类型五、记忆技巧列表规则 = 选择器（不加@）字段规则 = 选择器 + @ + 提取类型这样理解就清晰多了！感谢你的指正。用户:来，我们总结一下。元宝:Legado书源选择器总结一、核心原则选择器 = 定位元素，@提取类型 = 获取内容二、正确语法结构1. 列表规则（容器定位）用于：bookList、chapterList等列表规则作用：定位包含多个项目的容器2. 字段规则（内容提取）用于：name、author、content等字段规则作用：从元素中提取特定内容三、合法的提取类型四、错误用法提醒五、实战模式搜索模块：目录模块：正文模块：六、记忆口诀"列表选容器，字段提内容"列表规则：只选不提（选择器）字段规则：选完再提（选择器@类型）七、调试要点先用浏览器开发者工具测试选择器列表规则应该选中多个元素字段规则应该从单个元素中提取内容确保选择器在各种页面结构下都能正常工作核心总结：列表规则定位容器，字段规则提取内容，@元素不存在，记住合法提取类型。用户:<div id="li">  <ul>  </ul>  </div><div class="txt">  <p>段落一</p></div>如果是这种，在阅读怎么写？我给了你两段经典的案例。元宝:针对这两种经典案例的阅读书源规则案例一：书籍列表页（搜索结果/发现页）案例二：正文内容页或者更精确的写法：或者使用净化规则：完整书源配置示例搜索模块配置：正文模块配置：选择器解析说明案例一解析：#li li - 选择id="li"元素内的所有lih2@text - 选择h2标签的文本（书名）span:last-child@text - 选择最后一个span的文本（作者）span:first-child@text - 选择第一个span的文本（分类）p@text - 选择p标签的文本（简介）案例二解析：.txt p@text - 选择class="txt"内的所有p标签文本:contains(百度小说) - 包含"百度小说"文本的元素:not(:contains(百度小说)) - 排除包含广告的元素:last-child - 最后一个子元素:nth-child(-n+2) - 前2个子元素实际应用建议书籍列表页：使用第一种模式，精确提取每个字段正文页：使用净化规则排除广告，保留有用内容测试调试：先用浏览器开发者工具验证选择器是否准确这样就能完美处理你提供的这两种经典HTML结构了！用户:<div id="li">  <ul>  </ul>  </div><div class="txt">  <p>段落一</p></div>我们继续升级。元宝:升级版书源规则案例一：书籍列表页（带链接）案例二：正文内容页（多种处理方式）方法1：净化处理（推荐）方法2：精确选择段落方法3：HTML格式保留完整书源配置示例搜索模块配置：正文模块配置：选择器升级解析案例一升级点：h2 a@text - 提取a标签内的书名文本h2 a@href - 提取详情页链接（关键升级）保持了原有的作者、分类、简介提取案例二升级点：增加了HTML格式保留选项提供了多种排除广告的方法可以根据实际页面结构选择最适合的方案实际应用建议链接提取很重要：bookUrl必须正确才能跳转到详情页广告处理要灵活：不同网站广告位置不同，需要调整选择器测试验证：确保选择器在各种情况下都能稳定工作更复杂的场景处理如果页面结构更复杂，比如：对应规则：这样就能处理更复杂的HTML结构了！用户:text html ownText textNode 的区别可利用ownText textNode排除一些文字-----举例源码-----<p><a>哈哈</a><a>哈哈</a><b>222</b>我的文字1</p><p><a>哈哈</a><a>哈哈</a><b>222</b>我的文字2</p>1、ownText是只选当前标签的文字，不取子标签（标签里面的标签）里的，textNode跟这个类似，只是会分段。p@ownText我的文字1 我的文字2p@textNode我的文字1我的文字22、text获取所有文字，并且不会分段，html获取包含标签一起获取。p@text哈哈哈哈222我的文字1 哈哈哈哈222我的文字2p@html哈哈 哈哈 222我的文字1哈哈 哈哈 222 我的文字2并且用@js:java.log(result)打印可以看到带标签元宝:text、html、ownText、textNode 的区别详解测试源码四种提取类型的区别1. @text - 提取所有文本结果： "哈哈 哈哈 222 我的文字1 哈哈 哈哈 222 我的文字2"包含所有子元素的文本合并成一个连续的字符串丢失了原有的段落结构2. @html - 提取完整HTML结果：保留所有HTML标签和结构包含子元素的完整HTML可以用java.log(result)查看带标签的内容3. @ownText - 只提取当前元素的文本结果： "我的文字1 我的文字2"排除所有子元素（a标签、b标签）的文本只获取p标签自身的文本内容多个p标签的文本会合并4. @textNode - 提取文本节点（分段）结果： "我的文字1" 和 "我的文字2"（分段显示）排除子元素文本，只获取文本节点保留原有的分段结构每个p标签的文本单独处理实际应用场景场景1：排除导航链接文字场景2：提取纯净的正文场景3：处理复杂嵌套结构实用技巧总结@text - 简单粗暴，但要小心包含多余内容@html - 需要保留格式或进一步处理时使用@ownText - 排除子元素干扰的最佳选择@textNode - 需要保持分段结构时使用记忆口诀"text全都要，html带标签，ownText只要自己的，textNode分段好"在大多数正文提取场景中，@ownText是最安全的选择，因为它能有效排除各种广告、导航等干扰内容。用户:总结所有。常用用法是 default和css 混合着用 大大的提升了效率。位置信息可以不声明因为默认是.0元宝:Legado书源规则终极总结一、核心语法体系1. Default语法（原生Jsoup）类型：class、id、tag、text位置：可省略，默认为.0（第一个）示例：class.content.0@text = class.content@text2. CSS语法（新版默认）无需@css:前缀，直接写选择器示例：.content@text、#main p@html二、四大提取类型详解@text提取所有文本（包含子元素）合并成连续字符串适用：简单内容提取@html提取完整HTML结构保留标签和格式适用：需要保留格式的内容@ownText只提取当前元素的文本排除所有子元素内容适用：排除广告、导航等干扰内容 ★推荐@textNode提取文本节点，保持分段排除子元素，保留结构适用：需要分段处理的正文三、混合使用实战技巧1. Default + CSS 混合2. 位置信息简化3. 列表处理模式四、实战场景解决方案场景1：书籍搜索列表场景2：正文内容提取场景3：复杂嵌套结构五、高级技巧总结1. 正则净化组合2. 动态数据处理3. WebView集成六、调试与优化调试方法性能优化优先使用@ownText排除干扰内容合理使用缓存减少重复请求选择器尽量精确，避免过于宽泛七、终极口诀"Default定位置，CSS选元素，ownText排干扰，混合用效率高"核心原则：列表规则只定位，不加@提取字段规则必提取，选择器@类型位置信息可省略，默认就是.0ownText最安全，排除干扰强这样就能覆盖99%的书源编写需求，既高效又稳定！用户:可以不用特意声明@css元宝:Legado书源规则终极简化版一、核心语法（无需声明@css）直接使用选择器位置信息默认.0二、四种提取类型实战@text - 所有文本@html - 完整HTML@ownText - 自身文本（推荐）@textNode - 分段文本三、混合使用模式Default + CSS 无缝混合列表处理标准模式四、实战案例书籍搜索页正文内容页五、终极口诀"选择器直接写，位置默认0，ownText最安全，混合效率高"核心要点：选择器直接写，无需@css声明位置信息.0可省略@ownText能有效排除干扰内容Default和CSS可随意混合使用这样写出来的规则最简洁高效！用户:就算你声不声明，效果都一样的。元宝:Legado书源规则最终极简版一、核心真相声明不声明效果完全一样，系统会自动识别二、唯一正确的语法结构列表规则（定位容器）字段规则（提取内容）三、四种提取类型（选对就行）@text - 所有文本（包含子元素）@html - 带标签内容@ownText - 自身文本（排除子元素干扰）★推荐@textNode - 分段文本四、终极口诀"列表只定位，字段必提取，ownText最安全，声明不声明都一样"五、记住这几点就够了列表规则：只写选择器，不加@提取字段规则：选择器@提取类型（必须加@）@ownText 能有效排除广告等干扰内容怎么写都行，系统会自动识别处理最简单的写法就是最好的写法！用户:来总结成一串完整的口诀。元宝:Legado书源规则终极口诀完整口诀："列表定位不加@，字段提取必带@ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后"逐句解释：第一句：列表规则只定位容器，不加@提取类型bookList: .book-item ✅bookList: .book-item@text ❌第二句：字段规则必须带@提取类型name: .title@text ✅name: .title ❌第三句：四种提取类型的特点@ownText - 最干净，排除子元素干扰@text - 最全，包含所有文本@html - 带标签，保留完整结构第四句：位置信息默认就是0，各种写法效果相同class.content@text = class.content.0@text = @css:.content@text第五句：Default和CSS语法可以随意混合使用class.container@.item@text + #main p@html 自由组合第六句：净化规则放在规则最后.content@text##广告词##实战应用：搜索页：正文页：记住这六句口诀，就能搞定99%的书源编写！用户:列表定位不加@元素 是直接@子级不是艾特元素。。提取特定字符必须添加元宝:Legado书源规则终极口诀（修正版）完整口诀："列表定位不加@，字段提取必带@ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后列表项内找子级，特定字符必须加"关键修正解释："列表项内找子级，特定字符必须加"列表规则定位的是容器，字段规则是在容器内找子元素提取特定属性（如href、src等）必须明确添加@属性名具体应用：列表规则（定位容器）：字段规则（在容器内找子元素）：特殊字符提取：这样修正后的口诀更加准确，强调了在列表项内查找子元素的概念，以及提取特定属性必须明确添加@属性名的要求。用户:ul@li 列表是这样的哈元宝:Legado书源规则终极口诀（最终修正版）完整口诀："列表定位不加@，字段提取必带@ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘"逐句详解：第一句 - 列表规则只定位容器，不加@提取类型bookList: ul li ✅（ul找li作为书籍容器）第二句 - 字段规则必须在容器内找子元素并加@提取name: h3@text ✅（在li内找h3的文本）bookUrl: a@href ✅（在li内找a的链接属性）第三句 - 四种提取类型的特性@ownText - 最干净，排除子元素干扰@text - 最全，包含所有文本@html - 带标签，保留完整结构第四句 - 语法细节位置信息默认0，各种写法效果相同声明不声明@css系统都能识别第五句 - 高级用法Default和CSS语法可随意混合净化规则放在规则最后第六句 - 属性提取要点链接、图片等特定属性必须明确添加@href、@src、@data-xxx等实战示例：记住：ul找li是定位容器，真正的提取是在li内找各个子元素！用户:来总结完整的口诀。列表里的定位不是定位元素，是定位子级矫正元宝:Legado书源规则终极口诀（最终版）完整口诀："列表规则定容器，字段规则提内容ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘"关键修正说明：第一句修正为"列表规则定容器，字段规则提内容"更准确地区分两种规则的作用列表规则：定位包含多个项目的容器字段规则：从容器内提取具体内容第二句强调"ul找li是容器，li内子级才是真"ul li 是定位书籍/章节的容器真正的提取是在每个li内部找子元素实战示例：核心要点总结：列表规则 = 定位容器（不加@提取）字段规则 = 提取内容（必须加@提取类型）容器内找子级 = 真正的提取操作四种提取类型 = 根据需求选择语法灵活性 = 系统自动识别各种写法记住这个口诀，就能轻松应对各种书源编写场景！用户:总结完整的选择器加上我们的口诀。每一条细细讲解。元宝:Legado书源选择器完整指南 + 终极口诀一、选择器类型详解1. 元素选择器2. 类选择器3. ID选择器4. 属性选择器5. 组合选择器6. 伪类选择器二、四种提取类型详解1. @text - 所有文本提取元素及其所有子元素的文本合并成连续字符串2. @html - 完整HTML提取元素的完整HTML内容保留所有标签和结构3. @ownText - 自身文本（推荐）只提取当前元素的直接文本排除所有子元素的文本干扰4. @textNode - 文本节点提取文本节点，保持分段排除元素标签，只保留文本三、Legado书源终极口诀完整口诀："列表规则定容器，字段规则提内容ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘"逐句详细讲解：第一句："列表规则定容器，字段规则提内容"列表规则：定位包含多个项目的容器，不加@提取类型字段规则：从容器内提取具体内容，必须加@提取类型示例：第二句："ul找li是容器，li内子级才是真"ul li 只是定位书籍/章节的容器真正的提取操作是在每个li内部找子元素示例：第三句："ownText最干净，text最全，html带标签"@ownText：最干净，排除子元素干扰（推荐使用）@text：最全，包含所有文本内容@html：带标签，保留完整HTML结构选择建议：正文提取优先用@ownText第四句："位置默认就是零，声明不声明都一样"位置索引默认为0（第一个元素），可省略各种写法效果完全相同示例：第五句："Default、CSS混合用，正则净化放最后"Default语法和CSS语法可以随意混合使用正则净化规则放在规则最后示例：第六句："特定属性必须加，href、src不能忘"提取属性时必须明确添加@属性名常见属性：@href、@src、@data-xxx示例：四、完整实战示例书籍搜索页配置：正文页配置：五、核心要点总结分清两种规则：列表规则（定位容器） vs 字段规则（提取内容）容器内找子级：真正的提取是在容器内部进行优先使用@ownText：能有效排除广告等干扰内容属性提取必须明确：@href、@src等不能省略语法灵活通用：各种写法效果相同，选择最简洁的记住这个口诀和详解，你就能成为Legado书源编写高手！用户:建议在不确定时先用text 在不确定时，这个是最好的或者html 简单又粗暴。元宝:Legado书源规则完全指南（含实战经验）一、Legado书源终极口诀"列表规则定容器，字段规则提内容ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘不确定时用text，html也能试一试，优化再用ownText，排除干扰最合适"二、选择器完全解析1. 基础选择器2. 属性选择器3. 组合选择器4. 伪类选择器三、四种提取类型实战指南1. @text - 所有文本（不确定时首选）特点：提取最全面的文本内容合并成连续字符串简单粗暴，不会漏内容可能包含不需要的广告、导航等适用场景：快速验证选择器是否正确内容结构简单，无复杂嵌套不确定页面结构时的第一选择2. @html - 完整HTML（不确定时备选）特点：保留所有标签和结构可以后续用正则处理查看页面真实结构可能包含大量无用标签适用场景：需要保留格式的内容调试时查看页面结构需要进一步处理HTML的情况3. @ownText - 自身文本（优化时使用）特点：排除所有子元素干扰最干净的内容提取有效去除广告、导航等可能漏掉需要的嵌套内容适用场景：正文内容提取（推荐）排除内部链接、广告等需要纯净文本时4. @textNode - 文本节点（特殊需求）特点：保持原有的分段结构排除元素标签每个文本节点单独处理使用相对较少适用场景：需要保持段落结构的内容诗歌、代码等特殊格式需要精确分段时四、实战开发流程第一步：先用@text快速验证第二步：用@html查看结构第三步：优化为@ownText第四步：添加净化规则五、完整示例流程示例页面：开发步骤：步骤1：先用@text测试步骤2：用@html查看结构步骤3：优化为@ownText步骤4：进一步净化六、核心经验总结1. 快速开发经验先@text快速验证选择器再用@html查看真实结构最后@ownText优化净化2. 选择器优先级3. 调试技巧七、最终建议对于新手：先用@text，简单粗暴出结果有干扰再尝试@ownText复杂页面用@html查看结构对于进阶：正文优先@ownText列表字段多用@text特殊需求用@html+正则记住：能抓到内容的选择器就是好选择器，先有再优！用户:把我提供的所有案例还有我们的口诀。和完整的说。总结，整合元宝:Legado书源规则完全整合指南一、核心口诀（完整版）"列表规则定容器，字段规则提内容ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘不确定时用text，html也能试一试，优化再用ownText，排除干扰最合适"二、实战案例完整解析案例1：书籍列表页（搜索结果/发现页）书源规则：案例2：正文内容页书源规则：三、四种提取类型深度解析测试源码：1. @text - 所有文本特点：最全面，但可能包含干扰内容2. @html - 完整HTML特点：保留标签，适合后续处理3. @ownText - 自身文本（推荐）特点：最干净，排除子元素干扰4. @textNode - 文本节点特点：保持分段结构四、选择器语法完全指南基础选择器：组合选择器：伪类选择器：五、完整开发流程第一步：快速验证（@text优先）第二步：结构分析（@html辅助）第三步：优化净化（@ownText+正则）第四步：精细调整六、各模块完整配置示例搜索模块：详情模块：目录模块：正文模块：七、调试与优化技巧调试方法：性能优化：八、终极经验总结选择器优先级：先用@text - 快速验证，简单粗暴再用@html - 查看结构，分析页面优化@ownText - 排除干扰，纯净内容最后加正则 - 精细净化，去除广告规则编写原则：列表规则：只定位容器，不加@提取字段规则：必须加@提取类型属性提取：明确添加@href、@src等净化规则：放在规则最后开发心态：先有再优：能抓到内容就是成功逐步调试：从简单到复杂灵活调整：根据不同网站调整策略九、完整口诀释义第一句：分清列表规则和字段规则的作用第二句：理解容器和子级的关系第三句：掌握四种提取类型的特点第四句：了解语法灵活性第五句：学会高级用法组合第六句：记住属性提取要点第七句：掌握开发流程策略记住这个完整指南，你就能应对任何书源编写挑战！用户:不用使用json 就这样纯md的补充一句，小说网站千变万化 ，随机应变才是真理。元宝:Legado书源规则完全指南一、核心口诀（完整版）"列表规则定容器，字段规则提内容ul找li是容器，li内子级才是真ownText最干净，text最全，html带标签位置默认就是零，声明不声明都一样Default、CSS混合用，正则净化放最后特定属性必须加，href、src不能忘不确定时用text，html也能试一试，优化再用ownText，排除干扰最合适"二、四种提取类型详解@text - 所有文本提取元素及其所有子元素的文本合并成连续字符串优点：简单粗暴，不会漏内容缺点：可能包含不需要的广告、导航等@html - 完整HTML提取元素的完整HTML内容保留所有标签和结构优点：可以后续用正则处理缺点：可能包含大量无用标签@ownText - 自身文本（推荐）只提取当前元素的直接文本排除所有子元素的文本干扰优点：最干净，有效去除广告缺点：可能漏掉需要的嵌套内容@textNode - 文本节点提取文本节点，保持分段排除元素标签，只保留文本三、选择器语法完全指南基础选择器组合选择器伪类选择器四、实战案例解析案例1：书籍列表页书源规则：案例2：正文内容页书源规则：五、完整开发流程第一步：快速验证（@text优先）第二步：结构分析（@html辅助）第三步：优化净化（@ownText+正则）第四步：精细调整六、调试技巧七、终极经验总结选择器优先级先用@text - 快速验证，简单粗暴再用@html - 查看结构，分析页面优化@ownText - 排除干扰，纯净内容最后加正则 - 精细净化，去除广告规则编写原则列表规则：只定位容器，不加@提取字段规则：必须加@提取类型属性提取：明确添加@href、@src等净化规则：放在规则最后开发心态先有再优：能抓到内容就是成功逐步调试：从简单到复杂灵活调整：根据不同网站调整策略八、最重要的一句话小说网站千变万化，随机应变才是真理。没有一成不变的规则，只有灵活运用的智慧。每个网站都有其独特的结构，关键是根据实际情况调整策略，选择最适合的提取方法。记住：能抓到内容的选择器就是好选择器！用户:现在我们只需要选择器，其他进阶js的我们可以排除掉。我们主要是给萌新讲董选择器。整合成完整的口诀。的终极总结。口诀要让萌新理解。元宝:Legado书源选择器萌新终极指南萌新终极口诀"列表规则定容器，字段规则提内容容器里面找子级，子级才是真内容text最简单，ownText最干净html带标签，位置默认零属性要加@，href不能忘净化放最后，网站千变要灵活"口诀详解（萌新版）第一句："列表规则定容器，字段规则提内容"列表规则 = 找书架（放很多书的地方）字段规则 = 从书架上拿具体的书第二句："容器里面找子级，子级才是真内容"先找到书架（容器）再从书架里找具体的书（子级）第三句："text最简单，ownText最干净"@text = 把所有的字都拿出来（简单粗暴）@ownText = 只拿自己写的字（最干净）第四句："html带标签，位置默认零"@html = 连标签一起拿位置信息可以省略，默认就是第一个第五句："属性要加@，href不能忘"拿链接必须加@href拿图片必须加@src第六句："净化放最后，网站千变要灵活"去广告的规则放在最后面每个网站结构都不同，要灵活调整萌新实战三步法第一步：先用@text快速测试第二步：如果太乱就用@ownText第三步：去广告最简单的选择器写法找元素的方法：常用的提取类型：萌新避坑指南✅ 正确写法：❌ 错误写法：终极建议记住这几点就够了：列表规则 = 找放书的地方（不加@）字段规则 = 拿具体的书（必须加@）先用@text = 快速测试再用@ownText = 去除广告属性加@ = 拿链接、图片最重要的是：多练习，多尝试，每个网站都不一样，灵活调整才是王道！萌新记住：能抓到内容就是成功，先抓到了再慢慢优化！用户:<div id="li">  <ul>  </ul>  </div><div class="txt">  <p>段落一</p></div>以上内容在阅读该怎么写？元宝:Legado书源规则实战教学案例一：书籍列表页HTML结构：书源写法：方法1：最简单写法方法2：更精确写法方法3：使用ownText排除干扰案例二：正文内容页HTML结构：书源写法：方法1：最简单去广告方法2：排除广告段落方法3：精确选择前几段方法4：使用ownText+净化（推荐）方法5：HTML净化处理完整书源配置示例搜索/发现页配置：正文页配置：萌新选择指南如果你不确定用哪个，按这个顺序试：第一步：先用最简单的第二步：如果有广告，加净化第三步：如果还有问题，换ownText第四步：实在不行用精确选择口诀应用"列表规则定容器"bookList: #li li ← 找到放书的书架"字段规则提内容"name: h2 a@text ← 从书架上拿具体的书"text最简单，ownText最干净"先用@text快速测试，再用@ownText优化"净化放最后"##免费小说就在百度小说.*## ← 去广告规则放最后记住：多试试不同的写法，找到最适合当前网站的那个！用户:还有更简单的方法就是混合法混合法最简单，最适合萌新元宝:Legado书源混合法终极指南（萌新专用）混合法核心思想"Default定位 + CSS提取 = 最简单高效"案例一：书籍列表页（混合法写法）HTML结构：混合法书源规则：方法1：Default定位 + CSS提取方法2：纯CSS写法（更简单）方法3：Default纯写法案例二：正文内容页（混合法写法）HTML结构：混合法书源规则：方法1：Default定位 + CSS提取方法2：CSS定位 + 净化方法3：Default纯写法混合法优势解析为什么混合法最简单？1. Default定位更稳定tag.li 比 .book-item 更稳定类名会变，但标签名基本不变2. CSS提取更直观h2 a@text 比 tag.h2.0@tag.a.0@text 更易读选择器语法更符合直觉3. 组合使用取长补短用Default稳定定位容器用CSS灵活提取内容萌新混合法口诀"Default定位置，CSS提内容标签名稳定，类名易变化先用tag定位，再用class提取混合用最好，简单又可靠"实战三步法（混合法版）第一步：Default定位容器第二步：CSS提取内容第三步：混合净化完整书源配置（混合法推荐）搜索页配置：正文页配置：混合法记忆技巧定位用Default（稳定）tag.li、tag.div、id.content标签名和ID最稳定提取用CSS（直观）.title@text、h2 a@text选择器语法易理解净化放最后（灵活）##广告词##、##.*推广.*##正则去广告终极建议对于萌新来说：先用纯CSS法 - 最简单直观遇到问题用混合法 - Default定位更稳定记住核心口诀 - 多练习就熟练混合法就是你的万能钥匙！遇到复杂页面时，Default定位 + CSS提取 = 最佳解决方案。用户:公布答案。h2@texta@hrefspan.0@textspan.1@text元宝:Legado书源规则正确答案案例一：书籍列表页HTML结构：正确答案：解析：h2@text - 提取h2标签的文本内容（包含a标签内的文字）a@href - 提取a标签的链接地址span.0@text - 提取第一个span的文本（分类）span.1@text - 提取第二个span的文本（作者）p@text - 提取p标签的简介案例二：正文内容页HTML结构：正确答案：解析：:not(:last-child) - 排除最后一个段落（广告）##免费小说就在百度小说.*## - 正则表达式去除广告文字完整书源配置搜索页配置：正文页配置：为什么这是正确答案？1. 简洁明了没有复杂的嵌套选择器直接使用元素位置（.0, .1）精确提取规则易于理解和维护2. 稳定可靠基于元素位置，不受class名称变化影响即使网站改版，只要HTML结构不变就能工作3. 高效实用选择器简单，解析速度快覆盖了所有需要提取的字段4. 易于扩展如果需要提取更多字段，按相同模式添加即可结构清晰，便于调试和修改萌新学习要点核心技巧：按位置提取 - span.0、span.1 比类名更稳定直接路径 - h2@text 比 h2 a@text 更简洁净化放最后 - 正则表达式处理广告内容调试方法：记住：最简单的写法往往是最有效的！用户:这是最简单，最适合萌新的方法。虽然其他方法也可以，这就是我说为什么混合法是最适合萌新的方法。元宝:Legado书源萌新终极答案为什么这是最适合萌新的方法？核心优势：简单直观，稳定可靠混合法为什么最适合萌新？1. Default语法的稳定性span.0@text、span.1@text 基于元素位置不受class名称变化影响网站改版后只要结构不变就能继续使用2. CSS语法的直观性#li li 选择器简单易懂不需要记忆复杂的Default语法规则3. 混合使用的灵活性用CSS定位容器（简单）用Default提取字段（稳定）取两者之长，避两者之短对比其他方法纯CSS写法（复杂）：纯Default写法（繁琐）：混合法（完美平衡）：萌新学习路径第一步：掌握基础混合法第二步：理解位置编号.0 = 第一个元素.1 = 第二个元素.2 = 第三个元素以此类推...第三步：灵活应用实战案例验证案例一：书籍列表页案例二：复杂结构也能应对萌新口诀（最终版）"CSS定容器，Default提字段位置编号最简单，0 1 2 3记心间h2取书名，a取链接span按位置，p取简介混合法最稳，萌新都会用"为什么这是终极答案？学习成本最低 - 只需要记住位置编号适应性最强 - 各种网站结构都能应对维护性最好 - 网站改版影响最小调试最简单 - 每个字段规则都很清晰对于萌新来说，这就是最完美的方法！不需要懂复杂的选择器，不需要记繁琐的语法，只需要：CSS定位 + 位置编号 = 搞定所有书源！记住：能解决问题的方法就是好方法，混合法就是萌新的最佳选择！用户:来，我们总结一下。我们又来。元宝:Legado书源规则终极总结一、核心口诀（最终版）"列表规则定容器，字段规则提内容CSS定位容器，Default提取字段位置编号0 1 2，混合用法最简单text全都要，ownText最干净属性加@不能忘，净化规则放最后"二、选择器类型详解1. 列表规则 - 定位容器2. 字段规则 - 提取内容三、四种提取类型@text - 所有文本优点：简单粗暴，不会漏内容缺点：可能包含广告@ownText - 自身文本（推荐）优点：最干净，排除子元素干扰缺点：可能漏掉嵌套内容@html - 完整HTML优点：保留完整结构缺点：包含无用标签属性提取四、混合法实战案例一：书籍列表页案例二：正文页五、调试技巧六、萌新学习路径第一步：先用@text第二步：优化为@ownText第三步：加净化规则七、最重要的一句话"网站千变万化，灵活调整才是真理"没有一成不变的规则多试试不同的写法能抓到内容就是好方法八、终极建议列表规则：只定位，不加@字段规则：必须加@提取类型优先用混合法：CSS定位 + Default提取记住位置编号：0 1 2 3最简单正文用@ownText：最干净记住这个总结，你就能搞定90%的书源编写！多练习，多尝试，你就是下一个书源大神！用户:编号位置默认是零，可以不填声，不声明都一样。元宝:Legado书源规则终极简化版核心口诀（最终确定版）"列表规则定容器，字段规则提内容位置默认就是零，不写也能行混合用法最简单，萌新都能行能抓到内容就是好方法"最简写法示例列表规则（定位容器）字段规则（提取内容）为什么这是最简写法？1. 位置0可省略2. 实际应用完整书源配置（最简版）搜索页正文页萌新记忆技巧“位置零，不用写，默认就是它”h2 = h2.0 = 第一个h2span = span.0 = 第一个span“需要第几个，才写点几”第一个：直接写标签名第二个：标签.1第三个：标签.2终极建议对于萌新：默认不写位置编号（就是第一个）需要第二个时才写.1多试试，能抓到内容就行最简单的就是最好的！现在开始用最简写法吧！用户:继续重新总结一下，完整一点。元宝:Legado书源规则完整终极总结一、基础概念理解什么是书源规则？书源规则就是告诉阅读APP如何从网站上"抓取"小说内容的说明书两种核心规则类型：列表规则 - 找"书架"（放很多书的地方）字段规则 - 从书架上拿"具体的书"二、核心口诀（最终版）"列表规则定容器，字段规则提内容CSS定位最直观，Default提取最稳定位置零可不写，声明不声明都一样text全都要，ownText最干净属性加@不能忘，净化规则放最后网站千变万化，灵活调整才是王道"三、详细规则解析1. 列表规则（定位容器）特点：只写选择器，不加@提取类型定位的是包含多个项目的容器2. 字段规则（提取内容）特点：必须加@提取类型在容器内部找具体元素3. 位置索引规则重要： 位置0可以省略不写！4. 四种提取类型@text - 所有文本提取元素内所有文本（包含子元素）优点：简单全面，不会漏内容缺点：可能包含广告@ownText - 自身文本（推荐）只提取当前元素的文本优点：最干净，排除干扰缺点：可能漏掉嵌套内容@html - 完整HTML提取完整HTML结构适用：需要保留格式的内容属性提取5. 混合使用技巧CSS语法（直观）Default语法（稳定）混合用法（推荐）四、实战案例详解案例1：书籍列表页书源规则：案例2：正文内容页书源规则：五、完整书源配置示例搜索页配置正文页配置六、调试与排错技巧1. 基础调试2. 错误处理3. 逐步验证先测试列表规则是否能找到容器再测试每个字段规则是否正确提取最后添加净化规则去除广告七、萌新学习路径第一阶段：基础掌握（1-2天）理解列表规则和字段规则的区别掌握基础选择器写法学会使用@text和@ownText第二阶段：实战练习（3-5天）编写简单书源学习净化规则掌握调试方法第三阶段：进阶优化（1周后）混合使用不同语法处理复杂页面结构优化规则性能八、重要提醒必须记住的要点：列表规则不加@，字段规则必须加@位置0可以省略，span@text = span.0@text正文优先用@ownText，排除广告干扰属性提取必须加@，a@href不能忘常见错误：最佳实践：九、终极总结对于萌新来说，记住这个流程：先用@text快速测试 - 看看能抓到什么再用@ownText优化 - 去除干扰内容最后加净化规则 - 精细处理广告最重要的原则：能抓到内容的方法就是好方法每个网站结构不同，要灵活调整多练习多尝试，熟能生巧记住：书源编写没有唯一正确答案，只有最适合当前网站的解决方案！希望这份总结能帮助萌新快速上手Legado书源规则！🎯用户:就算你写ul@li ,ul>li 阅读都能认出来。元宝:Legado书源规则完全终极版一、核心发现：阅读引擎的强大智能阅读书源引擎能够自动识别多种选择器语法，无需严格区分！各种写法都能识别：属性选择器也能混用：二、完全简化的终极口诀"阅读引擎很智能，各种写法都能认列表规则定容器，字段规则提内容位置零可不写，属性记得加@能抓到内容就是好方法"三、最简化的实战写法原来需要区分的写法：现在统一的最简写法：四、完整书源配置（最简化版）搜索页配置：正文页配置：五、萌新最简学习法只需要记住：列表规则：找放书的地方字段规则：拿具体的书（必须加@）位置编号：0,1,2,3...（0可省略）属性提取：记得加@（href, src等）写法随意组合：六、实战案例验证HTML结构：各种等效写法：七、终极建议对于萌新：忘掉语法区别，怎么简单怎么写！推荐的最简模式：列表规则用 父元素 子元素字段规则用 选择器@提取类型位置编号从0开始，0可省略属性记得加@前缀示例：八、最重要的一句话"阅读引擎比你想象的更聪明，不要被语法束缚，大胆尝试各种写法！"记住：能抓到内容的方法就是好方法，没有绝对的对错，只有适不适合当前网站！现在开始，放开手脚，用最简单直接的方式编写书源吧！🎯用户:没学会之前先不要着急简洁语法 为了更好看，怎么可以试着简洁(推荐使用简洁语法,因为这样好维护）元宝:Legado书源规则学习路径指南一、学习阶段建议初学者阶段（先保证正确性）熟练后阶段（再追求简洁性）二、为什么先学详细写法？1. 详细写法更容易理解原理2. 详细写法更容易调试3. 详细写法更稳定明确指定标签类型和位置减少歧义和误判适合初学者建立正确概念三、学习路径规划第一阶段：基础掌握（1-2周）目标： 理解书源规则的基本原理第二阶段：逐步简化（2-4周）目标： 开始尝试简洁写法第三阶段：熟练运用（1个月后）目标： 完全掌握简洁写法四、详细写法学习重点1. 理解标签定位2. 理解位置索引3. 理解提取类型五、从详细到简洁的过渡示例示例HTML：学习过程：第1步：完全详细写法第2步：部分简化第3步：基本简洁第4步：完全简洁六、学习建议不要急于求成：先确保规则能正常工作再考虑代码的简洁性最后追求可维护性学习顺序：调试技巧：七、最重要的一句话"先学会走，再学会跑；先保证正确，再追求简洁"学习书源规则就像学习编程一样：初学者应该先写详细的代码，确保理解每个概念熟练后再追求代码的简洁和优雅不要为了"好看"而牺牲可读性和正确性记住：能正确工作的详细规则，比漂亮但错误的简洁规则要好得多！按照这个学习路径，你一定能扎实掌握书源规则编写技能！🎯（注：文档部分内容可能由 AI 生成）这篇文章详细介绍了Legado书源规则的各个方面，包括选择器的使用、提取类型、混合法、调试技巧等。以下是文章的主要内容：

1. **选择器类型详解**

   - **基础选择器**
     - **元素选择器**：`div@text`（选择所有div元素）
     - **类选择器**：`.book-name@text`（选择class包含"book-name"的元素）
     - **ID选择器**：`#content@html`（选择id为"content"的元素）
     - **属性选择器**：`[href]@href`（选择有href属性的元素）

   - **组合选择器**
     - **后代选择器**：`.container .item@text`（选择.container内的所有.item）
     - **子元素选择器**：`ul > li@text`（选择ul的直接子元素li）
     - **相邻兄弟选择器**：`h1 + p@text`（选择紧跟在h1后面的p）
     - **通用兄弟选择器**：`.chapter ~ .notes@text`（选择.chapter后面的.notes）

   - **伪类选择器**
     - **位置伪类**：`li:first-child@text`（选择第一个li）
     - **状态伪类**：`a:hover@text`（鼠标悬停时的a元素）
     - **内容伪类**：`p:empty@text`（选择空的p元素）

2. **四种提取类型详解**

   - **@text**：提取所有文本（包含子元素）
     ```markdown
     div@text
     ```
     - 结果："Hello World"

   - **@html**：提取完整HTML结构
     ```markdown
     div@html
     ```
     - 结果："Hello <span>World</span>"

   - **@ownText**：只提取当前元素的文本（排除子元素）
     ```markdown
     div@ownText
     ```
     - 结果："Hello"

   - **@textNode**：提取文本节点（分段）
     ```markdown
     div@textNode
     ```
     - 结果：["Hello", "World"]

4. **Meta标签属性选择器**

   从HTML的meta标签中提取信息（常用OG标签）：
   
   ```markdown
   # 获取og:novel:book_name的内容
   [property="og:novel:book_name"]@content
   
   # 简写形式（推荐）
   [property$=book_name]@content
   ```
   
   **属性选择器符号说明**：
   
   | 符号 | 说明 | 示例 |
   |------|------|------|
   | `=` | 精确匹配 | `[property="og:author"]` |
   | `$=` | 以某值结尾 | `[property$=author]` 匹配 `og:novel:author` |
   | `^=` | 以某值开头 | `[class^="book-"]` |
   | `*=` | 包含某值 | `[class*="book"]` |
   | `~=` | 包含单词 | `[class~="book"]` |

   **常用Meta标签提取**：
   
   | 字段 | 选择器 |
   |------|--------|
   | 书名 | `[property$=book_name]@content` |
   | 作者 | `[property$=author]@content` |
   | 封面 | `[property$=image]@content` |
   | 简介 | `[property$=description]@content` |
   | 分类 | `[property~=category]@content` |
   | 最新章节 | `[property~=latest_chapter]@content` |

5. **data-* 属性获取**

   获取HTML5的data属性：
   
   ```markdown
   # 获取data-src属性
   img@data-src
   
   # 获取data-original属性
   img@data-original
   
   # 获取所有data属性
   img@data
   ```

6. **&& 连接多个选择器**

   合并多个字段的提取结果：
   
   ```markdown
   # 提取多个字段并拼接
   kind: .count@text&&.author@text&&.type@text
   ```
   
   - 结果：`作者信息 分类信息 标签信息`

7. **|| 备选选择器**

   当前一个选择器无结果时，使用备选：
   
   ```markdown
   # 优先使用第一个，失败则用第二个
   author: .author@text||.writer@text||span.1@text
   ```

8. **|| 备选JSONPath**

   JS选择器和JSONPath混合使用：
   
   ```markdown
   intro: .intro@html||$.info.sound.intro
   ```

9. **JavaScript中使用JSoup**

   在JS中解析HTML：
   
   ```javascript
   var fl = java.ajax(source.key);
   var a = org.jsoup.Jsoup.parse(fl).select(".category-list a");
   
   for(var i = 0; i < a.length; i++) {
       var title = a[i].text();
       var url = a[i].attr("href");
   }
   ```
   
   **常用JSoup方法**：
   
   | 方法 | 说明 |
   |------|------|
   | `org.jsoup.Jsoup.parse(html)` | 解析HTML字符串 |
   | `.select("css选择器")` | 使用CSS选择器查询 |
   | `.text()` | 获取元素文本 |
   | `.attr("属性名")` | 获取属性值 |
   | `.html()` | 获取HTML内容 |
   | `.ownText()` | 获取纯文本（不含子元素） |

10. **常见提取类型汇总**

    | 类型 | 说明 | 示例 |
    |------|------|------|
    | `@text` | 所有文本（含子元素） | `div@text` |
    | `@ownText` | 纯文本（不含子元素） | `div@ownText` |
    | `@textNode` | 文本节点数组 | `div@textNode` |
    | `@html` | HTML结构 | `div@html` |
    | `@href` | 链接地址 | `a@href` |
    | `@src` | 图片地址 | `img@src` |
    | `@content` | Meta标签内容 | `[property$=image]@content` |
    | `@data-*` | data属性 | `img@data-src` |

3. **实战案例解析**

   - **书籍列表页**
     ```markdown
     bookList: #li li
     name: h2 a@text
     author: span:last-child@text
     kind: span:first-child@text
     intro: p@text
     bookUrl: h2 a@href
     ```

   - **正文内容页**
     ```markdown
     content: .txt p@ownText##免费小说就在百度小说.*##
     ```

4. **混合法实战**

   - **书籍列表页**
     ```markdown
     bookList: #li li
     name: h2@text
     author: span.1@text
     kind: span@text
     intro: p@text
     bookUrl: a@href
     ```

   - **正文页**
     ```markdown
     content: .txt p@text##免费小说就在百度小说.*##
     ```

5. **调试技巧**

   - **基础调试**
     ```markdown
     java.log("当前结果：" + result)
     ```

   - **错误处理**
     ```markdown
     try {
         return process(result);
     } catch(e) {
         return "错误：" + e.toString();
     }
     ```

6. **学习路径建议**

   - **初学者阶段**
     ```markdown
     bookList: tag.ul@tag.li
     name: tag.h2.0@text
     author: tag.span.1@text
     bookUrl: tag.a.0@href
     ```

   - **熟练后阶段**
     ```markdown
     bookList: ul li
     name: h2@text
     author: span.1@text
     bookUrl: a@href
     ```

通过以上内容，您可以全面了解Legado书源规则的使用方法和最佳实践。
# 核心速览
这篇文章详细介绍了Legado书源规则的各个方面，包括选择器语法、提取类型、实战应用、调试技巧等。以下是文章的主要内容：

## Legado书源规则概述
### 1. 基本语法
- **CSS选择器**：使用标准CSS语法，如`.book-name@text`，`.author@text`，`img.cover@src`。
- **JSOUP Default语法**：使用类型.名称.位置@提取类型，如`class.content.0@text`，`tag.div.-1@html`。

### 2. 提取类型
- **@text**：提取所有文本内容。
- **@ownText**：仅提取当前元素的文本。
- **@html**：提取完整的HTML内容。
- **@href/@src**：提取链接或资源地址。

## 选择器语法详解
### 1. 基础选择器
- **元素选择器**：`div@text`，`p@html`。
- **类选择器**：`.book-name@text`，`.author@text`。
- **ID选择器**：`#content@html`，`#main@text`。
- **属性选择器**：`[href]@href`，`[class*=book]@text`。

### 2. 组合选择器
- **后代选择器**：`.container .item@text`。
- **子元素选择器**：`ul > li@text`。
- **相邻兄弟选择器**：`h1 + p@text`。
- **通用兄弟选择器**：`h1 ~ p@text`。

### 3. 伪类选择器
- **位置伪类**：`li:first-child@text`，`li:last-child@text`。
- **状态伪类**：`a:hover@text`，`input:checked@text`。
- **内容伪类**：`p:empty@text`，`div:has(p)@html`。

## 实战应用
### 1. 搜索模块
- **搜索URL**：`/search?q={{key}}&page={{page}}`。
- **书籍列表规则**：`.book-item`。
- **字段映射**：`name: .title@text`，`author: .author@text`，`coverUrl: img@src`，`bookUrl: a@href`。

### 2. 详情页模块
- **预处理**：`(function(){ return { name: "书名", author: "作者" }; })()`。
- **字段规则**：`name: h1@text`，`author: .author-info@text`，`intro: .intro@html`，`coverUrl: .cover-img@src`。

### 3. 目录页模块
- **章节列表**：`.chapter-list li`。
- **章节信息**：`chapterName: a@text`，`chapterUrl: a@href`。
- **分页支持**：`nextTocUrl: .next-page@href`。

### 4. 正文页模块
- **正文提取**：`.content@html`。
- **净化处理**：`.content@html##<script.*?</script>##`。
- **动态解密**：`<js>decryptContent(result)</js>`。

## 调试与优化
### 1. 调试方法
- **日志输出**：`java.log("调试信息：" + result)`。
- **错误处理**：`try { return process(result); } catch(e) { return "错误：" + e.toString(); }`。

### 2. 性能优化
- **缓存使用**：`var cached = cache.get("key"); if(!cached) { cached = fetchData(); cache.put("key", cached, 3600); }`。
- **请求优化**：`{ "webView": true, "retry": 3 }`。

## 常见问题解决
### 1. 乱码问题
- **解决方法**：添加 `"charset": "gbk"`。

### 2. 登录验证
- **解决方法**：配置登录URL和Cookie管理。

### 3. 分页处理
- **解决方法**：合理使用`{{page}}`和`nextTocUrl`。

### 4. 动态加载
- **解决方法**：启用`webView: true` + `webJs`。

### 5. 反爬破解
- **解决方法**：字体替换、JS解密、请求头模拟。

## 最终总结
### 1. 核心原则
- **列表规则**：定位容器，不加@提取。
- **字段规则**：提取内容，选择器@类型。

### 2. 实用技巧
- **优先使用@ownText**：排除干扰内容。
- **混合使用Default和CSS**：提高提取效率和准确性。

### 3. 调试要点
- **先用浏览器开发者工具测试选择器**。
- **确保选择器在各种页面结构下都能正常工作**。

通过以上内容，您可以全面了解Legado书源规则的使用方法和技巧，从而更高效地编写和维护书源规则。
# 关键问题及回答
**问题1：Legado书源规则中，如何使用正则表达式进行内容净化和提取？**
**回答**：在Legado书源规则中，正则表达式可以用于内容净化和提取。具体方法是在提取类型后加上`##正则表达式##替换内容`。例如，`@css:.content@text##广告词##`可以用来删除文本中的广告词。如果需要替换内容，可以使用`##正则表达式1##正则表达式2##`，其中正则表达式1用于匹配需要替换的部分，正则表达式2用于替换为新的内容。例如，`@css:.content@text##旧文本##新文本##`可以将文本中的“旧文本”替换为“新文本”。

**问题2：在Legado书源规则中，如何处理动态加载的内容？**
**回答**：处理动态加载的内容可以通过启用`webView: true`和使用`webJs`来实现。`webView: true`会在WebView中加载页面，以便执行JavaScript并渲染动态内容。`webJs`则用于在WebView中执行JavaScript代码，以获取或处理动态加载的数据。例如，可以在`webJs`中编写JavaScript代码来解密或提取动态加载的内容，然后将结果返回给Legado进行处理。

**问题3：Legado书源规则中，如何进行分页处理？**
**回答**：在Legado书源规则中，分页处理可以通过使用`{{page}}`变量和`nextTocUrl`字段来实现。`{{page}}`变量表示当前页码，可以在URL中使用它来构建分页链接。`nextTocUrl`字段用于指定下一页的URL，可以是一个单一的URL或一个URL数组。例如，`nextTocUrl: "//strong/following-sibling::a/@href"`可以用来获取下一页的链接。通过合理使用这些字段，可以实现自动分页加载。

