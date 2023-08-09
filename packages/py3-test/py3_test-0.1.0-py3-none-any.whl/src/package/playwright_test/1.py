from playwright import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")

    # Click input[name="wd"]
    page.click('input[name="wd"]')

    # Fill input[name="wd"]
    page.fill('input[name="wd"]', "禾目大")

    # Press CapsLock
    page.press('input[name="wd"]', "CapsLock")

    # Fill input[name="wd"]
    page.fill('input[name="wd"]', "自动化测试实战宝典 ")

    # Press Enter
    page.press('input[name="wd"]', "Enter")
    # assert page.url() == "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E5%AE%9E%E6%88%98%E5%AE%9D%E5%85%B8%20&fenlei=256&rsv_pq=af40e9aa00012d5a&rsv_t=c659gpz2%2Fjri1SAoIXdT9gP%2BmrqufXzRtMSSAL0n0fv7GSoLF5vaiNVPA3U&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=38&rsv_sug1=22&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=8034&rsv_sug4=9153"

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
