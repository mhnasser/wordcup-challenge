# Imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import warnings
warnings.filterwarnings("ignore")

# Configs
driver_path = r'C:\Users\moham\Documents\utils\driver\chromedriver.exe'
url = 'https://www.fifa.com/fifa-world-ranking/men?dateId=id13792'
ranking_xpath = '//*[@id="content"]/main/section[2]/div/div/div[1]/table/tbody/tr/td[1]'
team_xpath = '//*[@id="content"]/main/section[2]/div/div/div[1]/table/tbody/tr/td[3]/span[1]'
score_xpath ='//*[@id="content"]/main/section[2]/div/div/div[1]/table/tbody/tr/td[4]/div/div[1]'
drill_button_xpath = '//*[@id="content"]/main/section[1]/div/div/div[1]/div[2]/div/button/div'
date_button_xpath = '//*[@id="content"]/main/section[1]/div/div/div[1]/div[2]/div/div/button[{i}]'
date_html_class = 'ff-dropdown_dropupContentButton__WC4zi'

def set_options():
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)

    return options

def get_url(year):

    browser.get(url.format(year=year))
    sleep(3)

    browser.find_element(By.ID, 'onetrust-reject-all-handler').click()
    sleep(3)

    browser.find_element(By.XPATH, drill_button_xpath).click()
    sleep(3)

def get_scores_date():

    dates_web_element = browser.find_elements(By.CLASS_NAME, 'ff-dropdown_dropupContentButton__WC4zi')
    dates = [date.text for date in dates_web_element]

    return dates, dates_web_element

def get_team_score():
    
    rankings = [team.text for team in browser.find_elements(By.XPATH, ranking_xpath)]
    teams = [team.text for team in browser.find_elements(By.XPATH, team_xpath)]
    scores = [score.text for score in browser.find_elements(By.XPATH, score_xpath)]

    return rankings, teams, scores

if __name__ == '__main__':

    df_list = list()
    browser = webdriver.Chrome(options=set_options(), executable_path=driver_path)
    
    get_url()
    dates, dates_web_element = get_scores_date()

    for n, date in enumerate(dates_web_element):

        sleep(0.5)
        button = browser.find_element(By.XPATH, date_button_xpath.format(i=n+1))
        browser.execute_script("arguments[0].click();", button)

        rankings, teams, scores = get_team_score()
        df_temp = pd.DataFrame(list(zip(rankings, teams, scores)),
                               columns=['rank','team', 'score'])
        df_temp['date'] = dates[n]
        df_list.append(df_temp)

        sleep(0.5)

        browser.find_element(By.XPATH, drill_button_xpath).click()

    df_final = pd.concat(df_list)
    df_final.to_csv('../data/scraped/fifa_scores.csv', index=False)