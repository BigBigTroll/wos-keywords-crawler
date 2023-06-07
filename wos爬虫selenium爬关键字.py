from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

# 临时储存一下所有link
link_tmp = [
    
]

driver = webdriver.Firefox()

all_paper = []

count = 0

# 依次打开链接获取keywords
for paper_link in link_tmp:

    window_before = driver.window_handles[0]

    # Send GET request for the given http protocol (link)
    driver.execute_script("window.open('" + paper_link + "', '_blank');")

    # Wait approx 3 seconds to enable the consent cookies to show up
    time.sleep(15)

    # 切换至新的tab
    window_new = driver.window_handles[1]
    driver.switch_to.window(window_new)

    # 用soup来解析
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # doi
    doi = soup.find(id='FullRTa-DOI')
    # 年代
    indexedDate = soup.find(id='FullRTa-indexedDate')
    # 标题
    title = soup.find(id='FullRTa-fullRecordtitle-0')
    # 关键字
    keywords = soup.find_all(class_='mat-tooltip-trigger authorKeywordLink-en ng-star-inserted')
    # 增强关键字
    keywords_plus = soup.find_all(class_='mat-tooltip-trigger keywordsPlusLink')
    # 被引数
    citations = soup.find(id='FullRRPTa-citationsLabelPlural-ALLDB')
    # 期刊名
    journal = soup.find(class_='mat-focus-indicator mat-tooltip-trigger font-size-14 summary-source-title-link '
                               'remove-space no-left-padding mat-button mat-button-base mat-primary font-size-16 '
                               'ng-star-inserted')
    # 作者
    author_set = soup.find_all(class_='mat-tooltip-trigger authors value ng-star-inserted')

    # 用dict保存 单个对象 循环最后加入数组
    single_paper_info = {}
    if doi is None:
        pass
    else:
        single_paper_info['doi'] = doi.text
    if indexedDate is None:
        pass
    else:
        single_paper_info['indexedDate'] = indexedDate.text
    if journal is None:
        pass
    else:
        single_paper_info['journal'] = journal.text
    if title is None:
        pass
    else:
        single_paper_info['title'] = title.text

    keywords_text = []
    for word in keywords:
        keywords_text.append(word.text)
    single_paper_info['keywords'] = keywords_text

    keywords_plus_text = []
    for word in keywords_plus:
        keywords_plus_text.append(word.text)
    single_paper_info['keywords_plus'] = keywords_plus_text

    if citations is None:
        pass
    else:
        single_paper_info['citations'] = citations.text

    authors_text = []
    for author in author_set:
        authors_text.append(author.text)
    single_paper_info['authors'] = authors_text

    all_paper.append(single_paper_info)
    # 关闭标签页
    driver.close()
    # switch to parent window
    driver.switch_to.window(driver.window_handles[0])

    df = pd.DataFrame(all_paper)
    df.to_excel('output.xlsx', index=False)

    count = count + 1
    print(count)
