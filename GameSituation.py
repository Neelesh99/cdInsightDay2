from enum import Enum


class Actions(Enum):
    MINE = 1,
    FARM = 2,
    TRADE = 3


class CityStats:
    populationSize = 1
    economy = 1

    def __init__(self):
        pass

    def getPopulationSize(self):
        return self.populationSize


class City:

    stats = None
    name = "Default"

    def __init__(self):
        self.stats = CityStats()

    def turnAction(self):
        return Actions.MINE

    def adjustPopulationSize(self, delta):
        self.stats.populationSize += delta

    def adjustEconomy(self, delta):
        self.stats.economy += delta

    def calculateScore(self):
        return self.stats.economy / self.stats.populationSize


class Game:
    cities = []
    baseMine = 10
    baseFarm = 10

    def __init__(self, baseMine=10, baseFarm=10):
        self.baseMine = baseMine
        self.baseFarm = baseFarm

    def addCity(self, city):
        self.cities.append(city)

    def startGame(self, turns: int):
        for turn in range(turns):
            self.runTurn()
        for city in self.cities:
            print(city.calculateScore())

    def runTurn(self):
        actions = {}
        mineCount = 0
        farmCount = 0
        for city in self.cities:
            action = city.turnAction()
            actions[city.name] = action
            if action == Actions.MINE:
                mineCount += 1
            if action == Actions.FARM:
                farmCount += 1
        oldCities = self.cities.copy()
        for city in self.cities:
            if actions[city.name] == Actions.MINE:
                city.adjustEconomy(self.handleMining(mineCount, city))
            if actions[city.name] == Actions.FARM:
                city.adjustPopulationSize(self.handleFarming(farmCount))
            if actions[city.name] == Actions.TRADE:
                city.adjustEconomy(self.handleTrading(self.skimTradeCity(oldCities, city.name), city))


    def skimTradeCity(self, oldList, cityName):
        newList = []
        for city in oldList:
            if city.name != cityName:
                newList = newList.append(city)
        return newList

    def handleMining(self, count, city):
        return (self.baseMine / count) * city.stats.populationSize

    def handleFarming(self, count):
        return self.baseFarm / count

    def handleTrading(self, oldCityStats, tradingCity):
        accEconomy = 0
        for city in oldCityStats:
            accEconomy += city.stats.economy
        avg = accEconomy / len(oldCityStats)
        return avg - tradingCity.stats.economy


game = Game(10,10)
game.addCity(City())
game.addCity(City())
game.startGame(5)