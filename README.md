# iOS_MDM_Guide iOS搭建MDM服务器流程
Guide to build MDM Service.

[TOC]

## 基本理念
英文好而且感兴趣的童鞋可以看下本仓库根目录的`BH_US_11_Schuetz_InsideAppleMDM_WP]`
摘抄书本主要内容：
>This paper describes how Apple’s MDM system works.
It details the method by which an MDM server initiates a connection to a managed device, how the device enrolls with the server, and the various commands available to the system. Full parameters are provided for each command, as well as details for specialized responses from the device. Finally, source code is provided for a very simple MDM server, that will permit basic experimentation with the MDM protocol using actual iOS devices.

大概翻译：
>本文主要分析MDM的工作机制，以及详细介绍以下功能的实现：
>1. MDM Server如何初始化一个和被管理设备的连接。
>2. 设备如何注册到服务器。
>3. 可用的一些指令及参数。
>4. 简单的MDM Server实现。

MDM 简历链接书中截图：
![](images/mdm_construct.png)

>1. MDM Server发送查询设备状态指令给APNs.
>2. APNs检查如果设备空闲就发送唤醒指令到设备。
>3. 设备收到唤醒指令，根据配置中的url去连接MDM Server。
>4. 连接建立之后，MDM Server和被管理设备之间即可交换指令。

## 基本条件

## 一、申请证书

### 1. 申请成为MDM Vender
没有专用于开通功能的网页，需要发送消息给`苹果开发者支持中心`。
链接地址：
[苹果开发者支持中心](https://developer.apple.com/contact/submit/)

**注意**：一定要用Team Agent权限登陆账号申请，Admin权限是会被Apple拒绝的，而且白等半天。

我的填写：
![](./images/apply_vender.png)

提交之后会受到邮件提醒，苹果会在1~2个工作日给予答复。

我等了XX。
答复如下：

完成之后可以进行下一步
### 2. 本地操作
#### i. 创建证书申请
在钥匙串点击左上角菜单

`钥匙串访问`->`证书助理`->`从证书颁发机构请求证书`

填写信息：
记住常用名称，我填的是'公司简称_MDM_个人名'，查询公私钥会用到
![](images/signing_request.png)
保存到MDM/Cer文件夹。

### ii. 导出.p12
还是在钥匙串中，点击密钥，输入`创建证书申请`中填写常用名称关键字查找，其中，专用密钥就是私钥。
![](images/find_crq_pri_key.png)
右键，导出，保存为xx_vender.p12，填写.p12使用密码[记住]
现在文件夹下面有2个文件：
> CertificateSigningRequest.certSigningRequest.
> xx_vender.p12

>注意，如果使用 mdm_vendor_sign.py 对 customer 的 csr 进行签名，则需要将私钥导出为 pem 格式（.key文件）：

``` command line
openssl pkcs12 -in xx_vender.p12 -nocerts -out xx_vender.key
```
执行过程中会让输入3次密码：
* 第一次：.p12的使用密码。
* 第二次：创建.key的使用密码。
* 第三次：确认.key的使用密码。

通过之后，文件夹下面会多出一个文件:
> xx_vender.key

### iii. 制作证书




## 参考链接
[iOS设备MDM证书申请流程 2015-07-09 悠哉-辰](https://blog.csdn.net/fobhappy/article/details/46819857)

[iOS MDM详解 2017-04-28 Light413](https://www.jianshu.com/p/6112050ea31a)














