# bet-web-scraper

A basic Python Web Scraper that gets the statistics of football games in https://www.bet.pt/live-betting/ (website as been changed so the scipt does not work anymore)
<br>
I have around 3000 games scraped from the website. If you need them for research purpose or anything like that contact me via email: gustavogillmorais@gmail.com
<br>
# How to run the script
1. Create a virtual environment and activate it:
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
Found 10 games:
1: CD Tondela SL Benfica
2: Southampton Leicester
3: Celta de Vigo Levante
4: Marselha Strasbourg
5: Werder Bremen Leipzig
6: Esteghlal Tehran Al Shorta [IRQ]
7: Al-Hilal Al Ahli (EAU)
8: FK Istiklol DushanbeAGMK FK
9: Antuérpia Genk
10: CD Lugo Saragoça
Choose a game:
```
Just choose a game number, type it and press enter. It should redirect the web browser to the respective game and start scraping it. The game can then be found in the *games_scraped* folder (there is also an example of a game). Don´t mind the warnings and enjoy it!
