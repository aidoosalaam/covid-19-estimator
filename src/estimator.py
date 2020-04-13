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
        self.__currentlyInfected = self.reportedCases * 10
        return self.__currentlyInfected

    def infectionByRequestedTime(self):
        self.periodType = self.periodType.lower()
        if self.periodType == "w":
            self.timeToElapse = self.timeToElapse * 7
        elif self.periodType == "m":
            self.timeToElapse = self.timeToElapse * 30
        else:
            self.timeToElapse = self.timeToElapse

        self.covid19ImpactEstimator()
        power = self.timeToElapse//3
        self.__projected_infections = self.__currentlyInfected * (2**power)
        return self.__projected_infections

    def severeCasesByRequestedTime(self):
        self.__severeCasesByRequestedTime = 0.15 * self.infectionByRequestedTime()
        return self.__severeCasesByRequestedTime

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = (0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime()
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = 0.05 * self.infectionByRequestedTime()
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = 0.02 * self.infectionByRequestedTime()
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = int((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse)
        return dollarsInFlight


class SevereImpact(Impact):
    def covid19ImpactEstimator(self):
        self.__currentlyInfected = self.reportedCases * 50
        return self.__currentlyInfected

    def infectionByRequestedTime(self):
        self.covid19ImpactEstimator()
        power = self.timeToElapse//3
        self.__projected_infections = self.__currentlyInfected * (2**power)
        return self.__projected_infections

    def severeCasesByRequestedTime(self):
        self.__severeCasesByRequestedTime = 0.15 * self.infectionByRequestedTime()
        return self.__severeCasesByRequestedTime

    def availableHospitalBedsByRequestedTime(self):
        hospitalBedsByRequestedTime = (0.35 * self.totalHospitalBeds) - self.severeCasesByRequestedTime()
        return hospitalBedsByRequestedTime

    def casesForICUByRequestedTime(self):
        casesForICUByRequestedTime = 0.05 * self.infectionByRequestedTime()
        return casesForICUByRequestedTime

    def casesForVentilatorsByRequestedTime(self):
        casesForVentilatorsByRequestedTime = 0.02 * self.infectionByRequestedTime()
        return casesForVentilatorsByRequestedTime

    def dollarsInFlight(self):
        dollarsInFlight = int((self.infectionByRequestedTime() * self.region_avgDailyIncomePopulation * self.region_avgDailyIncomeInUSD)// self.timeToElapse)
        return dollarsInFlight




def result_toJson(data):
    import json
    impact = Impact(data)
    severe_impact = SevereImpact(data)

    data = {
        "data" : data,
        "Impact":{
            "currentlyInfected" : impact.infectionByRequestedTime(),
            "severeCasesByRequestedTime" : impact.severeCasesByRequestedTime(),
            "hospitalBedsByRequestedTime" : impact.availableHospitalBedsByRequestedTime(),
            "casesForICUByRequestedTime" : impact.casesForICUByRequestedTime(),
            "casesForVentilatorsByRequestedTime" : impact.casesForVentilatorsByRequestedTime(),
            "dollarsInFlight" : impact.dollarsInFlight()
        },
        "SevereImpact":{
            "currentlyInfected" : severe_impact.infectionByRequestedTime(),
            "severeCasesByRequestedTime" : severe_impact.severeCasesByRequestedTime(),
            "hospitalBedsByRequestedTime" : severe_impact.availableHospitalBedsByRequestedTime(),
            "casesForICUByRequestedTime" : severe_impact.casesForICUByRequestedTime(),
            "casesForVentilatorsByRequestedTime" : severe_impact.casesForVentilatorsByRequestedTime(),
            "dollarsInFlight" : severe_impact.dollarsInFlight()
        }
    }
    # convert into JSON:
    data = json.dumps(data)
    return data

def result_toXml(data):
    from dicttoxml import dicttoxml
    impact = Impact(data)
    severe_impact = SevereImpact(data)

    data = {
        "data" : data,
        "Impact":{
            "currentlyInfected" : impact.infectionByRequestedTime(),
            "severeCasesByRequestedTime" : impact.severeCasesByRequestedTime(),
            "hospitalBedsByRequestedTime" : impact.availableHospitalBedsByRequestedTime(),
            "casesForICUByRequestedTime" : impact.casesForICUByRequestedTime(),
            "casesForVentilatorsByRequestedTime" : impact.casesForVentilatorsByRequestedTime(),
            "dollarsInFlight" : impact.dollarsInFlight()
        },
        "SevereImpact":{
            "currentlyInfected" : severe_impact.infectionByRequestedTime(),
            "severeCasesByRequestedTime" : severe_impact.severeCasesByRequestedTime(),
            "hospitalBedsByRequestedTime" : severe_impact.availableHospitalBedsByRequestedTime(),
            "casesForICUByRequestedTime" : severe_impact.casesForICUByRequestedTime(),
            "casesForVentilatorsByRequestedTime" : severe_impact.casesForVentilatorsByRequestedTime(),
            "dollarsInFlight" : severe_impact.dollarsInFlight()
        }
    }
    # convert into Xml:
    data = dicttoxml(data)
    return data


class TestEstimator(unittest.TestCase):
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
    
    impact = Impact(data)

    def test_impactInfectionByRequestedTime(self):
        currentlyInfected = impact.infectionByRequestedTime()
        self.assertEqual(currentlyInfected,200)

    def test_impactSevereCasesByRequestedTime(self):
        severCasesByRequestedTime = impact.severeCasesByRequestedTime()
        self.assertEqual(severCasesByRequestedTime, 3345454)

    if __name__ == "__main__":
        unittest.main()
    



if __name__ == "__main__":
   
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

    impact = Impact(data)
    severe_impact = SevereImpact(data)
    # print (result_toXml(data))
    # print (result_toJson(data))
