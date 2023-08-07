import requests
from bs4 import BeautifulSoup

class Profile():
    def __init__(self, username = str):
        page = requests.get('https://gdbrowser.com/u/' + username)
        soup = BeautifulSoup(page.text, 'lxml')
        self.stars = int(soup.find(id="stars").text)
        self.diamonds = int(soup.find(id="diamonds").text)
        self.coins = int(soup.find(id="coins").text)
        self.usercoins = int(soup.find(id="usercoins").text)
        self.demons = int(soup.find(id="demons").text)
        self.creatorpoints = int(soup.find(id="creatorpoints").text)
        AID = page.text.split('Account ID: ')[1]
        PID = AID.split('<br>Player ID: ')[1].split('</p>\r\n\t\t</div>\r\n\r\n\t\t<img src=')[0]
        AID = AID.split('<br>Player ID: ')[0]
        self.AID = int(AID)
        self.PID = int(PID)
        self.main_color = int(str(soup.find(id="mainIcon")).split('col1="')[1].split('" col2="')[0])
        self.second_color = int(str(soup.find(id="mainIcon")).split('col1="')[1].split('" col2="')[1].split('" glow="')[0])
        self.cube = int(str(soup.find(id="mainIcon")).split('iconform="icon" iconid="')[1].split('" id="mainIcon"')[0])
        self.ship = int(str(list(soup.find(class_="lightBox center profilePostHide"))[3]).split('iconform="ship" iconid="')[1].split('" imgstyle="height')[0])
        self.ball = int(str(list(soup.find(class_="lightBox center profilePostHide"))[5]).split('iconform="ball" iconid="')[1].split('"></gdicon>')[0])
        self.ufo = int(str(list(soup.find(class_="lightBox center profilePostHide"))[7]).split('iconform="ufo" iconid="')[1].split('"></gdicon>')[0])
        self.wave = int(str(list(soup.find(class_="lightBox center profilePostHide"))[9]).split('iconform="wave" iconid="')[1].split('" imgstyle="height:')[0])
        self.robot = int(str(list(soup.find(class_="lightBox center profilePostHide"))[11]).split('iconform="robot" iconid="')[1].split('"></gdicon>')[0])
        self.spider = int(str(list(soup.find(class_="lightBox center profilePostHide"))[13]).split('iconform="spider" iconid="')[1].split('"></gdicon>')[0])
        self.globalrank = int(soup.find(id="globalrank0").text.split('\n ')[1].split('\n')[0])
        self.youtube = str(soup.find(id="youtube")).split('href="')[1].split('" id="')[0]
        self.twitter = str(soup.find(id="twitter")).split('href="')[1].split('" id="')[0]
        self.twich = str(soup.find(id="twitch")).split('href="')[1].split('" id="')[0]

class NewGrounds():
    def __init__(self, songID = str | int) -> None:
        page = requests.get('https://www.newgrounds.com/audio/listen/' + str(songID))
        soup = BeautifulSoup(page.text, 'lxml')
        self.ID = int(songID)
        self.name = str(soup.find(class_="rated-e").text)
        self.duration = page.text.split('</span> \t\t\t\t\t\t\t\t\t</dd>\n\t\t\t\t\t\t\t<dd>\n\t\t\t\t\t\t\t\t\t\t\t')[1].split('\t\t\t\t\t\t\t\t\t</dd>\n\t\t\t\t\t\t</dl>')[0]
        self.duration = str(self.duration.split(' min ')[0] + ':' + self.duration.split(' min ')[1].split(' sec')[0])
        self.author_link = str(soup.find(class_="item-details-main")).split('href="')[1].split('">')[0]
        self.author = str(soup.find(class_="item-details-main").text.split('\n\n')[1])
        self.songlink = 'https://www.newgrounds.com/audio/listen/' + str(songID)
        
class Level():
    def __init__(self, levelID = int | str) -> None:
        page = requests.get('https://gdbrowser.com/' + str(levelID))
        soup = BeautifulSoup(page.text, 'lxml')
        self.ID = int(levelID)
        self.name = str(soup.find(class_="pre").text)
        self.creator = str(soup.find(id="authorLink").text.split('By ')[1])
        self.downloads = list(soup.find_all("h1"))[6].text
        self.rating = list(soup.find_all("h1"))[7].text
        self.duration = str(list(soup.find_all(class_="valign inline smaller spaced"))[2].text)
        self.orbs = int(list(soup.find_all("h1"))[9].text)
        self.difficulty = str(soup.find(id="difficultytext").text)
        self.stars = int(soup.find(class_="smaller inline stars").text)
        self.diamonds = int(soup.find(class_="smaller inline diamonds").text)
        self.discr = list(soup.find_all(class_="pre"))[4].text
        self.songID = int(soup.find(id="songInfo").text.split(' \xa0\xa0 ')[0].split('SongID: ')[1])
        self.songsize = float(soup.find(id="songInfo").text.split(' \xa0\xa0 ')[1].split('Size: ')[1].split('MB')[0])
        self.originalID = int(page.text.split(".replace('[[ORIGINALINFO]]', ")[1].split(' ==  "0" ? "" :')[0])
        self.objects = int(page.text.split(".replace('[[OBJECTINFO]]', '")[1].split(' ==  "0" ? "" :')[0].split("'")[0])
        self.gdversion = float(page.text.split('<br>GD Version:  <cy>')[1].split('</cy>')[0])
        self.levelversion = int(page.text.split('<br>Version:  <cy>')[1].split('</cy>')[0])