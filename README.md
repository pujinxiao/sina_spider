# 相关代码已经修改调试成功----2017-4-13 #

## 一、说明 ##
1.目标网址：[新浪微博](http://weibo.com/)

2.实现：跟踪比较活跃的微博号所发的微博内容，隔3-5分钟刷新（爬取）一次，只有更新了才爬的到，不爬取历史微博内容哦，**爬取正文、文中图片、所属微博昵称、发布时间（时间戳格式)**。

3.数据：数据都存在mysql数据库中。

4.**补充**：

![](http://i.imgur.com/Y8gllcS.png)

> 1.表**cookies_list**是存放你登录微博的cookies，我这里选择cookie登录。在遇到cookie被禁止就换cookie，微博帐号可以在某宝买到，你懂得。
> 
> 2.表**headers_list**是存放User-Agent，随机调用浏览器的头。
> 
> 3.表**weibo-id-list**是存放你要跟踪的微博帐号的url，如：[新浪电影微博](http://weibo.com/film?profile_ftype=1&is_all=1#_0)
> 
> 4.表**weibo_logging**是记录所有爬取的信息，不管有没有用，可以当做日志来看，其实在爬取的过程中有很多无效的信息，都需要过滤的。
> 
> 5.表**weibo_result**是最终的有效结果。

## 二、运行 ##
> 1. 首先配置好数据库，mysql。除了表weibo_result不用创建以外，其他都要额外创建好。例如：我存放在百度网盘里面，可自行看相关字段-------链接：[http://pan.baidu.com/s/1nuSx8vB](http://pan.baidu.com/s/1nuSx8vB) 密码：krqp
> 2. 备注处更改表明可以随便更改名称。很多说明程序也都有，点击运行即可。
## 三、问题----欢迎留言提出问题 ##
声明：本项目原先是想监控某些微博帐号所发内容，但是本人能力有限，所写并不是很好，就当是练手了。在这里推荐一个开源的关于新浪微博的爬虫的[项目](https://github.com/pujinxiao/SinaSpider)，我也是写完才发现这个的，但是实现的功能和我不一样，里面东西比较多，也比较复杂，可以学习学习。

> 1.这次就不写问题了，当练手了。有学习python爬虫的欢迎一起学习，我的博客：[https://www.cnblogs.com/jinxiao-pu/](https://www.cnblogs.com/jinxiao-pu/)欢迎参观。

**欢迎有兴趣的小伙伴帮我优化，解决以上问题，之后我将合并你的代码，作为贡献者,共同成长。**

## 四、附加 ##
我在另外的python_service.py文件中，我把次程序写进了windows服务里面，只要电脑一开机，设置一下就会自动启动爬取。具体的都在参考资料里面。

参考资料：

[http://blog.csdn.net/zhou191954/article/details/8290010](http://blog.csdn.net/zhou191954/article/details/8290010)

[http://www.tuicool.com/articles/Qjei2e](http://www.tuicool.com/articles/Qjei2e)

----------
如果本项目对你有用请给我一颗star，万分感谢。

