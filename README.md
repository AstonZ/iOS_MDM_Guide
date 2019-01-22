# iOS_MDM_Guide iOS搭建MDM服务器流程
Guide to build MDM Service.

[TOC]

## 基本理念

## 基本条件

## 一、申请证书

### 1. 申请成为MDM Vender
没有专用于开通功能的网页，需要发送消息给`苹果开发者支持中心`。
链接地址：
[苹果开发者支持中心](https://developer.apple.com/contact/submit/)

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
执行会让输入3次密码：
* 第一次：.p12的使用密码。
* 第二次：创建.key的使用密码。
* 第三次：验证.key的使用密码。
* 通过之后，文件夹下面会多出一个文件:
> xx_vender.key

### iii. 制作证书




## 参考链接
[IOS设备MDM证书申请流程 2015-7-9 悠哉-辰](https://blog.csdn.net/fobhappy/article/details/46819857)















