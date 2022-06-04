import requests
import json
from bs4 import BeautifulSoup

rawlinks = """
https://www.mediafire.com/folder/***1
https://www.mediafire.com/folder/***2
https://www.mediafire.com/folder/***3
"""

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Chrome/50.0",
           "Accept": "*/*",
           "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
           "Connection": "keep-alive",
           "Cache-Control": "no-cache",
           "Pragma": "no-cache"}

sesion = requests.session()
urlbase = "https://www.mediafire.com/folder/"
apifiles = "https://www.mediafire.com/api/1.4/folder/get_content.php?r=keyk&content_type=files&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key="
apifolders = "https://www.mediafire.com/api/1.4/folder/get_content.php?r=keyk&content_type=folders&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key="


def getFilesFromFolder(idFolder):
    filelink = apifiles + str(idFolder) + "&response_format=json"
    rlinks = sesion.get(filelink, headers=headers)
    apijson = json.loads(rlinks.text)
    try:
        if not apijson["response"]["folder_content"]["files"]:
            raise Exception
        for link in apijson["response"]["folder_content"]["files"]:
            dirlink = link["links"]["normal_download"]
            rgetdirect = sesion.get(dirlink, headers=headers)
            docdirect = BeautifulSoup(rgetdirect.text, "lxml")
            directlink = docdirect.find("a", {"aria-label": "Download file"})["href"]
            print(directlink)
    except:
        pass


ids_folder = []
for link in rawlinks.splitlines():
    if "mediafire.com/folder" in link:
        ids_folder.append(link.strip().split("folder/")[1].split("/")[0])

# getting links from api json
for idf in ids_folder:
    getFilesFromFolder(idf)

    # detecting subdirectory
    folderlink = apifolders + str(idf) + "&response_format=json"
    flinks = sesion.get(folderlink, headers=headers)
    apisubfjson = json.loads(flinks.text)
    try:
        if not apisubfjson["response"]["folder_content"]["folders"]:
            raise Exception
        for subflink in apisubfjson["response"]["folder_content"]["folders"]:
            subfdirlink = subflink["folderkey"]
            subfname = subflink["name"]
            print("Subfolder: " + subfname)
            try:
                getFilesFromFolder(subfdirlink)
            except:
                pass
    except:
        print("No se encontraron folders, link de carpeta vacio?")
