## 抖音自动并发批量上传视频
没有其他视频生成等的代码，代码简单，调试方便，也方便和其他爬虫项目对接。

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

在main.py中配置video_data_list，path写video目录下的视频文件名称，运行python main.py 可并发执行上传

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


--- 
^ ⑉・ᴗ・⑉ ૮ ˃感谢支持<br />
<img src="https://github.com/user-attachments/assets/8b12eac8-cb25-435d-b098-bd4de82f8777" width="300" />








