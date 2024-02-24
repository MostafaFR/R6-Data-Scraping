from turtle import title
from requests_html import HTMLSession
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.utils.exceptions import InvalidFileException
import os
import shutil


class LiquipediaScraper:
    def __init__(self, base_url="https://liquipedia.net"):
        self.base_url = base_url
        self.session = HTMLSession()
        self.excel_manager = ExcelManager()
        self.image_downloader = ImageDownloader(self.session)
        self.team_scraper = TeamScraper(self.session, self.base_url, self.image_downloader, self.excel_manager)
        self.tournament_scraper = TournamentScraper(self.session, self.base_url)

    def run(self):
        # self.team_scraper.scrape_teams()
        self.tournament_scraper.scrape_tournaments()
        self.excel_manager.save()


class ExcelManager:
    def __init__(self, file_path="out/LiquipediaScraping.xlsx"):
        self.file_path = file_path
        self.workbook = None
        self.load_or_create_workbook()

    def load_or_create_workbook(self):
        if not os.path.exists(self.file_path):
            self.workbook = Workbook()
            print("Fichier Excel créé avec succès.")
        else:
            try:
                self.workbook = load_workbook(self.file_path)
                print("Fichier Excel chargé avec succès.")
            except InvalidFileException:
                print("Le fichier Excel est corrompu et ne peut pas être ouvert. Un nouveau fichier sera créé.")
                self.workbook = Workbook()
                print("Fichier Excel créé avec succès.")
        self.prepare_sheet()

    def prepare_sheet(self):
        if "Players" in self.workbook.sheetnames:
            self.workbook.remove(self.workbook["Players"])
        elif self.workbook.active.title == "Sheet":
            self.workbook.remove(self.workbook["Sheet"])
        self.players_sheet = self.workbook.create_sheet(title="Players")
        self.players_sheet.append(["Flag", "Player Name", "Player Surname", "Role", "Team"])

    def save(self):
        self.workbook.save(self.file_path)
        print("Fichier Excel enregistré avec succès.")


class ImageDownloader:
    def __init__(self, session, media_folder="media/"):
        self.media_folder = media_folder
        self.session = session
        if not os.path.exists(self.media_folder):
            os.makedirs(self.media_folder)
        if not os.path.exists(self.media_folder + "TeamLogo"):
            os.makedirs(self.media_folder + "TeamLogo")
        if not os.path.exists(self.media_folder + "PlayerFlag"):
            os.makedirs(self.media_folder + "PlayerFlag")

    @staticmethod
    def get_image_name_from_url(url):
        return url.split("/")[-1]

    def download_image(self, folder, image_url):
        r = self.session.get(image_url)
        print(image_url)
        image_name = self.get_image_name_from_url(image_url)
        with open(self.media_folder + folder + image_name, "wb") as f:
            f.write(r.content)
        f.close()


