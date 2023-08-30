from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyscreenshot as ImageGrab
import os
import traceback

class wordpressbot:
    def __init__(self, _domain, _username, _password, _parts):
        global output, domain, username, password, parts, partName, subPartName
        output = "screenshot_bot/output/wordpress/"
        domain = _domain
        username = _username
        password = _password
        parts = _parts
        partName = ""
        subPartName = ""

    def logTitle(self):
        print("開始擷取 [" + partName + "] " + subPartName)

    def logError(self):
        print("========= 發生錯誤 =========")

    def startPart(self, name):
        global partName, subPartName
        partName = name
        subPartName = ""
        self.logTitle()
        self.setFileLocation(name)

    def startSubPart(self, name):
        global subPartName
        subPartName = name
        self.logTitle()

    def setFileLocation(self, name):
        global file_location
        file_location = output + name + "/"
        if not os.path.exists(file_location):
            os.makedirs(file_location)

    def saveImage(self, x1, y1, x2, y2):
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image.save(file_location + subPartName + ".png")

    def dismissNotice(self):
        driver.implicitly_wait(0)
        try:
            notice_dismiss = driver.find_elements(By.CLASS_NAME, 'notice-dismiss')
            for el in notice_dismiss:
                el.click()
        except:
            sleep(0.1)
        try:
            notice_dismiss = driver.find_elements(By.CSS_SELECTOR, "div.updraft-advert-dismiss a")
            for el in notice_dismiss:
                el.click()
        except:
            sleep(0.1)
        driver.implicitly_wait(30)

    def removeAlert(self):
        driver.implicitly_wait(0)
        try:
            alert = driver.find_element(By.CSS_SELECTOR, "div.components-surface.components-card.woocommerce-store-alerts")
            driver.implicitly_wait(30)
            alert = driver.find_element(By.CSS_SELECTOR, "div.components-surface.components-card.woocommerce-store-alerts.is-alert-update")
            driver.execute_script("arguments[0].style = 'display: none;';", alert)
            driver.implicitly_wait(0)
            alert = driver.find_element(By.CSS_SELECTOR, "div.error.inline")
            driver.execute_script("arguments[0].style = 'display: none;';", alert)
        except:
            sleep(0.1)
        driver.implicitly_wait(30)

    def addStyle(self, type, _element, extraStyle = ''):
        style = ""
        if type == "hidden":
            style = "text-decoration-line: line-through;text-decoration-thickness: 1rem;" + extraStyle           
        elif type == 'hidden-bg':
            style = "background-image: linear-gradient(to left, currentColor 90%, transparent 30%);color: black;" + extraStyle
        elif type == "highlight":
            style = "border: 2px solid red;" + extraStyle
        elif type == "custom":
            style = extraStyle
        driver.execute_script("arguments[0].style = '" + style + "';", _element)

    def setOption(self):
				#Handle chrome browser version missmatched issue
        global options
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)


    def start(self):
        global options
        options = webdriver.ChromeOptions()
        self.setOption()

        global driver
        try:
            driver = webdriver.Chrome(options=options)
        except:
            options = webdriver.EdgeOptions()
            self.setOption()
            driver = webdriver.Edge(options=options)

        driver.maximize_window()
        driver.implicitly_wait(30)

        driver.get(domain + "wp-admin")
        sleep(1)
        
        try:
            driver.implicitly_wait(0)
            driver.find_element(By.ID, 'user_login')
        except:
            driver.implicitly_wait(30)
            driver.get(domain + "backend-login")

        driver.find_element(By.ID, 'user_login').send_keys(username)
        driver.find_element(By.ID, 'user_pass').send_keys(password)
        driver.find_element(By.ID, 'wp-submit').click()

        if not os.path.exists(output):
            os.makedirs(output)

        # 公司網站
        if 1 in parts:
            try:
                self.startPart("公司網站")

                self.startSubPart("後端界面")
                driver.get(domain + "wp-admin/edit.php?post_type=page")
                self.saveImage(0, 70, 2000, 950)
            except:
                self.logError()

        # 網站備份系統
        if 2 in parts:
            try:
                self.startPart("網站備份系統")

                self.startSubPart("提供還原服務")
                driver.get(domain + "wp-admin/options-general.php?page=updraftplus")
                self.dismissNotice()
                sleep(1)
                self.addStyle("hidden", driver.find_element(By.CSS_SELECTOR, "span.updraft_time_now"))
                self.addStyle("hidden", driver.find_element(By.CSS_SELECTOR, "div#updraft_lastlogmessagerow > div"))
                elements = driver.find_elements(By.CSS_SELECTOR, "div.backup_date_label")
                for el in elements:
                    self.addStyle("hidden", el)
                self.saveImage(0, 70, 2000, 950)

                self.startSubPart("自動備份網站")
                driver.find_element(By.CSS_SELECTOR, "a#updraft-navtab-settings").click()
                sleep(1)
                self.saveImage(0, 70, 2000, 800)
            except:
                self.logError()

        # 網站統計系統
        if 3 in parts:
            try:
                self.startPart("網站統計系統")

                self.startSubPart("自動統計當日人數")
                driver.get(domain + "wp-admin/admin.php?page=wps_overview_page")
                self.dismissNotice()
                driver.find_element(By.CSS_SELECTOR, "div#wp-statistics-summary-widget div.o-table-wrapper")
                driver.find_element(By.ID, "wp-statistics-hits-meta-box-chart")
                driver.find_element(By.CSS_SELECTOR, "div#wp-statistics-pages-widget div.o-table-wrapper")
                driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "div.wps-wrap__main"))
                self.saveImage(0, 70, 2000, 840)

                self.startSubPart("可按地區_裝置類別等顯示統計")
                element = driver.find_element(By.ID, "wp-statistics-browsers-widget")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.saveImage(0, 70, 700, 950)
            except:
                self.logError()

        # 網站安全及防火牆
        if 4 in parts:
            try:
                self.startPart("網站安全及防火牆")

                self.startSubPart("自動要求所有管理員設置高難度密碼")
                driver.get(domain + "wp-admin/admin.php?page=itsec&path=%2Fsettings%2Fuser-groups")
                driver.find_element(By.LINK_TEXT, "Security Managers").click()
                self.addStyle("highlight", driver.find_element(By.LINK_TEXT, "Security Managers"))
                self.addStyle("highlight", driver.find_element(By.XPATH, "//h3[contains(text(), 'Password Requirements')]").find_element(By.XPATH, "following-sibling::*[1]"), "margin-right: auto;")
                self.saveImage(0, 70, 1630, 870)

                self.startSubPart("管理員登入_檔案改動等自動發送電郵")
                driver.get(domain + "wp-admin/admin.php?page=itsec&path=%2Fsettings%2Fnotification-center%2Ffile-change")
                self.addStyle("highlight", driver.find_element(By.LINK_TEXT, "File Change"))
                elements = driver.find_element(By.TAG_NAME, "legend").find_elements(By.XPATH, "following-sibling::*[position() <= 2]")
                for el in elements:
                    self.addStyle("highlight", el, "width: fit-content;")
                self.saveImage(0, 70, 1580, 870)
            except:
                self.logError()

        # 銷售單管理系統
        if 5 in parts:
            try:
                self.startPart("銷售單管理系統")

                self.startSubPart("新增銷售單_編輯銷售單_刪除銷售單_自動製作銷售單編號")
                driver.get(domain + "wp-admin/post-new.php?post_type=shop_order")
                self.removeAlert()
                for el in driver.find_elements(By.CSS_SELECTOR, "a.edit_address"):
                    el.click()
                self.addStyle("highlight", driver.find_element(By.CLASS_NAME, "wp-heading-inline"))
                self.addStyle("highlight", driver.find_element(By.ID, "woocommerce-order-actions"))
                self.saveImage(0, 70, 2000, 950)

                self.startSubPart("支援訂單部份交付")
                driver.get(domain + "wp-admin/post-new.php?post_type=shop_order")
                self.removeAlert()
                driver.find_element(By.CSS_SELECTOR, ".select2-selection.select2-selection--single").click()
                self.saveImage(0, 70, 1600, 700)

                self.startSubPart("退款處理")
                driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                self.removeAlert()
                elements = driver.find_elements(By.CSS_SELECTOR, "div.order_data_column")[1:3]
                for el in elements:
                    elements2 = el.find_elements(By.CSS_SELECTOR, "p a")
                    elements2.append(el.find_elements(By.TAG_NAME, "p")[0])
                    for el2 in elements2:
                        self.addStyle("hidden", el2, "color: black;")
                self.addStyle("hidden", driver.find_element(By.ID, "select2-customer_user-container"), "color: black;")
                self.addStyle("hidden", driver.find_element(By.CSS_SELECTOR, "span.woocommerce-Order-customerIP"), "color: black;")
                element = driver.find_element(By.ID, "postbox-container-2")
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                driver.find_element(By.CSS_SELECTOR, "button.button.refund-items").click()
                sleep(1)
                self.addStyle("highlight", driver.find_element(By.CSS_SELECTOR, "#woocommerce-order-items > div.inside > div.wc-order-data-row.wc-order-refund-items.wc-order-data-row-toggle > table"))
                self.saveImage(0, 70, 1600, 950)
            except:
                self.logError()

        # 客戶管理系統
        if 6 in parts:
            try:
                self.startPart("客戶管理系統")

                # self.startSubPart("記錄客戶資料後自動儲存")
                # driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                # driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                # product_name = driver.find_element(By.CLASS_NAME, "wc-order-item-name").text
                # self.removeCouponAlert()
                # elements = driver.find_elements(By.CSS_SELECTOR, "div.order_data_column")[1:3]
                # for el in elements:
                #     elements2 = el.find_elements(By.CSS_SELECTOR, "p a")
                #     elements2.append(el.find_elements(By.TAG_NAME, "p")[0])
                #     for el2 in elements2:
                #         self.addStyle("hidden", el2, "color: black;")
                # self.addStyle("hidden", driver.find_element(By.ID, "select2-customer_user-container"), "color: black;")
                # self.addStyle("hidden", driver.find_element(By.CSS_SELECTOR, "span.woocommerce-Order-customerIP"), "color: black;")
                # self.saveImage(0, 70, 1900, 600)

                self.startSubPart("會員制及會員名單管理_客戶購買記錄")
                driver.get(domain + "wp-admin/admin.php?page=wc-admin&path=%2Fcustomers")
                self.removeAlert()
                toggle_button = driver.find_element(By.CSS_SELECTOR, "button.components-button.woocommerce-ellipsis-menu__toggle")
                toggle_button.click()
                unchecked_indices = [1, 2, 7, 8, 9, 10]
                toggle_elements = driver.find_elements(By.CSS_SELECTOR, ".components-form-toggle input.components-form-toggle__input[type=checkbox]")
                for idx, toggle_element in enumerate(toggle_elements):
                    if idx in unchecked_indices:
                        if toggle_element.is_selected():
                            toggle_element.click()
                    else:
                        if not toggle_element.is_selected():
                            toggle_element.click()
                toggle_button.click()
                
                customer_name = driver.find_element(By.CSS_SELECTOR, "div.woocommerce-table__table table tr:not(:first-child) th a").text
                names = driver.find_elements(By.CSS_SELECTOR, "div.woocommerce-table__table table tr:not(:first-child) th a")
                for el in names:
                    self.addStyle("hidden-bg", el)
                users = driver.find_elements(By.CSS_SELECTOR, "div.woocommerce-table__table table tr:not(:first-child) td:nth-child(2)")
                for el in users:
                    driver.execute_script("arguments[0].innerHTML = `<span>${arguments[0].innerHTML}</span>`;", el)
                    self.addStyle("hidden-bg", el.find_element(By.CSS_SELECTOR, "span"))
                emails = driver.find_elements(By.CSS_SELECTOR, "div.woocommerce-table__table table tr:not(:first-child) td:nth-child(3) a")
                for el in emails:
                    self.addStyle("hidden-bg", el)
                amounts = driver.find_elements(By.CSS_SELECTOR,"div.woocommerce-table__table table tr:not(:first-child) td:nth-child(5)")
                for el in amounts:
                    driver.execute_script("arguments[0].innerHTML = `<span>${arguments[0].innerHTML}</span>`;", el)
                    self.addStyle("custom",el.find_element(By.CSS_SELECTOR, "span"),'background-image:linear-gradient(to left, currentColor 60%, transparent 30%);')
                AOV = driver.find_elements(By.CSS_SELECTOR,"div.woocommerce-table__table table tr:not(:first-child) td:nth-child(6)")
                for el in AOV:
                    driver.execute_script("arguments[0].innerHTML = `<span>${arguments[0].innerHTML}</span>`;", el)
                    self.addStyle("custom",el.find_element(By.CSS_SELECTOR, "span"),'background-image:linear-gradient(to left, currentColor 60%, transparent 30%);')
                
                self.saveImage(0, 70, 1900, 880)

                self.startSubPart("搜尋功能")
                customer_name = driver.find_element(By.CSS_SELECTOR, "div.woocommerce-table__table table tr:not(:first-child) th a").text.split(' ')[0]
                driver.find_element(By.CSS_SELECTOR, "input.woocommerce-select-control__control-input").send_keys(customer_name)
                element = driver.find_element(By.CSS_SELECTOR, "div.woocommerce-select-control__listbox button:not(:first-child)")
                driver.execute_script("arguments[0].innerHTML = `<span>${arguments[0].innerHTML}</span>`;", element)
                self.addStyle("custom",element.find_element(By.CSS_SELECTOR, "span"),'background-image:linear-gradient(to left, currentColor 60%, transparent 30%);')
                self.saveImage(0, 70, 1900, 880)
            except:
                self.logError()

        # 報告管理系統
        if 7 in parts:
            try:
                self.startPart("報告管理系統")

                driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                product_name = driver.find_element(By.CLASS_NAME, "wc-order-item-name").text

                self.startSubPart("年月日製作銷售報告")
                driver.get(domain + "wp-admin/admin.php?page=wc-reports&range=year")
                self.removeAlert()
                driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "div.wrap.woocommerce"))

                # driver.find_element(By.CSS_SELECTOR, "div.woocommerce-summary__item-value span")
                # driver.find_element(By.CSS_SELECTOR, "div.d3-chart__tooltip")
                self.saveImage(0, 70, 2000, 1000)
                
                # self.startSubPart("製作最受歡迎服務報告")
                # self.saveImage(0, 70, 2000, 1000)

                self.startSubPart("製作單一服務的銷售報告")
                driver.get(domain + "wp-admin/admin.php?page=wc-admin&path=%2Fanalytics%2Fproducts&period=year&compare=previous_year")
                driver.find_elements(By.CSS_SELECTOR, "button.components-button.woocommerce-dropdown-button")[1].click()
                driver.find_elements(By.CSS_SELECTOR, "button.components-button.woocommerce-filters-filter__button")[1].click()
                driver.find_element(By.CSS_SELECTOR, "input.woocommerce-select-control__control-input").send_keys(product_name)
                driver.find_element(By.CSS_SELECTOR, "button.components-button.woocommerce-select-control__option").click()
                self.removeAlert()
                driver.execute_script("window.scrollBy(0,30);")
                driver.find_element(By.CSS_SELECTOR, "div.woocommerce-summary__item-label span")
                driver.find_element(By.CSS_SELECTOR, "td.woocommerce-table__item a")
                self.saveImage(0, 70, 2000, 1000)
            except:
                self.logError()

        # 公司報表系統
        if 8 in parts:
            try:
                self.startPart("公司報表系統")

                driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                product_name = driver.find_element(By.CLASS_NAME, "wc-order-item-name").text

                self.startSubPart("總訂單報表_總發票報表")
                driver.get(domain + "wp-admin/admin.php?page=wc-admin&path=%2Fanalytics%2Forders&period=year&compare=previous_year")
                self.removeAlert()
                driver.find_element(By.CSS_SELECTOR, "div.woocommerce-summary__item-value span")
                driver.find_element(By.CSS_SELECTOR, "div.d3-chart__tooltip")
                self.saveImage(0, 70, 2000, 1000)

                self.startSubPart("服務銷量報表_單一服務銷量報表")
                driver.get(domain + "wp-admin/admin.php?page=wc-admin&path=%2Fanalytics%2Fproducts&period=year&compare=previous_year")
                driver.find_elements(By.CSS_SELECTOR, "button.components-button.woocommerce-dropdown-button")[1].click()
                driver.find_elements(By.CSS_SELECTOR, "button.components-button.woocommerce-filters-filter__button")[1].click()
                driver.find_element(By.CSS_SELECTOR, "input.woocommerce-select-control__control-input").send_keys(product_name)
                driver.find_element(By.CSS_SELECTOR, "button.components-button.woocommerce-select-control__option").click()
                self.removeAlert()
                driver.execute_script("window.scrollBy(0,30);")
                driver.find_element(By.CSS_SELECTOR, "div.woocommerce-summary__item-label span")
                driver.find_element(By.CSS_SELECTOR, "td.woocommerce-table__item a")
                self.saveImage(0, 70, 2000, 1000)
            except:
                self.logError()

        # 訂單管理系統
        if 9 in parts:
            try:
                self.startPart("訂單管理系統")

                self.startSubPart("訂單功能_發票功能")
                driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                self.removeAlert()
                elements = driver.find_elements(By.CSS_SELECTOR, "div.order_data_column")[1:3]
                for el in elements:
                    elements2 = el.find_elements(By.CSS_SELECTOR, "p a")
                    elements2.append(el.find_elements(By.TAG_NAME, "p")[0])
                    for el2 in elements2:
                        self.addStyle("hidden", el2, "color: black;")
                self.addStyle("hidden", driver.find_element(By.ID, "select2-customer_user-container"), "color: black;")
                self.addStyle("hidden", driver.find_element(By.CSS_SELECTOR, "span.woocommerce-Order-customerIP"), "color: black;")
                # self.addStyle("highlight", driver.find_element(By.CSS_SELECTOR, "a.page-title-action"))
                # self.addStyle("highlight", driver.find_element(By.CSS_SELECTOR, "table.wf_invoice_metabox"))
                self.saveImage(0, 70, 1900, 1000)
            except:
                self.logError()

        # 產品管理系統
        if 10 in parts:
            try:
                self.startPart("產品管理系統")

                self.startSubPart("建立_更改_刪除產品功能")
                driver.get(domain + "wp-admin/edit.php?post_type=product")
                self.dismissNotice()
                self.removeAlert()
                self.addStyle("highlight", driver.find_elements(By.LINK_TEXT, "新增")[1])
                element = driver.find_element(By.CSS_SELECTOR, "td.name.column-name")
                self.addStyle("highlight", element)
                ActionChains(driver).move_to_element(element).perform()
                self.saveImage(0, 70, 1900, 1000)

                self.startSubPart("製作貨物編號")
                driver.find_element(By.CSS_SELECTOR, "a.row-title").click()
                driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, "woocommerce-product-data"))
                driver.execute_script("window.scrollBy(0,-70);")
                driver.find_element(By.CSS_SELECTOR, "li.inventory_options a").click()
                self.addStyle("highlight", driver.find_element(By.CSS_SELECTOR, "p.form-field._sku_field"))
                sleep(0.5)
                self.saveImage(0, 70, 1900, 1000)

                self.startSubPart("設定貨物類別")
                driver.get(domain + "wp-admin/edit-tags.php?taxonomy=product_cat&post_type=product")
                self.removeAlert()
                self.saveImage(0, 70, 1900, 800)
            except:
                self.logError()
                traceback.print_exc()


        # 付款管理系統
        if 11 in parts:
            try:
                self.startPart("付款管理系統")

                self.startSubPart("可設定付款方式_付款時可選擇付款方式_支援多種付款系統")
                driver.get(domain + "wp-admin/admin.php?page=wc-settings&tab=checkout")
                self.removeAlert()
                self.saveImage(0, 70, 1900, 800)
                
                self.startSubPart("自動計算折扣")
                driver.get(domain + "wp-admin/edit.php?post_type=shop_order")
                driver.find_element(By.CSS_SELECTOR, "a.order-view").click()
                driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "div.woocommerce_order_items_wrapper"))
                driver.execute_script("window.scrollBy(0,-70);")
                self.saveImage(0, 70, 1600, 550)
                
                self.startSubPart("可設定活動_優惠等")
                driver.get(domain + "wp-admin/edit.php?post_type=shop_coupon")
                self.removeAlert()
                self.saveImage(0, 70, 1900, 500)
            except:
                self.logError()