# bet-web-scraper

A basic Python Web Scraper that gets the statistics of football games in https://www.bet.pt/live-betting/
<br>
<br>
# How to run the script
1. Create a virtual environment:
```sh
python -m venv venv
```
2. Install the mandatory libraries to run the script:
```sh
pip install -r requirements.txt
```
You are now ready to start using it
<br>
<br>
# How to use the script
When you run the script, the first thing you see is a web browser poping up and, depending on how many games are on the website, something like this will be printed:
```sh
Found 3 games:
1: WuhanShanghai Shenhua
2: Zhetysu TaldykorganShakhtyor Karagandy 
3: FC Saburtalo TbilisiSamgurali Tskaltubo
Choose a game:
```
Just choose a game number, type it and press enter. It should redirect the web browser to the respective game and start scraping it. The game can then be found in the *games_scraped* folder. Don´t mind the warnings and enjoy it!