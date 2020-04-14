import math
import unittest

class Impact(object):
    __currentlyInfected = 0
    __projected_infections = 0
    __severeCasesByRequestedTime = 0
    __data = {}

    def __init__(self, data):
        if data is not None:
            self.data = data
            self.periodType = data["periodType"]
            self.timeToElapse = data["timeToElapse"]
            self.reportedCases = data["reportedCases"]
            self.population = data["population"]
            self.totalHospitalBeds = data["totalHospitalBeds"]
            self.region_name = data["region"]["name"]
            self.region_avgAge = data["region"]["avgAge"]
            self.region_avgDailyIncomeInUSD = data["region"]["avgDailyIncomeInUSD"]
            self.region_avgDailyIncomePopulation = data["region"]["avgDailyIncomePopulation"]

    def covid19ImpactEstimator(self):
        self.__currentlyInfected = math.trunc(math.trunc(self.reportedCases * 10))
        return self.__currentlyInfected

    def infectionByRequestedTime(self):
        self.periodType = self.periodType.lower()
        if self.periodType == "weeks":
            self.timeToElapse = self.timeToElapse * 7
        elif self.periodType == "months":
            self.timeToElapse = self.timeToElapse * 30
        else:
            self.timeToElapse = self.timeToElapse

        self.covid19ImpactEstimator()
        power = self.timeToElapse//3
        self.__projected_infections = math.trunc(self.__currentlyInfected * (2**power))
        return self.__projected_infections

    def severeCasesByRequestedTime(self):
        self.__severeCasesByRequestedTime = math.trunc(0.15 * self.infectionByRequestedTime())
        return self.__severeCasesByRequestedTime

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = math.trunc((0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime())
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = math.trunc(0.05 * self.infectionByRequestedTime())
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = math.trunc(0.02 * self.infectionByRequestedTime())
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = math.trunc(int((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse))
        return dollarsInFlight

class SevereImpact(Impact):
    def covid19ImpactEstimator(self):
        self.__currentlyInfected = math.trunc(self.reportedCases * 50)
        return self.__currentlyInfected

    def infectionByRequestedTime(self):
        self.covid19ImpactEstimator()
        power = self.timeToElapse//3
        self.__projected_infections = math.trunc(self.__currentlyInfected * (2**power))
        return self.__projected_infections

    def severeCasesByRequestedTime(self):
        self.__severeCasesByRequestedTime = math.trunc(0.15 * self.infectionByRequestedTime())
        return self.__severeCasesByRequestedTime

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = math.trunc((0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime())
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = math.trunc(0.05 * self.infectionByRequestedTime())
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = math.trunc(0.02 * self.infectionByRequestedTime())
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = math.trunc(int((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse))
        return dollarsInFlight

class TestEstimator(unittest.TestCase):
   
    def test_impactInfectionByRequestedTime(self):
        data = {
                "region": {
                        "name": "Africa",
                        "avgAge": 19.7,
                        "avgDailyIncomeInUSD": 5,
                        "avgDailyIncomePopulation": 0.71
                },
                "periodType": "days",
                "timeToElapse": 58,
                "reportedCases": 674,
                "population": 66622705,
                "totalHospitalBeds": 1380614
        }

        severImpact = SevereImpact(data)
        currentlyInfected = severImpact.infectionByRequestedTime()
        self.assertEqual(currentlyInfected,200)

    def test_impactSevereCasesByRequestedTime(self):
        data = {
                "region": {
                        "name": "Africa",
                        "avgAge": 19.7,
                        "avgDailyIncomeInUSD": 5,
                        "avgDailyIncomePopulation": 0.71
                },
                "periodType": "days",
                "timeToElapse": 58,
                "reportedCases": 674,
                "population": 66622705,
                "totalHospitalBeds": 1380614
        }

        severImpact = SevereImpact(data)
        severCasesByRequestedTime = severImpact.severeCasesByRequestedTime()
        self.assertEqual(severCasesByRequestedTime, 3345454)



# if __name__ == "__main__":
   
#     data = {
#                 "region": {
#                         "name": "Africa",
#                         "avgAge": 19.7,
#                         "avgDailyIncomeInUSD": 5,
#                         "avgDailyIncomePopulation": 0.71
#                 },
#                 "periodType": "days",
#                 "timeToElapse": 58,
#                 "reportedCases": 674,
#                 "population": 66622705,
#                 "totalHospitalBeds": 1380614
#             }

#     impact = Impact(data)
#     severe_impact = SevereImpact(data)
#     # print (result_toXml(data))
#     # print (result_toJson(data))
