from playwright import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.newContext()

    # Open new page
    page = context.newPage()

    # Go to https://www.meituan.com/
    page.goto("https://www.meituan.com/")

    # Click text="立即登录"
    page.click('text="立即登录"')
    # assert page.url == "https://passport.meituan.com/account/unitivelogin?service=www&continue=https%3A%2F%2Fwww.meituan.com%2Faccount%2Fsettoken%3Fcontinue%3Dhttps%253A%252F%252Fwww.meituan.com%252F"

    # Click input[name="password"]
    page.click('input[name="password"]')

    # Fill input[name="password"]
    page.fill('input[name="password"]', "Lijc0210")

    # Click input[name="commit"]
    page.click('input[name="commit"]')

    # Click //div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']
    page.click("//div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']")

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Double click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.dblclick('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Triple click div[id="yodaBox"]
    page.click('div[id="yodaBox"]', clickCount=3)

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Double click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.dblclick('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click input[name="email"]
    page.click('input[name="email"]')

    # Fill input[name="email"]
    page.fill('input[name="email"]', "19901718151")

    # Press Tab
    page.press('input[name="email"]', "Tab")

    # Fill input[name="password"]
    page.fill('input[name="password"]', "Lijc0210")

    # Click input[name="commit"]
    page.click('input[name="commit"]')

    # Click //div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']
    page.click("//div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']")

    # Click //div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']
    page.click("//div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']")

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBox"]
    page.click('div[id="yodaBox"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click //div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']
    page.click("//div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']")

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Double click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.dblclick('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Double click div[id="yodaBox"]
    page.dblclick('div[id="yodaBox"]')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Click //div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']
    page.click("//div[2]/div[2]/div[normalize-space(.)='请向右拖动滑块 请向右拖动滑块']")

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"
    page.click('div[id="yodaBoxWrapper"] >> text="请向右拖动滑块"')

    # Click div[id="yodaBoxWrapper"]
    page.click('div[id="yodaBoxWrapper"]')

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
