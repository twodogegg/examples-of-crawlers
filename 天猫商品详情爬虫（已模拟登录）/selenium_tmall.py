# -*- coding: utf-8 -*-

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# 抓取单个商品
# 参考 https://segmentfault.com/a/1190000018494083
# 以后计划 写商品搜索的爬虫，将搜索结果爬取下来
class tmall:

    def __init__(self, driver_path, weibo_username, weibo_password):
        self.login_url = 'https://login.taobao.com/member/login.jhtml'
        self.weibo_username = weibo_username
        self.weibo_password = weibo_password
        self.headless = False  # 是否无页面抓取

        options = webdriver.ChromeOptions()

        # 无页面抓取
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=driver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

        self.login()

    def login(self):
        # 打开网页
        self.browser.get(self.login_url)

        # 翻墙后不可以，可能是到了国际版导致css不对了，以后研究
        # 等待 密码登录选项 出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(self.weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(self.weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))

        # 淘宝昵称
        if (taobao_name.text):
            print(taobao_name.text)
            print('登录成功')
        else:
            self.browser.quit()
            raise Exception('登录失败')

    def crawl_goods(self, goods_url):
        # 打开网页
        self.browser.get(goods_url)


        # 商品标题
        goods_title = self.browser.find_element_by_css_selector('.tb-detail-hd > h1')
        print("商品标题:" + goods_title.text)

        # 轮播图，缩略图
        goods_thumbs = self.browser.find_elements_by_css_selector('#J_UlThumb > li')
        imgs = []
        for goods_thumb in goods_thumbs:
            img_url = goods_thumb.find_element_by_css_selector('a > img').get_attribute('src').replace('_60x60q90.jpg', '')
            imgs.append(img_url)

        print("轮播图：")
        print(imgs)

        main_img = imgs[0]  # 主图
        print("商品主图：" + main_img)

        goods_market_price = self.browser.find_element_by_css_selector('#J_StrPriceModBox .tm-price')  # 商品市场价
        print("商品市场价：" + main_img)
        goods_sales_price = self.browser.find_element_by_css_selector('#J_PromoPrice  .tm-price')  # 商品售价
        print("商品售价：" + main_img)

        # 无浏览器模式下需要延迟一秒
        if self.headless:
            time.sleep(1)

        # 将浏览器滚动条拖下来点防止拖动过快
        self.browser.execute_script('''
                window.scrollTo({
                top: 800,
                behavior: "smooth"
            });
        ''')

        # 延迟一点五秒，防止拖动过快，如果还是快了就两秒
        time.sleep(1.5)

        # 拖动到底部
        self.browser.execute_script('''
            window.scrollTo({
            top: 100000,
            behavior: "smooth"
        });
        ''')

        # 商品详情的 html
        goods_desc_html = self.browser.find_element_by_css_selector('#description .content').get_attribute('innerHTML')

        print("商品详情：" + goods_desc_html)

        if self.headless:
            self.browser.close()  # 关闭进程
            self.browser.quit()  # 关闭浏览器


if __name__ == "__main__":
    goods_url = "https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.735747ceHYV7Dm&id=521497533935&skuId=4391617166783&is_b=1&rn=8c688f8523770057407b6906f6cd920f"  # 需要爬取的商品链接

    spider = tmall(driver_path="chromedriver 地址", weibo_username="你的微博用户名", weibo_password="你的微博密码")
    spider.crawl_goods(goods_url=goods_url)  # 爬取单个商品
