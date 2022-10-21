# coding: utf-8

import glob
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import shutil


def baixar_csv_ibovespa(url, text_bottom):
    driver = webdriver.Chrome()
    driver.maximize_window()
    sem_conexao = True

    while sem_conexao:
        try:
            driver.get(url)
            sem_conexao = False
        except:
            pass

    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        if link.get_property("textContent") == text_bottom:
            print('Clicou no botão para download')
            link.click()

        time.sleep(3)
    driver.quit()

    return


def pegar_arquivo_csv(diret, name_file_ibov_find, new_directory_files):
    filename_ibov = None

    files_directory = glob.glob(diret + "/*.csv")
    files_directory.sort(key=os.path.getmtime)

    for filename in reversed(files_directory):
        if filename.find(name_file_ibov_find) != -1:
            filename_ibov = filename
            break
        
    if (filename_ibov):
        filename_ibov = shutil.move(filename_ibov, new_directory_files)
    else:
        print('Arquivo "{}" não encontrado no diretório "{}".'.format(name_file_ibov_find, diret))

    return filename_ibov


def clean_file_ibov(path_file):
    lines_file = []
    last_line = 0
    with open(path_file, encoding='ISO-8859-1', mode='r') as fp:
        last_line = len(fp.readlines()) - 2

    with open(path_file, encoding='ISO-8859-1', mode='r') as f:
        for i, line in enumerate(f):
            if (i != 0 and i < last_line):
                if (str(line.strip())[-1] == ';'):
                    lines_file.append(str(line)[:-2].split(';'))
                else:
                    lines_file.append(line.split(';'))

    return lines_file


def read_file_ibov(path_file):
    df = pd.DataFrame(path_file, index=None)
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    print(df)


if __name__ == '__main__':
    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br'
    text_bottom = 'Download'
    old_directory_files = '/home/cayo/Downloads/'
    new_directory_files = './historico_ibov_diario/'
    name_file_ibov_find = 'IBOVDia'

    baixar_csv_ibovespa(url, text_bottom)

    file_ibov = pegar_arquivo_csv(old_directory_files, name_file_ibov_find, new_directory_files)

    if (file_ibov == None):
        print('Não foi possível encontrar o arquivo do ibovespa no diretório "{}".'.format(
            old_directory_files))
    else:
        read_file_ibov(clean_file_ibov(file_ibov))
