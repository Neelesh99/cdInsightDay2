from enum import Enum
from random import random


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
        if self.stats.populationSize == 0:
            return 0
        return self.stats.economy / self.stats.populationSize

class MedCity(City):

    name = "CoolCity"

    def turnAction(self):
        if self.stats.populationSize < 5:
            return Actions.FARM
        elif random() < .2:
            return Actions.MINE
        else:
            return Actions.TRADE


class Game:
    cities = []
    baseMine = 10
    baseFarm = 10
    miningProb = 0.5
    miningRecursion = 0.1
    baseProb = 0.5
    farmingReward = 5

    def __init__(self, baseMine=10, baseFarm=10, miningProb=0.5, miningRecursion=0.1, farmingReward=5):
        self.baseMine = baseMine
        self.baseFarm = baseFarm
        self.miningProb = miningProb
        self.miningRecursion = miningRecursion
        self.baseProb = miningProb
        self.farmingReward = farmingReward

    def addCity(self, city):
        self.cities.append(city)

    def scrubCities(self):
        self.cities = []

    def startGame(self, turns: int):
        for turn in range(turns):
            self.runTurn()
        results = []
        for city in self.cities:
            results.append(city.calculateScore())
        return results

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
                reward = self.handleMining(mineCount, city)
                city.adjustEconomy(reward)
                if reward < 0:
                    city.adjustPopulationSize(-1)
            if actions[city.name] == Actions.FARM:
                city.adjustPopulationSize(self.handleFarming(farmCount))
                city.adjustEconomy(self.farmingReward)
            if actions[city.name] == Actions.TRADE:
                city.adjustEconomy(self.handleTrading(self.skimTradeCity(oldCities, city.name), city))


    def skimTradeCity(self, oldList, cityName):
        newList = []
        for city in oldList:
            if city.name != cityName:
                newList.append(city)
        return newList

    def handleMining(self, count, city):
        if random() < self.miningProb:
            self.miningProb = self.baseProb
            return -1 * city.stats.populationSize
        else:
            self.miningProb += self.miningRecursion
            return (self.baseMine / count) * city.stats.populationSize

    def handleFarming(self, count):
        return self.baseFarm / count

    def handleTrading(self, oldCityStats, tradingCity):
        accEconomy = 0
        for city in oldCityStats:
            accEconomy += city.stats.economy
        avg = accEconomy / len(oldCityStats)
        return avg - tradingCity.stats.economy

class RunGame:

    cities = None
    def __init__(self, cities):
        self.cities = cities

    def runFull(self, iterations):
        scores = []
        for city in self.cities:
            scores.append([])
        for i in range(iterations):
            res = self.runSingle()
            for j in range(len(self.cities)):
                scores[j].append(res[j])
        for elem in scores:
            print(sum(elem) / len(elem))


    def runSingle(self):
        game = Game(10, 1, 0.1, 0.05)
        game.scrubCities()
        for i in range(len(self.cities)):
            game.addCity(self.cities[i]())
        return game.startGame(10)

cities = [City, City, MedCity]

runner = RunGame(cities)
runner.runFull(1000)