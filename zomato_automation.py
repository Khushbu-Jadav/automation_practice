from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
        user_data_dir = "./user_data"
        context = p.chromium.launch_persistent_context(user_data_dir, headless=False,slow_mo=1000)
 
        page = context.new_page()
        page.goto("https://www.zomato.com/ahmedabad/nook-by-grace-coffee-co-navrangpura/book")

        page.get_by_text("Book a table").nth(0).click()

        #date
        page.locator("//div[@class='sc-qnejpk-9 cUZRcH']").nth(0).click()
        page.locator("//div[@aria-label='Mon, 06 Jul']").click()

        #guest
        page.locator("//div[@class='sc-qnejpk-9 cUZRcH']").nth(1).click()
        page.locator("//div[@aria-label='4 guests']").click()

        #dinner
        page.locator("//div[@class='sc-qnejpk-9 cUZRcH']").nth(2).click()
        page.locator("//div[@aria-label='Dinner']").click()

        #time
        page.locator("//div[@class='sc-bFADNz hUuLZX']").nth(2).click()

        #offer
        page.locator("//div[@class='sc-bFADNz eseAyo']").nth(1).click()

        #proceed to cart
        page.locator("//div[@class='sc-bFADNz jbinGU']").click()

        #book now #proceed to payment
        page.locator("//div[@class='sc-bFADNz kmtoAj']").nth(0).click()

        #pay
        page.locator("//span[@class='sc-1kx5g6g-3 dkwpEa']").nth(0).click()

        time.sleep(15)
        context.close()