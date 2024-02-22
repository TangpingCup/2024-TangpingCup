# 题目列表

| 分类 | 官方题解和源码 | 题目标题 | Flag | 分值 | 校内通过 | 总通过 |
| --- | --- | --- | --- | --- | --- | --- |
| Web | [→ prob01-xxx](../official_writeup/prob01-xxx/) | X…什么？ | X...什么? | 300 | 0+0 | 5+1 |
| Misc | [→ prob05-uncrackable](../official_writeup/prob05-uncrackable/) | Uncrackable | Uncrackable | 200 | 0+0 | 4+1 |
|  | [→ prob06-hoyomix](../official_writeup/prob06-hoyomix/) | 非常好忽悠混合 | 你咋知道? | 200 | 0+0 | 17+1 |
|  |  |  | 我没看见 | 200 | 0+0 | 13+2 |
|  | [→ prob02-mosaic](../official_writeup/prob02-mosaic/) | 心中无码，自然高清 | 心中无码，自然高清 | 400 | 0+0 | 13+2 |
|  | [→ prob07-morse](../official_writeup/prob07-morse/) | bepbep | 嘀嘀嘟嘟的码 | 50 | 0+0 | 14+1 |
|  |  |  | 眼前一黑的码 | 70 | 0+0 | 12+4 |
|  | [→ prob08-box2](../official_writeup/prob08-box2/) | 我朝，大盒 | 我朝，大盒 | 60 | 0+0 | 17+1 |
|  |  |  | 真人快打 | 100 | 0+0 | 9+1 |
|  | [→ prob09-tpask](../official_writeup/prob09-tpask/) | 躺平问答 | 一半的问题 | 60 | 0+0 | 30+1 |
|  |  |  | 所有的问题 | 100 | 0+0 | 14+0 |
| Web | [→ prob10-tpforum](../official_writeup/prob10-tpforum/) | 躺平论坛 | 看不见的flag | 60 | 0+0 | 59+1 |
|  |  |  | 找不到的flag | 100 | 0+0 | 8+0 |
| Reverse | [→  prob11-tpchat](../official_writeup/ prob11-tpchat/) | 躺平聊天室2.0 | 眼前一糊 | 80 | 0+0 | 13+2 |
|  |  |  | 眼前一黑 | 100 | 0+0 | 11+2 |
|  |  |  | 眼前一亮 | 120 | 0+0 | 8+0 |
| Crypto | [→ prob12-mygo1](../official_writeup/prob12-mygo1/) | 主唱太拼命了 | 主唱太拼命了 | 200 | 0+0 | 4+0 |
| Reverse | [→ prob13-hit](../official_writeup/prob13-hit/) | HIT! 准入认证! | 说走就走的旅行 | 100 | 0+0 | 43+3 |
|  |  |  | 太美丽了某校 | 400 | 0+0 | 5+0 |
|  | [→ third01-crackme](../official_writeup/third01-crackme/) | [投稿]CrackMe | / | 0 | 0+0 | 3+0 |

“分值” 表示题目原始分值，实际分值取决于校内第一阶段通过人数。

“校内通过” 和 “总通过” 人数的两个部分分别表示第一阶段和第二阶段的通过人数。

## [Web] X…什么？

**[【→ 官方题解和源码】](../official_writeup/prob01-xxx/)**

<p>经过十个甚至九个小时的苦熬，你终于攻破了躺平杯比赛的服务器</p>
<p>但是服务器里没有flag,所以你留下了一个上传点，想利用它 配合一些手段 得到出题人电脑上的flag....</p>
<p>当你发现出题人用的是chrome的时候，你的嘴角勾起了弧度</p>
<p>快点动手吧 flag 就在面前</p>
<div class="codehilite" style="background: #f8f8f8"><pre style="line-height: 125%;"><span></span><code>FROM python:3

# install libs

RUN apt-get update &amp;&amp; apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    unzip xvfb

# install chrome

COPY vendor/chrome-114.0.5735.90-linux64.zip /usr/src/
RUN unzip /usr/src/chrome-114.0.5735.90-linux64.zip -d /usr/src

# copy chrome driver

COPY vendor/chromedriver /usr/bin/
RUN chmod +x /usr/bin/chromedriver

# install python requirements

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

# copy src

COPY xssbot.py ./
COPY token.pub ./

CMD [&quot;python&quot;, &quot;xssbot.py&quot;]
</code></pre></div>

<div class="well"><strong>第二阶段提示</strong><br>
Chrome CVE
<div>

## [Misc] Uncrackable

**[【→ 官方题解和源码】](../official_writeup/prob05-uncrackable/)**

<h2>Uncrackable</h2>
<p>出题人把flag放在了ZIP压缩包里并添加了密码！</p>
<p>但是为什么还能得到flag呢...?</p>
<div class="well">
<strong>补充信息</strong>
<br>
什么？你问密码？random.sample(string.ascii_letters + string.digits, 12)
</div>

<div class="well"><strong>第二阶段提示</strong><br>
压缩包内一部分似乎能被找到
<div>

## [Misc] 非常好忽悠混合

**[【→ 官方题解和源码】](../official_writeup/prob06-hoyomix/)**

