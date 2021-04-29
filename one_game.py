# scraper for football games in "https://www.bet.pt/live-betting/"
# Author: Gustavo Morais
# Github: https://github.com/GustavoGil13

import time
import pandas as pd
import datetime
import os
from bs4 import BeautifulSoup
from selenium import webdriver

pc_path = os.getcwd().replace("\\","/") + "/"
webdriver_path = pc_path + "/WebDrivers/chromedriver.exe"
games_location = pc_path + "/games_scraped/"

global_url = "https://www.bet.pt"

dt = datetime.datetime.today()
head = ["game","home_odds","draw_odds","away_odds","home_goals","away_goals","home_possession","away_possession","home_opportunities","away_opportunities","home_shots_on_goal",
        "away_shots_on_goal","home_shots_off_goal","away_shots_off_goal","home_corners","away_corners","home_yellows_cards","away_yellows_cards","home_red_cards",
        "away_red_cards","home_fouls","away_fouls","home_odds_next_goal","odds_no_goal","away_odds_next_goal","full_time"]

browser = webdriver.Chrome(webdriver_path)
browser.get("https://www.bet.pt/live-betting/")
browser.execute_script("window.scrollTo(0, 300)")
time.sleep(5)

html_live_betting = browser.page_source
soup_live_betting = BeautifulSoup(html_live_betting, 'lxml')

a_links = soup_live_betting.find_all("a",href=True)
links = [link["href"] for link in a_links if "#" in link["href"]]
links = list(dict.fromkeys(links))
print(f"Found {str(len(links))} games:")

game_names = [games_names_text.text for games_names_text in soup_live_betting.find_all("div", class_="rj-ev-list__ev-card__section-item rj-ev-list__ev-card__names")]

for i, game in enumerate(game_names):
    print(f"{i + 1}: {game}")

n = int(input("Choose a game: ")) - 1
url = global_url + links[n]

browser.get(url)
time.sleep(5)

jogo_stats = []
df = pd.DataFrame(jogo_stats,columns=head)

home_odds = 0
draw_odds = 0
away_odds = 0

home_odds_next_goal = 0
odds_no_goal = 0
away_odds_next_goal = 0

