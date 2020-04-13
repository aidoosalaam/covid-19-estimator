class Impact(object):
    __currentlyInfected = 0
    __projected_infections = 0

    def __init__(self, data):
        if data is not None:
            self.periodType = data["periodType"]
            self.timeToElapse = data["timeToElapse"]
            self.reportedCases = data["reportedCases"]
            self.population = data["population"]
            self.totalHospitalBeds = data["totalHospitalBeds"]

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

    def hospitalBedsByRequestedTime(self,totalHospitalBeds):
        severeCasesByRequestedTime = 0.15 * self.infectionByRequestedTime()
        available_beds = totalHospitalBeds - severeCasesByRequestedTime
        return available_beds


class SevereImpact(Impact):
    def covid19ImpactEstimator(self):
        self.__currentlyInfected = self.reportedCases * 50
        return self.__currentlyInfected

    def infectionByRequestedTime(self):
        self.covid19ImpactEstimator()
        power = self.timeToElapse//3
        self.__projected_infections = self.__currentlyInfected * (2**power)
        return self.__projected_infections


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
    print ("impact: " , impact.infectionByRequestedTime(),
    "\nSevereImpact: " , severe_impact.infectionByRequestedTime())