<p>我爱忽悠混合 --出题人1</p>
<p>我朝 原.....来你也玩.....  --出题人2</p>
<div class="well"><strong>第二阶段提示</strong><br>
一个是奇怪的名字，一个在某一帧里
<div>

## [Misc] 心中无码，自然高清

**[【→ 官方题解和源码】](../official_writeup/prob02-mosaic/)**

<h2>心中无码，自然高清</h2>
<p>马赛克挡住的 不只是知识 还有Flag</p>
<p>通常 面对马赛克  你可以用技术手段修复/还原部分</p>
<p>但是其实只要摘下你的近视眼镜 你就会发现马赛克也是高清的一种</p>
<p>但是这次马赛克下可是flag啊</p>
<p>出题人曰:心中无码，自然高清</p>
<div class="well"><strong>第二阶段提示</strong><br>
你说得对但是都试一遍会怎样
<div>

## [Misc] bepbep

**[【→ 官方题解和源码】](../official_writeup/prob07-morse/)**

<h2>神秘的声音</h2>
<h3>一段神秘的音频 包含了通往{flag}的钥匙</h3>
<h3>叭叭叭叭叭叭叭叭叭叭叭叭 嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟嘟</h3>
<div class="well"><strong>补充说明</strong><br>flag1内容应均为小写</div>

<div class="well"><strong>第二阶段提示</strong><br>
空间站是怎么传输图片的？什么？电视？什么？慢？
<div>

## [Misc] 我朝，大盒

**[【→ 官方题解和源码】](../official_writeup/prob08-box2/)**

<h2>我朝，大盒</h2>
<h4>距离上次躺平杯114.514天后，AGI趁着在出题人身处高考考场，无法使用电子产品，偷袭了出题人的手机并留下了后门</h4>
<h4>就在几天前，AGI通过这个后门截获了出题人的部分短信信息，由于上次被攻击后flag被泄露，出题人选择将flag随身携带而不是存入电子产品</h4>
<h4>根据速度和GPS推算，出题人应该是在一列列车上，但是是在哪辆列车上呢？</h4>
<h4>出题人随手拍下的窗外景色，同样成为了AGI推断出题人位置的有效助力</h4>
<h4>AGI由此火速定位了出题人所在的列车并黑入车厢监控，成功看到了出题人随身携带的flag</h4>
<h4>flag 人人爱之 AGI再次建立了网站 答出出题人所在位置送flag1，答出出题人所乘车次号送flag2</h4>
<h2>附加题：</h2>
<p>答出出题人身份证号送【数据删除】，错答出其他出题人身份证号送【数据删除】</p>
<p>在组委会不为人知的过去，有一个名为Jac***L的生死大敌，答出身份证号送【数据删除】</p>
<p>以上格式均为flag{身份证号}</p>

## [Misc] 躺平问答

**[【→ 官方题解和源码】](../official_writeup/prob09-tpask/)**

<h2>躺平问答</h2>
<h3>听说躺平杯又出新问答了</h3>
<h3>我tm flag 呢</h3>
<h3>我不到啊</h3>

## [Web] 躺平论坛

**[【→ 官方题解和源码】](../official_writeup/prob10-tpforum/)**

<h2>躺平论坛</h2>
<h3>Flag在论坛里,自己去找</h3>
<h3>大佬flag在哪为什么我找不到?</h3>
<h3>大佬flag掉了补一下?</h3>
<h3>大佬没法解压?</h3>
<h3>大佬密码是多少?</h3>
<h3>大佬这是什么，手机能做吗？</h3>

## [Reverse] 躺平聊天室2.0

**[【→ 官方题解和源码】](../official_writeup/ prob11-tpchat/)**

<h2>躺平聊天室</h2>
<h3>去年躺平杯的老熟人，但是更加令人眼前一黑(模糊)</h3>
<div class="well">
<strong>补充说明</strong><br>
该题目尚未适配darkmode<del>，部分选手做题可能确实眼前一黑了。</del>
</div>

## [Crypto] 主唱太拼命了

**[【→ 官方题解和源码】](../official_writeup/prob12-mygo1/)**

<h2>主唱太拼命了</h2>
<p>你是cryichic的主唱, 第一场live结束后被人评价"主唱太拼命了" , </p>
<p>对方想要继续发送flag时却已经被鼓手提前拉黑, </p>
<p>快尝试还原flag, 不要让cryichic就这么解散!</p>

## [Reverse] HIT! 准入认证!

**[【→ 官方题解和源码】](../official_writeup/prob13-hit/)**

<h2>HIT! 准入认证!</h2>
<p>你咋知道我跑去HIT了？  --来自出题人</p>
<p>我不到啊 我沈阳大街上等你嗷 --来自验题人</p>
<p>好 你等我登录上再说 --来自出题人</p>
<p>这套系统有两个flag，一个是flag，另一个也是flag</p>
<div class="well"><strong>第二阶段提示</strong><br>
一个是线性函数一个是奇怪的bbbbbbbb64
<div>

## [Reverse] [投稿]CrackMe

**[【→ 官方题解和源码】](../official_writeup/third01-crackme/)**

<p>投稿题目</p>