import asyncio
import logging
import json
import copy

from config import Config


async def init():
    old_languages = None
    old_translates = None

    old_prices = None

    old_user_lang = None

    old_admins = None
    old_questions = None

    old_answers = None

    old_pays = None

    old_pre_questions = None

    old_pay_lang = None


    
    while True:
        
        if Config.languages != old_languages:
            old_languages = copy.deepcopy(Config.languages)
            with open("cache/languages.json", "w", encoding="utf-8") as f:
                json.dump(old_languages, f, ensure_ascii=False, indent=2)
        
        if Config.translates != old_translates:
            old_translates = copy.deepcopy(Config.translates)
            with open("cache/translates.json", "w", encoding="utf-8") as f:
                json.dump(old_translates, f, ensure_ascii=False, indent=2)


        
        if Config.prices != old_prices:
            old_prices = copy.deepcopy(Config.prices)
            with open("cache/prices.json", "w", encoding="utf-8") as f:
                json.dump(old_prices, f, ensure_ascii=False, indent=2)



        if Config.user_lang != old_user_lang:
            old_user_lang = copy.deepcopy(Config.user_lang)
            with open("cache/user_lang.json", "w", encoding="utf-8") as f:
                json.dump(old_user_lang, f, ensure_ascii=False, indent=2)



        if Config.admins != old_admins:
            old_admins = copy.deepcopy(Config.admins)
            with open("cache/admins.json", "w", encoding="utf-8") as f:
                json.dump(old_admins, f, ensure_ascii=False, indent=2)



        if Config.questions != old_questions:
            old_questions = copy.deepcopy(Config.questions)
            with open("cache/questions.json", "w", encoding="utf-8") as f:
                json.dump(old_questions, f, ensure_ascii=False, indent=2)



        if Config.answers != old_answers:
            old_answers = copy.deepcopy(Config.answers)
            with open("cache/answers.json", "w", encoding="utf-8") as f:
                json.dump(old_answers, f, ensure_ascii=False, indent=2)



        if Config.pays != old_pays:
            old_pays = copy.deepcopy(Config.pays)
            with open("cache/pays.json", "w", encoding="utf-8") as f:
                json.dump(old_pays, f, ensure_ascii=False, indent=2)



        if Config.pre_questions != old_pre_questions:
            old_pre_questions = copy.deepcopy(Config.pre_questions)
            with open("cache/pre_questions.json", "w", encoding="utf-8") as f:
                json.dump(old_pre_questions, f, ensure_ascii=False, indent=2)



        if Config.pay_lang != old_pay_lang:
            old_pay_lang = copy.deepcopy(Config.pay_lang)
            with open("cache/pay_lang.json", "w", encoding="utf-8") as f:
                json.dump(old_pay_lang, f, ensure_ascii=False, indent=2)





        await asyncio.sleep(5)
