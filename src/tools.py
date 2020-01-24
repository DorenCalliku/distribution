# roads: https://en.wikipedia.org/wiki/List_of_highways_in_Turkey
roads = ["Edirne – Lüleburgaz – İstanbul – Gebze – Kocaeli – Sakarya – Düzce – Bolu – Gerede – Ilgaz – Merzifon – Amasya – Niksar – Erzincan – Erzurum – Ağrı",
"Çanakkale – Bandırma – Bursa – Eskişehir – Sivrihisar – Ankara – Kırıkkale – Yozgat - Sivas – Erzincan",
"Çeşme - İzmir – Salihli – Uşak – Afyonkarahisar – Akşehir – Konya – Aksaray – Nevşehir – Kayseri – Pınarbaşı – Gürün – Malatya – Elazığ – Bingöl – Muş – Bitlis – Van",
"Datça - Fethiye – Antalya – Alanya – Anamur – Mersin – Adana – Gaziantep – Şanlıurfa – Şırnak – Yüksekova - Esendere",
"Karasu – Akçakoca - Zonguldak – Çaycuma – Bartın – Cide – İnebolu – Ayancık – Sinop – Gerze-Bafra-Samsun – Çarşamba – Ünye – Fatsa – Ordu – Bulancak – Giresun – Tirebolu – Trabzon – Sürmene – Rize – Ardeşen – Hopa – Borçka – Şavşat – Ardahan - Çıldır – Arpaçay – Akçakale",
"Edirne – Çanakkale – Edremit – İzmir – Aydın – Muğla",
"Karasu – Sakarya – Bilecik – Kütahya – Afyonkarahisar – Sandıklı – Burdur – Antalya",
"Zonguldak – Gerede – Ankara – Aksaray – Pozantı – Tarsus",
"Ünye – Tokat – Sivas – Malatya – Gaziantep – Kilis",
"Hopa – Artvin – Erzurum – Bingöl – Diyarbakır – Mardin",
#"Kaynarca-Karasu",
#"Edirne-Kırklareli-Pınarhisar-Vize-Saray-Istanbul-Şile-Kandıra-Kaynarca",
#"Devrek-Yenice-Karabük-Araç-Kastamonu-Taşköprü-Boyabat-Durağan-Vezirköprü-Havza-Ladik",
#"Köse-Bayburt-Aşkale-Dadaşköy",
#"Yalova-Karamürsel-Kandıra",
#"Orhangazi-İznik-Pamukova-Geyve-Taraklı",
#"Kestel-Yenişehir-Bilecik-Gölpazarı-Taraklı-Göynük-Bolu",
#"Taraklı-Göynük-Nallıhan",
#"Çanakkale-Çan",
#"Edremit-Havran-Balıkesir-Kepsut-Dursunbey-Harmancık-Tavşanlı-İnönü - Eskişehir",
#"Afyonkarahisar-Bayat-Sivrihisar-Polatlı-Haymana-Gölbaşı-Bala-Karakeçili-Kaman-Kırşehir-Mucur-Kayseri-Gemerek-Şarkışla-Ulaş-Ulaş-Kangal-Divriği-Arapgir-Keban-Elazığ"
]

def get_cities_in_main_roads():
    clean_roads = [each.replace(" - ", ",").replace(" – ",",").replace("-",",").split(',') 
               for each in roads ]
    return clean_roads