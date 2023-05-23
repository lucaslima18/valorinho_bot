from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options



class BlitzggHandler():
    def __init__(self, username: str, tag: str) -> None:
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/google-chrome"
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        self.browser = Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), chrome_options=chrome_options)
        self.username = username
        self.tag = tag
        self.stats_data = {}
        self.wait = WebDriverWait(self.browser, 50)

    def __call__(self):
        self.last_match_overview()
        self.loading_match()
        print(self.stats_data)
    
    def player_main_page(self):
        return self.browser.get(f'https://blitz.gg/valorant/profile/{self.username}-{self.tag}')


    def last_match_overview(self):
        self.stats_data['match_overview'] = {}

        self.browser.get(f'https://blitz.gg/valorant/profile/{self.username}-{self.tag}')

        match = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "w-full"))
        )[0]
        topic_stats = match.find_elements(By.CLASS_NAME, 'type-subtitle2')
        subtopic_stats = match.find_elements(By.CLASS_NAME, 'match-sub-stat')

        self.stats_data['match_overview'] = {
            "type": match.find_element(By.CLASS_NAME, 'queue-name').text,
            "agent_image": match.find_element(
                By.CLASS_NAME, 'profile_match-image'
            ).get_attribute('src'),
            "scoreboard": topic_stats[0].text,
            "ama": topic_stats[1].text,
            "apr": topic_stats[2].text,
            "hs_avg": topic_stats[3].text,
            "map": subtopic_stats[0].text,
            "kda": subtopic_stats[1].text,
            "mdr": subtopic_stats[2].text,
            "points_avg": match.find_element(By.CLASS_NAME, 'avg-score').text,
            "time": match.find_element(By.CLASS_NAME, 'time-ago').text
        }

        return self.stats_data

    def loading_match(self):
        self.stats_data['players'] = {}
        match_info = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "w-full"))
        )[0]
        match_info_link = match_info.find_element(
            By.TAG_NAME, 'a'
        ).get_attribute('href')

        self.browser.get(match_info_link)

        players_list = self.wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'col-agent'))
        )
        team_players = [
            {
                "name": player.find_elements(By.CLASS_NAME, 'player-name')[0].text,
                "link": player.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            } for player in players_list[1:6]]
        enemy_players = [
            {
                "name": player.find_elements(By.CLASS_NAME, 'player-name')[0].text,
                "link": player.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            } for player in players_list[7:11]
        ]
        self.stats_data['players']['team_players'] = [{"name": player['name'], "rank": self.get_player_rank(player['link'])} for player in team_players]
        self.stats_data['players']['enemy_players'] = [{"name": player['name'], "rank": self.get_player_rank(player['link'])} for player in enemy_players]

        return self.stats_data

    def loading_team_players_data():
        ...

    def get_player_rank(self, player_url):
        self.browser.get(player_url)

        rank_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "type-body1-form--active"))
        )
        rank = rank_element.text

        return rank


BlitzggHandler(username='Kakaroto', tag='1415')()