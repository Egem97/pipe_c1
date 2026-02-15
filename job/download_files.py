from playwright.sync_api import sync_playwright
import time
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()



def download_files_c1(mes):
    print("Ejecutando Playwright en modo headless...")
    
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=['--start-maximized']
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
  
        download_url = None
        
        def handle_download(download):
            nonlocal download_url
            download_url = download.url
            print(f"URL de descarga capturada: {download_url}")
        
        page.on("download", handle_download)

        print("🔐 Navegando a página de login...")
        page.goto(os.getenv("WEB"))
        
        print("Llenando formulario de login...")

        page.fill('xpath=//input[@name="login"]', os.getenv("USER"))
        page.fill('xpath=//input[@name="password"]', os.getenv("PASSWORD"))
        print("Haciendo click en login...")
        page.click('xpath=//html/body/div/main/div/form/div[3]/button')

        print("⏳ Esperando que cargue la página...")
        
        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a").click()

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[7]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[7]/a").click()
        ##INGRESAR VALOR AL SELECT
        #mes = "Feb"
        page.wait_for_selector("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()
        time.sleep(5)  

        #RUTA DE DESCARGA
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        download_folder = os.path.join(base_path, "data", "download")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        
        file_name = f"Detalle_nino_{mes}.xls"
        save_path = os.path.join(download_folder, file_name)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path}")
        with page.expect_download(timeout=900000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/header/button[2]").click()
                                #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path)
        print(f"💾 Archivo guardado exitosamente en: {save_path}")

        ######################## SIGUIENTE ARCHIVO VD CHILS
        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a").click()

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[6]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[6]/a").click()
        ####
        page.wait_for_selector("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()

        file_name_vd = f"Reporte_actividades_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=900000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/header/button[2]").click()
                                #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")
        ############################ GESTANTES CARGA

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a").click()

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[14]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[14]/a").click()

        page.wait_for_selector("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()

        file_name_vd = f"Detalle_madre_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=900000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/header/button[2]").click()
                                #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")
        ############################ GESTANTES DESCARGA VD

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/a").click()

        page.wait_for_selector("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[13]/a", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[11]/ul/li[13]/a").click()

        page.wait_for_selector("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()

        file_name_vd = f"Reporte_actividades_madres_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=900000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div[2]/div/div/header/button[2]").click()
                                #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")
       





