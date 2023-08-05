class PlayerError(Exception):
    pass


class GameF:
    def __init__(self, name, height=100, width=100):
        self.height = height
        self.width = width
        self.player_ = []
        self.door_ = True
        self.name = name
        self.weather_ = 'sunny'
        self.money_ = {}

        class door:
            def __init__(self):
                self.door_ = True

            def open(self):
                self.door_ = True

            def close(self):
                self.door_ = False

        self.door = door()

        class player:
            def __init__(self):
                self.player_ = []
                self.door_ = True

            def add(self, name: str):
                if self.door_ == True:
                    self.player_.append(name)
                else:
                    raise PlayerError(f'You can\'t add {name} to our island because the door is closed.')

            def delete(self, name: str):
                if not name in self.player_:
                    raise PlayerError('We have no this player')
                if self.door_ == True:
                    self.player_.remove(name)
                else:
                    raise PlayerError(f'You can\'t remove {name} because the door is closed.')

            def remove_to(self, name: str, island):
                if not name in self.player_:
                    raise PlayerError('We have no this player')
                if self.door_ == True and island.door_ == True:
                    island.player_.append(name)
                    self.player_.remove(name)
                else:
                    raise PlayerError(f'You can\'t remove {name} to {island.name} because the door is closed.')
                island.player.player_ = island.player_

        self.player = player()

        class weather:
            def __init__(self):
                self.weather_ = 'sunny'

                class set:
                    def __init__(self):
                        self.weather_ = 'sunny'

                    def sunny(self):
                        self.weather_ = 'sunny'

                    def cloudy(self):
                        self.weather_ = 'cloudy'

                    def rainy(self):
                        self.weather_ = 'rainy'

                self.set = set()

                def random(self):
                    import random
                    r = random.randint(1, 3)
                    if r == 1:
                        self.weather_ = 'sunny'
                    elif r == 2:
                        self.weather_ = 'cloudy'
                    elif r == 3:
                        self.weather_ = 'rainy'

        class money:
            def __init__(self):
                self.player_ = []
                self.money_ = {}

            def init(self, money=100):
                for i in self.player_:
                    self.money_[i] = money

            def add(self, name, money):
                if not name in self.player_:
                    raise PlayerError('We have no this player')
                self.money_[name] += money

            def minus(self, name, money):
                if not name in self.player_:
                    raise PlayerError('We have no this player')
                self.money_[name] -= money

        self.money = money()
        self.weather = weather()

    def flushed(self):
        self.door_ = self.door.door_
        self.player_ = self.player.player_
        self.weather.weather_ = self.weather.set.weather_
        self.weather_ = self.weather.weather_
        self.player.door_ = self.door_
        self.money.player_ = self.player_
        self.money_ = self.money.money_

    def destroy_self(self):
        del self
