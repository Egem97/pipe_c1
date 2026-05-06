from playwright.sync_api import sync_playwright
import time
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

def download_files_vd(mes):
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
        page.wait_for_load_state("networkidle", timeout=60000)

        print("Llenando formulario de login...")

        try:
            page.wait_for_selector(
                'xpath=//html/body/div[1]/main/div[1]/form/div[1]/input',
                timeout=60000,
            )
        except Exception:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            debug_dir = os.path.join(base_path, "data", "debug")
            os.makedirs(debug_dir, exist_ok=True)
            page.screenshot(path=os.path.join(debug_dir, "login_timeout.png"), full_page=True)
            with open(os.path.join(debug_dir, "login_timeout.html"), "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"Login form no apareció. URL actual: {page.url} | Title: {page.title()}")
            raise

        page.fill('xpath=//html/body/div[1]/main/div[1]/form/div[1]/input', os.getenv("APP_USER") or os.getenv("USER"))
        page.fill('xpath=//html/body/div[1]/main/div[1]/form/div[2]/input', os.getenv("PASSWORD"))
        print("Haciendo click en login...")
        page.click('xpath=//html/body/div[1]/main/div[1]/form/div[3]/button')

        print("⏳ Esperando que cargue la página...")
        NAVEGADOR_DESCARGAS = '//html/body/header/nav/div[3]/button[9]/span'
        page.wait_for_selector(f"xpath={NAVEGADOR_DESCARGAS}", timeout=100000)
        time.sleep(1)  
        page.locator(f"xpath={NAVEGADOR_DESCARGAS}").click()
        
        ##DETALLE DE NIÑO 
        page.wait_for_selector("xpath=//html/body/div[2]/div[1]/div[1]/div/a[3]", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/div[2]/div[1]/div[1]/div/a[3]").click()
         
        
        ##INGRESAR VALOR AL SELECT
        SELECTOR_MES = '//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select'
        page.wait_for_selector(f"xpath={SELECTOR_MES}", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator(f"xpath={SELECTOR_MES}")
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
        with page.expect_download(timeout=120000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[1]/div/button[2]").click()
                               
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path)
        print(f"💾 Archivo guardado exitosamente en: {save_path}") 
    #######################################################################
    
        page.wait_for_selector(f"xpath={NAVEGADOR_DESCARGAS}", timeout=100000)
        time.sleep(1)  
        page.locator(f"xpath={NAVEGADOR_DESCARGAS}").click()   
        ##REPORTE DE ACTIVIDAD
        page.wait_for_selector("xpath=//html/body/div[2]/div[1]/div[1]/div/a[2]", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/div[2]/div[1]/div[1]/div/a[2]").click()
        ##INGRESAR VALOR AL SELECT
        SELECTOR_MES = '//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select'
        page.wait_for_selector(f"xpath={SELECTOR_MES}", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator(f"xpath={SELECTOR_MES}")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()
        time.sleep(5) 
        
        file_name_vd = f"Reporte_actividades_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=120000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[1]/div/button[2]").click()
                                    #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")   
        
        ############################ GESTANTES CARGA
        page.wait_for_selector(f"xpath={NAVEGADOR_DESCARGAS}", timeout=100000)
        time.sleep(1)  
        page.locator(f"xpath={NAVEGADOR_DESCARGAS}").click()   
        ##DETALLE GESTANTES
        page.wait_for_selector("xpath=//html/body/div[2]/div[1]/div[1]/div/a[8]", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/div[2]/div[1]/div[1]/div/a[8]").click()
        ##
        page.wait_for_selector("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()
        
        file_name_vd = f"Detalle_madre_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=120000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[1]/div/button[2]").click()
                                    #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")
        
        ##############################################################GESTANTES DESCARGA VD
        page.wait_for_selector(f"xpath={NAVEGADOR_DESCARGAS}", timeout=100000)
        time.sleep(1)  
        page.locator(f"xpath={NAVEGADOR_DESCARGAS}").click()   
        ##REPORTE DE ACTIVIDAD GESTANTES
        page.wait_for_selector("xpath=//html/body/div[2]/div[1]/div[1]/div/a[7]", timeout=100000)
        time.sleep(1)  
        page.locator("xpath=//html/body/div[2]/div[1]/div[1]/div/a[7]").click()
        
        page.wait_for_selector("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select", timeout=100000)
        time.sleep(1) 
        select_value_mes = page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/select")
        select_value_mes.select_option(label=mes)
        select_value_mes.click()
        
        file_name_vd = f"Reporte_actividades_madres_{mes}.xls"
        save_path_vd = os.path.join(download_folder, file_name_vd)
        print(f"⬇️ Iniciando descarga... Esperando archivo: {save_path_vd}")
        with page.expect_download(timeout=120000) as download_info:
            page.locator("xpath=//html/body/div[1]/div/div/div[2]/div/div/div[1]/div/button[2]").click()
                                    #/html/body/div[1]/div/div[2]/div/div/header/button[2]
        download = download_info.value
        print(f"✅ Descarga detectada: {download.suggested_filename}")
        download.save_as(save_path_vd)
        print(f"💾 Archivo guardado exitosamente en: {save_path_vd}")
        
