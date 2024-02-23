from requests_html import HTMLSession
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.utils.exceptions import InvalidFileException
import os
import shutil

s = HTMLSession()
url_root = "https://liquipedia.net/"
url_rainbow6 = "https://liquipedia.net/rainbowsix"
url_teams = "https://liquipedia.net/rainbowsix/Portal:Teams"
url_tournaments = "https://liquipedia.net/rainbowsix/Portal:Tournaments"
list_tournaments = ["S-Tier_Tournaments", "A-Tier_Tournaments", "B-Tier_Tournaments", "C-Tier_Tournaments"]
excel_file = "out/LiquipediaScraping.xlsx"
media_folder = "media/"

def create_excel_file():
    workbook = Workbook()
    worksheet_players = workbook.active
    worksheet_players.title = "Players"
    worksheet_players.append(["Flag", "Player Name", "Player Surname", "Role", "Team"])
    workbook.save(excel_file)
    print("Fichier Excel créé avec succès.")
    return workbook


try:
    if not os.path.exists(excel_file):
        workbook = create_excel_file()
    else:
        # copie le fichier excel existant
        shutil.copyfile(excel_file, excel_file + ".bak")

        # Tentez d'ouvrir le fichier existant
        workbook = load_workbook(excel_file)
        print("Fichier Excel chargé avec succès.")
        if "Players" in workbook.sheetnames:
            workbook.remove(workbook["Players"])
            worksheet_players = workbook.create_sheet(title="Players")
            worksheet_players.append(
                ["Flag", "Player Name", "Player Surname", "Role", "Team"]
            )
        else:
            worksheet_players = workbook.create_sheet(title="Players")
            worksheet_players.append(
                ["Flag", "Player Name", "Player Surname", "Role", "Team"]
            )
except InvalidFileException:
    # Gère le cas où le fichier est corrompu et ne peut pas être ouvert
    print(
        "Le fichier Excel est corrompu et ne peut pas être ouvert. Un nouveau fichier sera créé."
    )
    workbook = create_excel_file()
except Exception as e:
    # Gestion d'autres types d'erreurs potentielles
    print(f"Une erreur inattendue est survenue: {e}")
    # delete le fichier excel et le remplacer par le bak
    os.remove(excel_file)
    shutil.copyfile(excel_file + ".bak", excel_file)


# Selectionne des feuilles
worksheet_players = workbook["Players"]


# Si le dossier media n'existe pas, on le crée
if not os.path.exists(media_folder):
    os.makedirs(media_folder)


def main():
    get_teams()


def get_image_name_from_url(url):
    return url.split("/")[-1]


def download_image(image_url):
    r = s.get(image_url)
    with open(media_folder + get_image_name_from_url(image_url), "wb") as f:
        f.write(r.content)


def get_teams():
    r = s.get(url_teams)
    # Recupère la liste des régions
    region_html_list = r.html.find("div.tabs-static li")
    region_list = []
    for region_html in region_html_list:
        region = region_html.find("a", first=True).full_text
        if region != "Overview" and region != "Players":
            region_list.append(region)

    # Recupère la liste des équipes par région
    for region in region_list:
        url_region = url_teams + "/" + region
        r = s.get(url_region)

        team_html_list = r.html.find("div.template-box table.wikitable")

        for team_html in team_html_list:
            team_logo = team_html.find(
                "span.team-template-image-icon img", first=True
            ).attrs["src"]
            download_image(url_root + team_logo)

            team_name = team_html.find("span.team-template-text", first=True).full_text
            player_html_list = team_html.find("tr")[2:]
            for player_html in player_html_list:
                player_flag = player_html.find("td img")[0].attrs["src"]
                player_surname = player_html.find("td")[0].full_text
                player_name = player_html.find("td")[1].full_text
                player_role = player_html.find("td")[2].full_text

                # download playerflag image si elle n'existe pas
                if not os.path.exists(
                    media_folder + get_image_name_from_url(player_flag)
                ):
                    download_image(url_root + player_flag)

                # Insertion dans le fichier excel
                worksheet_players.append(
                    ["", player_name, player_surname, player_role, team_name]
                )
                # insertion de l'image dans le fichier excel
                flag = Image(media_folder + get_image_name_from_url(player_flag))
                worksheet_players.add_image(
                    flag, get_column_letter(1) + str(worksheet_players.max_row)
                )
                print(
                    f"Joueur {player_name} {player_surname} ajouté pour l'équipe {team_name}"
                )
    workbook.save(excel_file)
    
def getMatchs():
    if len(list_tournaments) == 0 or list_tournaments == None:
        print("Aucun tournoi n'a été trouvé.")
        return
    for tournament in list_tournaments:
        url_tournament = url_rainbow6 + "/" + tournament
        r = s.get(url_tournament)
        match_html_list = r.html.find("div.mw-parser-output div.gridTable.tournamentCard")
        
        print(len(match_html_list))


# main()
getMatchs()
