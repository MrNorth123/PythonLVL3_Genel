import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import asyncio
import time
from datetime import datetime,timedelta

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.last_feed_time = datetime.now
        self.hunger = 100   # 100 ise aç , 0 ise tok
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
        if pokemon_trainer in Pokemon.pokemons:
            old = Pokemon.pokemons[pokemon_trainer]
            self.name = old.name
            self.pokemon_number = old.pokemon_number
            self.hunger = old.hunger
        else:
            Pokemon.pokemons[pokemon_trainer] = self


    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür



    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  
        return f"""Pokémonun ismi: {self.name}
                Pokemonun açlığı: {self.hunger}
                Pokemonun gücü: {self.power}
                Pokemonun canı: {self.hp}"""
    
    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
               if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    img_url = data["sprites"]["front_default"]
                    return img_url
               else:
                   return None
               
    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {self.last_feed_time+delta_time}"           

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1,3)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

class Wizard(Pokemon):
    def feed(self):
        return super().feed(feed_interval=10)
    

class Fighter(Pokemon):
    async def attack(self,enemy):
        super_power = random.randint(5,15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
    def feed(self):
        return super().feed(feed_interval=20)
    
"""‼️TEST‼️
async def main():
    wizard = Wizard("deniz")
    fighter= Fighter("kuzey")

    print(await wizard.info())
    print("#" * 10)
    print(await fighter.info())
    print("#" * 10)
    print(await wizard.attack(fighter))
    print(await fighter.attack(wizard))

# Asenkron main fonksiyonunu çalıştırıyoruz
asyncio.run(main()) """
