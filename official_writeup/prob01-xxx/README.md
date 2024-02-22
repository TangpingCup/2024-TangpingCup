# [Web] X…什么？

- 命题人：ZianTT
- X...什么?：300 分

## 题目描述

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

**【网页链接：访问题目网页】**

**【终端交互：连接到题目】**

## 预期解法

TODO: 出题人题解，后面可以按需增加更多的二级标题