class TeamScraper:
    def __init__(self, session, base_url, image_downloader, excel_manager):
        self.session = session
        self.base_url = base_url
        self.image_downloader = image_downloader
        self.excel_manager = excel_manager

    def scrape_teams(self, teams_url="https://liquipedia.net/rainbowsix/Portal:Teams"):
        r = self.session.get(teams_url)
        # Recupère la liste des régions
        region_html_list = r.html.find("div.tabs-static li")
        region_list = []
        for region_html in region_html_list:
            region = region_html.find("a", first=True).full_text
            if region != "Overview" and region != "Players":
                region_list.append(region)

        # Recupère la liste des équipes par région
        for region in region_list:
            url_region = teams_url + "/" + region
            r = self.session.get(url_region)
            team_html_list = r.html.find("div.template-box table.wikitable")

            for team_html in team_html_list:
                team_logo = team_html.find("span.team-template-image-icon img", first=True).attrs["src"]
                self.image_downloader.download_image("TeamLogo/", self.base_url + team_logo)

                team_name = team_html.find("span.team-template-text", first=True).full_text
                player_html_list = team_html.find("tr")[2:]
                for player_html in player_html_list:
                    player_flag = player_html.find("td img")[0].attrs["src"]
                    player_surname = player_html.find("td")[0].full_text
                    player_name = player_html.find("td")[1].full_text
                    player_role = player_html.find("td")[2].full_text

                    # download playerflag image si elle n'existe pas
                    if not os.path.exists(self.image_downloader.media_folder + self.image_downloader.get_image_name_from_url(player_flag)):
                        self.image_downloader.download_image("PlayerFlag/", self.base_url + player_flag)

                    # Insertion dans le fichier excel
                    self.excel_manager.players_sheet.append(["", player_name, player_surname, player_role, team_name])
                    # insertion de l'image dans le fichier excel
                    flag = Image(self.image_downloader.media_folder + "PlayerFlag/" + self.image_downloader.get_image_name_from_url(player_flag))
                    self.excel_manager.players_sheet.add_image(
                        flag,
                        get_column_letter(1) + str(self.excel_manager.players_sheet.max_row),
                    )
                    print(f"Joueur {player_name} {player_surname} ajouté pour l'équipe {team_name}")


class TournamentScraper:
    def __init__(
        self,
        session,
        base_url,
        r6_base_url="https://liquipedia.net/rainbowsix/",
        list_tiers=[
            "S-Tier_Tournaments",
            "A-Tier_Tournaments",
            "B-Tier_Tournaments",
            "C-Tier_Tournaments",
        ],
    ):
        self.session = session
        self.base_url = base_url
        self.r6_base_url = r6_base_url
        self.list_tiers = list_tiers

    def scrape_tournaments(self):
        if len(self.list_tiers) == 0 or self.list_tiers == None:
            print("Aucun tournoi n'a été trouvé.")
            return

        header_list_temp = [
            "G & S",
            "Tournament",
            "Date",
            "Prize\xa0Pool",
            "Location",
            "P#",
            "Winner",
            "Runner-up",
        ]

        for tiers in self.list_tiers:
            url_tier = self.r6_base_url + tiers
            r = self.session.get(url_tier)

            header_list_temp = []
            headers_html = r.html.find("div.mw-parser-output div.gridTable.tournamentCard", first=True).find("div.gridHeader div.gridCell")
            for header in headers_html:
                header_list_temp.append(header.full_text)

            tournaments_html_list = r.html.find("div.mw-parser-output div.gridTable.tournamentCard div.gridRow")
            for tournament_html in tournaments_html_list:
                # create tournament object with name, date, prize_pool, location, number_of_participants, winner, runner_up
                tournament = {
                    "name": tournament_html.find("div.gridCell.Tournament a")[-1].full_text,
                    "url": tournament_html.find("div.gridCell.Tournament a")[-1].attrs["href"],
                    "date": tournament_html.find("div.gridCell.Date", first=True).full_text,
                    "prize_pool": tournament_html.find("div.gridCell.Prize", first=True).full_text,
                    "location": tournament_html.find("div.gridCell.Location", first=True).full_text,
                    "number_of_participants": tournament_html.find("div.gridCell.PlayerNumber", first=True).full_text,
                }
                try:
                    tournament["winner"] = tournament_html.find("div.gridCell.FirstPlace a")[-1].full_text
                    tournament["runner_up"] = tournament_html.find("div.gridCell.SecondPlace a")[-1].full_text
                except:
                    tournament["winner"] = ""
                    tournament["runner_up"] = ""
                MatchScraper(self.session, self.base_url, tournament)
            break


class MatchScraper:
    def __init__(self, session, base_url, tournament):
        self.session = session
        self.base_url = base_url
        self.tournament = tournament

    def scrape_match(self):
        r = self.session.get(self.base_url + self.tournament["url"])
        print(r.html.find("div.matchlist", first=True).full_text)

scraper = LiquipediaScraper()
scraper.run()