t = ""
game_status = ""
while game_status != "Acabou" or game_status != "Adiado" or "Partida sem cobertura" in game_status or "Adiado" in t:

    html_game = browser.page_source
    game_soup = BeautifulSoup(html_game, 'lxml')

    try:
        check1 = game_soup.find("div",class_="sr-status-limited-coverage").text
    except Exception:
        check1 = ""

    if "Partida sem cobertura" in check1:
        break
    
    try:
        check = game_soup.find("table",class_="rj-scoreboard__live-table")
    except Exception:
        check = None

    if check != None:
        break
    
    try:
        game_status = game_soup.find("div", class_="sr-status-info-fullscore").text.strip()
    except Exception:
        game_status = ""
    
    
    if game_status == "Intervalo" or game_status == "Esperando tempo Extra" or "INT" in game_status:
        time.sleep(30)
        browser.refresh()
        browser.get(url)
    else:

        try:
            t = game_soup.find("div", class_="sr-status-info-fullscore").text.replace(" ", "").replace(u'\xa0', u'').split("/")[0]
        except Exception:
            t = np.nan

        if "45:00+3" in str(t):
            browser.refresh()
            browser.get(url)
            time.sleep(5)   

        try:
            odds_headline = game_soup.find("h4", class_="toggleableHeadline clearfix expanded branch_header_class_1").text.strip()
        except Exception:
            odds_headline = ""
            if "90:00+" in str(t):
                break

        if odds_headline == "1X2":
            odds_info = game_soup.find_all("span", class_="bet-odds", limit=3)
            odds1X2 = [odds_number.text for odds_number in odds_info]
            home_odds, draw_odds, away_odds = [float(i) for i in odds1X2]
            home_odds_next_goal, odds_no_goal, away_odds_next_goal = [0, 0, 0]
        elif "º Golo" in odds_headline:
            odds_info = game_soup.find_all("span", class_="bet-odds", limit=3)
            odds = [odds_1.text for odds_1 in odds_info]
            home_odds_next_goal, odds_no_goal, away_odds_next_goal = [float(i) for i in odds]
            home_odds,draw_odds,away_odds = [0, 0, 0]
        else:
            browser.refresh()
            browser.get(url)
            time.sleep(5)

        try:
            home_team = game_soup.find("div", class_="sr-team-name sr-team-name-home").text.replace(" ", "")
        except Exception:
            pass

        try:
            away_team = game_soup.find("div", class_="sr-team-name sr-team-name-away").text.replace(" ", "")
        except Exception:
            pass
        
        try:
            goals = game_soup.find("div", class_="sr-result").text.replace(" ", "").split(":")
            home_goals, away_goals = [int(i) for i in goals]
        except Exception:
            home_goals, away_goals = (np.nan,np.nan)

        try:
            ball_possession = game_soup.find("div", class_="sr-stats-wrapper sr-stat-110 sr-clearfix").text.split()
            home_possession = int(ball_possession[0])
            away_possession = int(ball_possession[2])
        except Exception:
            home_possession, away_possession = (np.nan,np.nan)

        try:
            goals_opportunities = game_soup.find("div", class_="sr-stats-wrapper sr-stat-goalattempts sr-clearfix").text.split()
            home_opportunities, away_opportunities = [int(i) for i in goals_opportunities[:2]]
        except Exception:
            home_opportunities, away_opportunities = (np.nan,np.nan)

        try:
            goal_shots = game_soup.find("div", class_="sr-stats-wrapper sr-stat-125 sr-clearfix").text.split()
            home_shots_on_goal, away_shots_on_goal = [int(i) for i in goal_shots[:2]]
        except Exception:
            home_shots_on_goal, away_shots_on_goal = (np.nan,np.nan)

        try:
            shots_off = game_soup.find("div", class_="sr-stats-wrapper sr-stat-126 sr-clearfix").text.split()
            home_shots_off_goal, away_shots_off_goal = [int(i) for i in shots_off[:2]]
        except Exception:
            home_shots_off_goal, away_shots_off_goal = (np.nan,np.nan)

        try:
            corners = game_soup.find("div", class_="sr-stats-wrapper sr-stat-124 sr-clearfix").text.split()
            home_corners, away_corners = [int(i) for i in corners[:2]]
        except Exception:
            home_corners, away_corners = (np.nan,np.nan)

        try:
            yellows_cards = game_soup.find("div", class_="sr-stats-wrapper sr-stat-40 sr-clearfix").text.split()
            home_yellows_cards, away_yellows_cards = [int(i) for i in yellows_cards[:2]]
        except Exception:
            home_yellows_cards, away_yellows_cards = (np.nan,np.nan)

        try:
            red_cards = game_soup.find("div", class_="sr-stats-wrapper sr-stat-50 sr-clearfix").text.split()
            home_red_cards, away_red_cards = [int(i) for i in red_cards[:2]]
        except Exception:
            home_red_cards, away_red_cards = (np.nan,np.nan)

        try:
            fouls = game_soup.find("div", class_="sr-stats-wrapper sr-stat-129 sr-clearfix").text.split()
            home_fouls, away_fouls = [int(i) for i in fouls[:2]]
        except Exception:
            home_fouls, away_fouls = (np.nan,np.nan)

        try:
            equipa_stats = [home_team + "vs" + away_team,
                            home_odds, draw_odds, away_odds,
                            home_goals, away_goals,
                            home_possession, away_possession,
                            home_opportunities, away_opportunities,
                            home_shots_on_goal, away_shots_on_goal,
                            home_shots_off_goal, away_shots_off_goal,
                            home_corners, away_corners,
                            home_yellows_cards, away_yellows_cards,
                            home_red_cards, away_red_cards,
                            home_fouls, away_fouls,
                            home_odds_next_goal, odds_no_goal, away_odds_next_goal,
                            t]
        except Exception:
            pass
        
        try:
            if equipa_stats[:-1] != jogo_stats[:-1]:
                jogo_stats = equipa_stats
                df = df.append({column_name:jogo_stats[i] for i, column_name in enumerate(head)}, ignore_index=True)
                end_path = games_location + home_team + "vs" + away_team + "_" + str(dt.day) + "_" + str(dt.month) + ".xlsx"
                df.to_excel(end_path)
                print(df)
        except Exception:
            pass

    time.sleep(10)

print("Game ended")
browser.close()
browser.quit()