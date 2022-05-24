import configparser

# таблица соответствий букв общетюркского алфавита и татарской кирилицы
namefile_cfg = "cfg/cfg-alifba.cfg"


def get_alifbasi(namefile_cfg):
    """ наполнение словарей перевода одних букв в другие """
    with open(namefile_cfg, "r") as f:
        lines = f.readlines()

    common_turic_alifbasi_to_cyrilic_tatar = dict()  # из общетюркского алфавита в кирилический татарский
    cyrilic_tatar_to_common_turic_alifbasi = dict()  # из  кирилического татарского в общетюркский алфавит
    for line in lines:
        line = line.replace("\n", "")
        l = line.split("=")
        turk = l[0]
        cyrilic = l[1]
        if turk in common_turic_alifbasi_to_cyrilic_tatar:
            common_turic_alifbasi_to_cyrilic_tatar[turk] = "[{0}*{1}]".format(
                common_turic_alifbasi_to_cyrilic_tatar[turk], cyrilic)
        else:
            common_turic_alifbasi_to_cyrilic_tatar[turk] = cyrilic
        if cyrilic in cyrilic_tatar_to_common_turic_alifbasi:
            cyrilic_tatar_to_common_turic_alifbasi[cyrilic] = "[{0}*{1}]".format(
                cyrilic_tatar_to_common_turic_alifbasi[cyrilic], turk)
        else:
            cyrilic_tatar_to_common_turic_alifbasi[cyrilic] = turk
    return cyrilic_tatar_to_common_turic_alifbasi, common_turic_alifbasi_to_cyrilic_tatar
    # END наполнение словарей перевода одних букв в другие 


def isletter_k_g(sim):
    glas = ["к", "г"]
    if sim in glas:
        return True
    else:
        return False


# перевод из кирилицы в общетюркский алфавит
def translate_cyrilic_to_cta(original_text, cyrilic_tatar_to_common_turic_alifbasi):
    """ перевод из кирилицы в общетюркский алфавит
            original_text - текст который нужно перевести
            cyrilic_tatar_to_common_turic_alifbasi - 
     """

    translate_text = ""  # перевод текста
    # TODO: сначала надо отсканировать все сочетания символов которые по два или более символа.    
    for i in original_text:
        try:
            if i.isupper():
                sim = i.lower()
                if not isletter_k_g(sim):
                    translate_text += (cyrilic_tatar_to_common_turic_alifbasi[sim]).upper()
                else:
                    translate_text += i
            else:
                if not isletter_k_g(i):
                    translate_text += cyrilic_tatar_to_common_turic_alifbasi[i]
                else:
                    translate_text += i
        except KeyError:
            translate_text += i

    # print(translate_text)

    # обработка символов у которых два варианта (мягкий и твердый звук).
    soft_letter = ["ä", "ü", "i", "e", " "]  # мягкие гласные
    hard_letter = ["a", "o", "u", "ı"]  # твердые гласные
    glas = ["к", "г"]

    try:
        pos = translate_text.find("к")

        while pos != -1:
            if translate_text[pos + 1] in hard_letter:
                translate_text = translate_text[:pos] + "q" + translate_text[pos + 1:]
            else:
                translate_text = translate_text[:pos] + "k" + translate_text[pos + 1:]
            pos = translate_text.find("к")
    except IndexError:
        translate_text = translate_text[:pos] + "k"

    try:
        pos = translate_text.find("г")

        while pos != -1:
            if translate_text[pos + 1] in hard_letter:
                translate_text = translate_text[:pos] + "ğ" + translate_text[pos + 1:]
            else:
                translate_text = translate_text[:pos] + "g" + translate_text[pos + 1:]
            pos = translate_text.find("г")
    except IndexError:
        translate_text = translate_text[:pos] + "g"

    # END обработка символов у которых два варианта (мягкий и твердый звук).

    return translate_text


# END перевод из кирилицы в общетюркский алфавит


# перевод из общетюркского алфавита в кирилицу татарский
def translate_cta_to_cyrilic(original_text, cta_to_cyr_tat):
    """ перевод из кирилицы в общетюркский алфавит
            original_text - текст который нужно перевести
            cyrilic_tatar_to_common_turic_alifbasi - 
     """

    translate_text = ""  # перевод текста
    # TODO: сначала надо отсканировать все сочетания символов которые по два или более символа.
    # TODO: надо научиться помечать/обрабатывать смволы у которых может быть два варианта.,
    list_two_letter = list()
    for i in cta_to_cyr_tat:
        if len(i) > 1:
            list_two_letter.append(i)

            # print(list_two_letter)
    original_text_replace = original_text
    for i in list_two_letter:
        original_text_replace = original_text_replace.replace(i, cta_to_cyr_tat[i])
    # надо научиться помечать/обрабатывать смволы у которых может быть два варианта.,

    # print("original_text_replace: {}".format(original_text_replace))

    for i in original_text_replace:
        try:
            if i.isupper():
                sim = i.lower()
                translate_text += (cta_to_cyr_tat[sim]).upper()
            else:
                translate_text += cta_to_cyr_tat[i]
        except KeyError:
            translate_text += i
    return translate_text


# END перевод из общетюркского алфавита в кирилицу татарский

#     

cyr2cta, cta2cyr = get_alifbasi(namefile_cfg)

original_text = "Соңгы елларда себертатар теле белән гомумтатар әдәби телнең уртаклыгы телгә дә алынмаганлыктан, соңгы айларда Татарстан мәктәпләреннән ана телен кысрыклап чыгаруга бәйле вазгыять себертатарларның татар дөньясыннан аерылып чыгуын тәэмин итә, дигән уйны ныгытып өлгергән иде инде. Бәлки, нәкъ менә шушы вазгыять Төмәннең күренекле себертатар активистларын урыслашу ассимиляциясенә каршылык йөзеннән әдәби телгә йөз белән борылырга этәргәндер дә.Соңгы елларда себертатар теле белән гомумтатар әдәби телнең уртаклыгы телгә дә алынмаганлыктан, соңгы айларда Татарстан мәктәпләреннән ана телен кысрыклап чыгаруга бәйле вазгыять себертатарларның татар дөньясыннан аерылып чыгуын тәэмин итә, дигән уйны ныгытып өлгергән иде инде. Бәлки, нәкъ менә шушы вазгыять Төмәннең күренекле себертатар активистларын урыслашу ассимиляциясенә каршылык йөзеннән әдәби телгә йөз белән борылырга этәргәндер дә."

original_text2 = "гомумтатар казан к кызык.г"
print(original_text2)
text = translate_cyrilic_to_cta(original_text, cyr2cta)
print(text)

# org_text2 = "Tatar imlasın kamilläşterügä zur öleş kertkän ğälimnär arasında Äxmäthadi Maqsudiğa (1864-1941) ayırım tuqtalıp ütärgä bula. Äxmäthadi Maqsudinıñ 1892. yılda berençe tapqır dönya kürgän «Möğällime äwwäl» isemle älifbası ayıruça zur uñış qazana. Kitapnıñ utızdan artıq basması bar, ğömümi bastıru 1,200,000 danädän artıp kitä. ä.Maqsudinıñ bu älifbası buyınça Tatarlar ğına tügel, Üzbäklär, Qazaqlar, Qırğızlar, Qırım Tatarları häm başqa Törki xalıqlar da uqu-yazu nigezlären üzläştergännär."
# text2 =translate_cta_to_cyrilic(org_text2,cta2cyr)
# print(text2)
