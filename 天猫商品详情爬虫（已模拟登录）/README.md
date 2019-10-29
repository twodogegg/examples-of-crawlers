
> 大家都知道现在爬取天猫商品详情的数据需要先登录，简直就是巨难啊，刚好在网上看到一篇教程可以用微博登录，刚好可以规避这个问题。

## 编写思路

- 使用selenium 进行爬取，淘宝对 selenium 做了检测，需要跳过检测。
- 由于在商品详情页登录实在太难，就改成用淘宝登录然后再到商品详情页
- 商品详情页的 商品详情 如果直接抓取会抓取不到需要模拟浏览器下滑一段路程

1.过检测
```python
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
```

2.模拟下滑

```python
self.browser.execute_script('''
    window.scrollTo({
    top: 800,
    behavior: "smooth"
    });
''')
```

## 使用教程

1. [点击这里下载](https://www.google.com/chrome/)下载chrome浏览器
2. 查看chrome浏览器的版本号，[点击这里下载](http://chromedriver.storage.googleapis.com/index.html)对应版本号的chromedriver驱动
3. pip安装下列包

[x] pip install selenium
4. [点击这里](https://account.weibo.com/set/bindsns/bindtaobao)登录微博，并通过微博绑定淘宝账号密码
5. 在main中填写chromedriver的绝对路径
6. 在main中填写需要抓取的商品链接
7. 在main中填写微博账号密码

