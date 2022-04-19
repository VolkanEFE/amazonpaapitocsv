import os
import json
import time
import csv
import textwrap
from pathlib import Path
from amazon_paapi import AmazonApi 

if os.path.exists('asins.csv'):
    os.remove('asins.csv')

datas = []

with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"usa.json", encoding="utf-8") as config_file:
    config = json.load(config_file)

    amazon = AmazonApi(config['API_KEY'],config['SECRET_KEY'],config['AFFILIATE_ID'],config['COUNTRY'])

    
    listeler = [
#ASIN LIST
'B08LHCVNZG','B0722PN5PQ','B09NSWJ6XB','B09K5QW33J','B08QF1V3XN','B08X5ZP5KR','B01I1TSB0M','B095H1CTH8','B07JMC36Q2','B07FTCC75Y','B09P1VDGG6','B08LB6RZJW'

    ]
    

    chunked_list = list()
    chunk_size = 10

    for i in range(0, len(listeler), chunk_size):
        chunked_list.append(listeler[i:i+chunk_size])
        try:
            for ch_liste in chunked_list:
                products = amazon.get_items(ch_liste)
                for product in products:    
                    try:
                        kucukResimler = []   
                        baslik = product.item_info.title._display_value
                        liste = product.item_info._features.display_values
                        resim = product.images.primary.large.url
                        resimler = product.images.variants
                        for resim1 in resimler:
                            kucukResimler.append(resim1.large.url)
                        link = product.detail_page_url
                        icerik = ','.join(liste)
                        etiket = product.item_info._classifications.product_group.display_value
                            
                        datas.append([baslik, icerik, link, etiket, resim, 
                        kucukResimler[0],
                        kucukResimler[1],
                        kucukResimler[2],
                        kucukResimler[3],
                        kucukResimler[4]
                        ])

                    except:
                        continue
                time.sleep(5)
        except:
            continue

    with open('asins.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        for data in datas:
            writer.writerow(data)

f = open('asins.txt', 'r+')
f.truncate(0)
            