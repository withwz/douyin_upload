## 抖音并发批量自动化上传视频
参考了 https://github.com/Superheroff/douyin_uplod 这个项目，去除了视频生成拼接等的代码。

代码简单，方便和其他爬虫项目对接。

## 如何使用

```shell
git clone https://github.com/withwz/douyin_upload.git

pip install -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple/

# 安装无头浏览器
playwright install chromium

# 获取登录抖音凭证
python get_cookie.py

python main.py
```

在main.py中配置video_data_list，path写video目录下的视频文件名称，运行python main.py 可并发执行自动化上传

```python
    video_data_list = [
        {
            "title": "可可爱爱的一天",
            "desc": ["开心的一天", "#旭旭宝宝", "#宝妈"],
            "path": "aa.mp4",
        },
        {
            "title": "美好的一刻",
            "desc": ["旅行", "#风景", "#美食"],
            "path": "aa.mp4",
        },
        # ...
    ]
```
如上配置后运行main.py会打开两个无头浏览器同步执行自动化上传任务
<img width="1486" alt="image" src="https://github.com/user-attachments/assets/e6996b48-838c-42b2-a5ac-fd7630b7e1a2">



--- 
^ ⑉・ᴗ・⑉ ૮ ˃感谢支持<br />
<img src="https://github.com/user-attachments/assets/8b12eac8-cb25-435d-b098-bd4de82f8777" width="300" />








