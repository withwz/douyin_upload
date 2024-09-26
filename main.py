import asyncio
import os
import traceback
from utils.logger import logger
from playwright.async_api import Playwright, async_playwright
from utils.config import config


class DouyinUploader:
    def __init__(self, timeout: int, cookie_file: str, video_data: object):
        self.timeout = timeout * 1000  # 将超时时间转换为毫秒
        self.cookie_file = cookie_file
        self.ua = {
            "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36",
            "app": "com.ss.android.ugc.aweme/110101 Android 5.1.1",
        }
        self.video_path = config.video_path
        self.video_data = video_data
        self.ensure_video_path_exists()

    def ensure_video_path_exists(self):
        """确保视频路径存在，如果不存在则创建"""
        if not os.path.exists(self.video_path):
            os.makedirs(self.video_path)

    async def init_playwright(self, p: Playwright, headless=False):
        """初始化Playwright"""
        browser = await p.chromium.launch(
            headless=headless,
            chromium_sandbox=False,
            ignore_default_args=["--enable-automation"],
            channel="chrome",
        )
        return browser

    async def upload_video(self, p: Playwright) -> None:
        """上传视频的主要流程"""
        browser = await self.init_playwright(p)
        context = await browser.new_context(
            storage_state=self.cookie_file, user_agent=self.ua["web"]
        )
        page = await context.new_page()
        await page.add_init_script(path="stealth.min.js")
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")

        logger.info("正在判断账号是否登录")
        if "/creator-micro/" not in page.url:
            logger.info("账号未登录")
            return

        logger.info("账号已登录")

        try:
            # 等待文件上传按钮加载完成并可见
            await page.locator(".container-drag-info-Tl0RGH").wait_for(state="visible")
            logger.info("文件上传按钮已加载可见")

            file_path = os.path.join(self.video_path, self.video_data["path"])
            # 上传文件
            await page.set_input_files("input[type='file']", file_path)
            logger.info("文件已成功上传")

            logger.info("确认发布")
            await self.confirm_and_publish(page)

        except Exception as e:
            logger.error(f"发布视频失败，可能网页加载失败了: {e}")
            traceback.print_exc()

        finally:
            await browser.close()

    async def confirm_and_publish(self, page):
        """确认并发布视频"""
        try:
            # 等待页面跳转
            await page.wait_for_url(
                "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page"
            )
            logger.info("页面跳转成功，准备输入标题和标签")
            await self.input_video_title_and_tags(page)

            await self.set_declaration(page)

            # 点击发布按钮
            await self.publish_video(page)

        except Exception as e:
            logger.error(f"发布视频过程中出错: {e}")
            traceback.print_exc()

    async def set_declaration(self, page):
        """添加非原创声明"""

        # 点击添加非原创声明按钮
        await page.locator(".addUserDeclaration-Iw_U0p").click()

        await page.wait_for_timeout(500)

        content_network_locator = page.locator("span.semi-radio-addon").filter(
            has_text="内容取材网络"
        )
        await content_network_locator.scroll_into_view_if_needed()
        await content_network_locator.click(force=True)

        await page.wait_for_timeout(500)

        source_outside_locator = page.locator("span.semi-radio-addon").filter(
            has_text="取材站外"
        )
        await source_outside_locator.click(force=True)

        await page.wait_for_timeout(500)

        # 点击 '确定' 按钮
        confirm_button = page.locator(".btnWrapper-gQSo9N span").filter(has_text="确定")
        await confirm_button.scroll_into_view_if_needed()
        await confirm_button.click()

    async def input_video_title_and_tags(self, page):
        """输入视频标题和标签"""
        title_css_class = ".container-sGoJ9f"
        await page.locator(f"{title_css_class} > div").click()
        await page.type(title_css_class, self.video_data["title"])

        css_selector = ".zone-container"
        await page.locator(".ace-line > div").click()
        video_desc_tag = self.video_data["desc"]
        for tag in video_desc_tag:
            await page.type(css_selector, tag)
            await page.press(css_selector, "Space")
            logger.info(f"正在添加话题: {tag}")

        logger.info("视频标题输入完毕，准备发布")

    async def publish_video(self, page):
        """点击发布按钮并检查发布结果"""
        try:
            # 创建一个异步任务，等待页面跳转
            url_wait_task = asyncio.create_task(
                page.wait_for_url(
                    "https://creator.douyin.com/creator-micro/content/manage?enter_from=publish",
                    timeout=self.timeout,
                )
            )

            while True:
                await page.wait_for_timeout(10000)
                # 点击发布按钮
                await page.get_by_role("button", name="发布", exact=True).click()
                logger.info("发布按钮点击成功，继续等待页面跳转")

                # 每次点击后等待一段时间，避免太频繁点击
                await page.wait_for_timeout(2000)

                # 检查是否页面已经跳转
                if url_wait_task.done():
                    try:
                        # 如果任务成功，表示页面跳转完成
                        url_wait_task.result()  # 检查是否有异常
                        logger.info("页面跳转成功，视频发布成功")
                        break
                    except Exception as url_error:
                        # 如果页面跳转失败，记录日志并继续
                        logger.warning(f"页面跳转失败或未发布成功: {url_error}")
                        break  # 根据业务需求，可以选择退出或继续尝试发布

        except Exception as e:
            logger.error(f"发布视频失败: {e}")

    async def main(self):
        """主入口函数"""
        async with async_playwright() as playwright:
            await self.upload_video(playwright)


def find_files(directory, extension):
    """在指定路径中查找指定类型的文件"""
    path = os.path.abspath(directory)
    if not os.path.exists(path):
        os.makedirs(path)

    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith(extension)
    ]


async def run(video_data):
    """程序运行入口"""
    cookie_files = find_files("cookie", ".json")

    for index, cookie_file in enumerate(cookie_files, start=1):
        logger.info(f"正在使用账号[{index}]发布作品")
        uploader = DouyinUploader(60, cookie_file, video_data)
        await uploader.main()


async def upload_in_batches(video_data_list, batch_size=5, delay=20):
    for i in range(0, len(video_data_list), batch_size):
        # 每次取 batch_size 个任务
        batch = video_data_list[i : i + batch_size]

        # 创建任务列表，并发执行本批次
        tasks = [run(video_data) for video_data in batch]

        # 并发执行本批次任务
        await asyncio.gather(*tasks)

        # 如果还有下一批任务，等待 delay 秒
        if i + batch_size < len(video_data_list):
            print(f"等待 {delay} 秒后开始上传下一批...")
            await asyncio.sleep(delay)


async def main():
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
    ]

    # 创建任务列表，并发执行
    tasks = [run(video_data) for video_data in video_data_list]

    await upload_in_batches(video_data_list)


if __name__ == "__main__":
    # 运行主异步函数
    asyncio.run(main())
