import asyncio
from pyppeteer import launch
from pyppeteer.launcher import Launcher


async def main():
    print("If you see an error here during build, there's something wrong with pyppeteer.")
    print("============")
    print(' '.join(Launcher().cmd))
    print("============")
    browser = await launch({ 'headless': True,  'args': [
        '--no-sandbox',
        '--single-process',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-zygote'
    ] })
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': '/tmp/example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())