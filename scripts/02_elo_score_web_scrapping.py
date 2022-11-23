# Imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

# Configs
driver_path = r'C:\Users\moham\Documents\utils\driver\chromedriver.exe'
base_url = 'https://www.eloratings.net/{y}'
ranking_xpath = '//*[@id="maintable_{y}"]/div[6]/div/div/div[1]'
team_xpath = '//*[@id="maintable_{y}"]/div[6]/div/div/div[2]/a'
score_xpath ='//*[@id="maintable_{y}"]/div[6]/div/div/div[3]'

def set_options():
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)

    return options

def get_url(year):

    browser.get(base_url.format(y=year))
    sleep(2)

def get_team_score(year):

    rankings = [team.text for team in browser.find_elements(By.XPATH, ranking_xpath.format(y=year))]
    teams = [team.text for team in browser.find_elements(By.XPATH, team_xpath.format(y=year))]
    scores = [score.text for score in browser.find_elements(By.XPATH, score_xpath.format(y=year))]

    return rankings, teams, scores


if __name__ == '__main__':

    df_list = list()
    browser = webdriver.Chrome(options=set_options(), executable_path=driver_path)
    print('\nColetando os Dados... \n')
    for year in tqdm(range(1930,2023)):

        get_url(year)
        rankings, teams, scores = get_team_score(year)
        
        
        df_temp = pd.DataFrame(list(zip(rankings, teams, scores)),
                               columns=['rank','team', 'score'])
        df_temp['year'] = year
        df_list.append(df_temp)

    print('Feito!')
    df_final = pd.concat(df_list, ignore_index=True)
    df_final.to_csv('../data/scraped/elo_scores.csv', index=False)
    print('DataFrame Salvo!')