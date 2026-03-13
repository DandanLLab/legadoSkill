
## 消息摘要/散列消息鉴别码

- **digestHex**
  - **用途**：生成摘要，并转为16进制字符串。
  - **使用方法**：`digestHex(data, algorithm)`
  - **参数说明**：
    - `data`：被摘要数据。
    - `algorithm`：签名算法。

- **digestBase64Str**
  - **用途**：生成摘要，并转为Base64字符串。
  - **使用方法**：`digestBase64Str(data, algorithm)`
  - **参数说明**：
    - `data`：被摘要数据。
    - `algorithm`：签名算法。

- **HMacHex**
  - **用途**：生成散列消息鉴别码，并转为16进制字符串。
  - **使用方法**：`HMacHex(data, algorithm, key)`
  - **参数说明**：
    - `data`：被摘要数据。
    - `algorithm`：签名算法。
    - `key`：密钥。

- **HMacBase64**
  - **用途**：生成散列消息鉴别码，并转为Base64字符串。
  - **使用方法**：`HMacBase64(data, algorithm, key)`
  - **参数说明**：
    - `data`：被摘要数据。
    - `algorithm`：签名算法。
    - `key`：密钥。

## 对称加密解密

- **createSymmetricCrypto**
  - **用途**：创建对称加密解密对象。
  - **使用方法**：
    - `createSymmetricCrypto(transformation, key, iv)`：指定转换、密钥和初始化向量。
    - `createSymmetricCrypto(transformation, key)`：指定转换和密钥。
    - `createSymmetricCrypto(transformation, key)`：指定转换和密钥（字符串形式）。
    - `createSymmetricCrypto(transformation, key, iv)`：指定转换、密钥（字符串形式）和初始化向量（字符串形式）。
  - **参数说明**：
    - `transformation`：加密转换方式，如`AES/CBC/PKCS5Padding`。
    - `key`：加密密钥，可以是字节数组或字符串。
    - `iv`：初始化向量，可以是字节数组或字符串。

## 非对称加密解密

- **createAsymmetricCrypto**
  - **用途**：创建非对称加密解密对象。
  - **使用方法**：`createAsymmetricCrypto(transformation)`
  - **参数说明**：
    - `transformation`：加密转换方式。

## 签名

- **createSign**
  - **用途**：创建签名对象。
  - **使用方法**：`createSign(algorithm)`
  - **参数说明**：
    - `algorithm`：签名算法。

## MD5

- **md5Encode**
  - **用途**：进行MD5加密。
  - **使用方法**：`md5Encode(str)`
  - **参数说明**：
    - `str`：待加密的字符串。

- **md5Encode16**
  - **用途**：进行MD5加密，并取中间16位。
  - **使用方法**：`md5Encode16(str)`
  - **参数说明**：
    - `str`：待加密的字符串。

## 已废弃的对称加密解密方法

以下方法均已废弃，建议使用`createSymmetricCrypto`替代。

### AES 解码

- `aesDecodeToByteArray`
- `aesDecodeToString`
- `aesBase64DecodeToByteArray`
- `aesBase64DecodeToString`

### AES 加密

- `aesEncodeToByteArray`
- `aesEncodeToString`
- `aesEncodeToBase64ByteArray`
- `aesEncodeToBase64String`

### DES 解码

- `desDecodeToString`
- `desBase64DecodeToString`

### DES 加密

- `desEncodeToString`
- `desEncodeToBase64String`

### 3DES 解码

- `tripleDESDecodeStr`
- `tripleDESDecodeArgsBase64Str`

### 3DES 加密

- `tripleDESEncodeBase64Str`
- `tripleDESEncodeArgsBase64Str`