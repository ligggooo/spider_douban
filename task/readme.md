#第七模块：项目实战一·第2章爬虫实战

## 动态爬取豆瓣电影中“更多”电影详情数据

作业截止时间：
2019-02-14 23:59

## 作业需求:

### 基础需求：85%
建议：使用pycharm进行开发
1. 使用任意代理IP进行如下操作
2. 使用requests模块进行豆瓣电影的个人用户登录操作
3. 使用requests模块访问个人用户的电影排行榜->分类排行榜->任意分类对应的子页面
4. 爬取需求3对应页面的电影详情数据
5. 爬取3对应页面中滚动条向下拉动2000像素后加载出所有电影详情数据，存储到本地json文件中或者相应数据库中
【备注】电影详情数据包括：海报url、电影名称、导演、编剧、主演，类型，语言，上映日期，片长，豆瓣评分

### 编码规范需求：15%
1. 代码规范遵守pep8 (https://python.org/dev/peps/pep-0008/)
2. 函数有相应的注释
3. 程序有文档说明文件（README.md参考：https://github.com/csrftoken/vueDrfDemo）
4. 程序的说明文档必须包含的内容：程序的开发环境、程序的实现的功能、程序的启动方式、登录用户信息、程序的运行效果
5. 程序设计的流程图：
(可以参考：https://www.processon.com/view/link/589eb841e4b0999184934329)

## 程序说明
### 开发环境
pycharm + chromedriver
### 依赖
lxml
selenium
requests

## 实现的功能：
1. 豆瓣网的账户密码登陆
2. 电影排行榜下的分类列表自动获取，交由用户选择
3. 获取该分类下的电影（页面下移2000px）详情页url和海报url  
    保存在./data下的 类型_movie_lv0 文件中
4. 依次进入电影详情页，展开被折叠的字段，获取全部摘要和评分
    保存在./data下的 类型_movie_lv1 文件中
5. 每部电影的详情页会被截图，保存在./data/screen_shot

## 程序的启动方式
1. 配置 /service/settings.py
    ```
            CHROME_PATH = r'F:\luffycity\课件\第7模块课件\chromedriver_win32\chromedriver.exe'
    USER = {
        'name': '账户名',
        'password': '密码',
    }
    
    DATA_DIR = './data'
    SCREEN_SHOT_DIR = './data/screen_shot'
    ```
2. 配置入口程序 /task/douban_main.py
    ```
    if __name__ == '__main__':
        session = login()
        movie_type_url,movie_type = get_type()
        get_movies(movie_list_url=movie_type_url, file_out='movies_lv0', movie_type=movie_type)
        get_movie_info(file_in='movies_lv0', file_out='movies_lv1', movie_type=movie_type)
    ```
## 登录用户信息

## 程序的运行效果
1. 用户选择分类
   
    ```
        25 武侠
        26 古装
        27 运动
        28 黑色电影
        请输入序号:22
    ```
2. 详情页url和海报url
   
    ```
    完成 https://movie.douban.com/subject/1418019/ https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2266298961.jpg
    完成 https://movie.douban.com/subject/1292213/ https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2455050536.jpg
    完成 https://movie.douban.com/subject/1291560/ https://img1.doubanio.com/view/photo/s_ratio_poster/public/p537668599.jpg
    ```
3. 详情页抓取+解析
    ```
    福尔摩斯二世 Sherlock Jr. (1924) 已经完成1/共40部
    {'title': '福尔摩斯二世 Sherlock Jr. (1924)', 'detail': ['导演: 巴斯特·基顿', '编剧: 克莱德·布鲁克曼 / 让·C·阿韦', '主演: 巴斯特·基顿 / 凯瑟琳·麦奎尔 / 乔·基顿', '类型: 喜剧 / 奇幻', '制片国家/地区: 美国', '语言: 无对白', '上映日期: 1924-04-21', '片长: 45 分钟', '又名: 小私家侦探', 'IMDb链接: tt0015324'], 'rating': '9.4'}
    千与千寻 千と千尋の神隠し (2001) 已经完成2/共40部
    {'title': '千与千寻 千と千尋の神隠し (2001)', 'detail': ['导演: 宫崎骏', '编剧: 宫崎骏', '主演: 柊瑠美 / 入野自由 / 夏木真理 / 菅原文太 / 中村彰男 / 玉井夕海 / 神木隆之介 / 内藤刚志 / 泽口靖子 / 我修院达也 / 大泉洋 / 小林郁夫 / 上条恒彦 / 小野武彦', '类型: 剧情 / 动画 / 奇幻', '制片国家/地区: 日本', '语言: 日语', '上映日期: 2001-07-20(日本)', '片长: 125分钟', '又名: 神隐少女(台) / Spirited Away / A Voyage of Chihiro / Sen to Chihiro no kamikakushi', 'IMDb链接: tt0245429'], 'rating': '9.3'}
    大闹天宫 (1961) 已经完成3/共40部
    {'title': '大闹天宫 (1961)', 'detail': ['导演: 万籁鸣 / 唐澄', '编剧: 李克弱 / 万籁鸣', '主演: 邱岳峰 / 富润生 / 毕克 / 尚华 / 于鼎 / 李梓 / 刘广宁', '类型: 动画 / 奇幻', '制片国家/地区: 中国大陆', '语言: 汉语普通话', '上映日期: 1961(中国大陆) / 1964(中国大陆) / 1978(中国大陆) / 2004(中国大陆)', '片长: 114分钟', '又名: 大闹天宫 上下集 / The Monkey King / Havoc in Heaven / Uproar in Heaven', 'IMDb链接: tt0059855'], 'rating': '9.3'}
    大话西游之大圣娶亲 西遊記大結局之仙履奇緣 (1995) 已经完成4/共40部
    ```