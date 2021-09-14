import time
import pandas as pd
from driver import *

law_file = pd.read_excel("rawwestlawfile_1.xlsm", skiprows=[0])
law_file.drop(['Title', 'Result', 'Entity Name', 'Status'], axis=1, inplace=True)
print(law_file)
corp_terms = pd.read_csv(r"corp_terms_list.csv", names=['corpterms'])
lp_llc = []
for business_name in law_file['Business Name']:
    flag = False
    terms0 = business_name.split()
    for i in terms0:
        terms1 = i.split(',')
        for j in terms1:
            k = j.lower()
            if k in list(corp_terms['corpterms']):
                flag = True
                if k == "lp" or k == "llc":
                    lp_llc.append(business_name)
                break
            else:
                k = k.capitalize()
                if k in list(corp_terms['corpterms']):
                    flag = True
                    if k == "Lp" or k == "Llc":
                        lp_llc.append(business_name)
                    break
        if flag:
            break
    if not flag:
        law_file.drop(law_file.index[(law_file['Business Name'] == business_name)], axis=0, inplace=True)
law_file.reset_index(inplace=True)
law_file.drop('index', axis=1, inplace=True)
print(law_file)
print(lp_llc)

driver = Web()
for business_name in list(law_file['Business Name']):
    try:
        time.sleep(5)
        driver.get("https://businesssearch.sos.ca.gov/")
        time.sleep(5)
        if business_name in lp_llc:
            driver.get_element_by_id("LLCNameOpt").click()
        else:
            driver.get_element_by_id("CorpNameOpt").click()
        driver.get_element_by_id("SearchCriteria").send_keys(business_name)
        driver.get_element_by_xpath("//*[@id='formSearch']/div[5]/div/div/div/button").click()
        upper = business_name.upper()
        element_not_found = True
        while element_not_found:
            list_names = driver.get_elements_by_name("EntityId")
            for name in list_names:
                str_name = name.text
                if str_name.upper() == upper:
                    driver.get_element_by_xpath(f"//button[text()='{str_name}']").click()
                    element_not_found = False
                    break
            if element_not_found:
                try:
                    driver.get_element_by_css_selector("li.paginate_button.next.disabled")
                except selenium.common.exceptions.NoSuchElementException:
                    driver.get_element_by_xpath("//*[@id='enitityTable_next']/a").click()
                else:
                    break

        if not element_not_found:
            street_address = driver.get_element_by_xpath("//*[@id='maincontent']/div[3]/div[1]/div[6]/div[2]").text
            address1 = street_address.split('\n')
            law_file.loc[law_file['Business Name'] == business_name, 'Street Address'] = address1[0]
            address2 = address1[1].split()
            law_file.loc[law_file['Business Name'] == business_name, 'Zip'] = address2[-1]
            law_file.loc[law_file['Business Name'] == business_name, 'State'] = address2[-2]
            law_file.loc[law_file['Business Name'] == business_name, 'City'] = " ".join(address2[0:-2])
            law_file.loc[law_file['Business Name'] == business_name, 'Source'] = "https://businesssearch.sos.ca.gov/"
            law_file.to_csv("rawwestlawfile_1.csv")

        else:
            driver.get("https://www.corporationwiki.com/")
            time.sleep(5)
            driver.get_element_by_id("keywords").send_keys(business_name)
            time.sleep(5)
            driver.get_element_by_xpath("//*[@id='sub-search-bar']/div/span/button/span").click()
            time.sleep(5)
            list_names = driver.get_elements_by_class("ellipsis")
            for name in list_names:
                str_name = name.text
                if str_name.upper() == upper:
                    driver.get_element_by_xpath(f"//a[text()='{str_name}']").click()
                    law_file.loc[law_file['Business Name'] == business_name, 'Street Address'] = driver.\
                        get_element_by_xpath(f"//a[@class='list-group-item']/span/span[1]").text
                    law_file.loc[law_file['Business Name'] == business_name, 'City'] = driver.\
                        get_element_by_xpath(f"//a[@class='list-group-item']/span/span[2]").text
                    law_file.loc[law_file['Business Name'] == business_name, 'State'] = driver.\
                        get_element_by_xpath(f"//a[@class='list-group-item']/span/span[3]").text
                    law_file.loc[law_file['Business Name'] == business_name, 'Zip'] = driver.\
                        get_element_by_xpath(f"//a[@class='list-group-item']/span/span[4]").text
                    law_file.loc[law_file['Business Name'] == business_name, 'Source'] = \
                        "https://www.corporationwiki.com/"
                    break
            law_file.to_csv("rawwestlawfile_1.csv")
    except selenium.common.exceptions.NoSuchElementException:
        pass


