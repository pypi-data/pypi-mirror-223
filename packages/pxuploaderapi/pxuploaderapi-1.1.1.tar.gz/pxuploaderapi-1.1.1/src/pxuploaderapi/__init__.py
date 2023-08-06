import pickle
import datetime
import os

class EcommerceUploaderAPI:
    def __init__(self, path):
        self.path = path
        # Get the uploader object from the path
        with open(self.path, "rb") as f:
            self.uploader_dict = pickle.load(f)

    def getName(self) -> str:
        return self.getUploader()["name"]
    
    def getUUID(self) -> str:
        return self.getUploader()["uuid"]
    
    def getTesting(self) -> bool:
        return self.getUploader()["testing"]
    
    def getFields(self) -> dict:
        return self.getUploader()["fields"]

    def getUploader(self) -> dict:
        return self.uploader_dict
    
    def getTestOptions(self) -> dict:
        return self.getUploader()["test_options"]
    
    def getDeployOptions(self) -> dict:
        return self.getUploader()["deploy_options"]
    
    def getGithubOptions(self) -> dict:
        return self.getUploader()["github_options"]
    
    
    

class ScoreAPI:
    def __init__(self, path_to_installation):
        self.score_file = os.path.join(path_to_installation, "bin", "scores.bin")
        # score_dict maps uuid to (successes, partial, failure, date)
        try:
            self.getScores()
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find scores file at {self.score_file}. Ensure you have entered the correct path to the installation and that you are using the latest version of the Uploader Hub.")

    def getScores(self) -> dict:
        with open(self.score_file, "rb") as f:
            score_dict = pickle.load(f)
        return score_dict
    
    def writeToFile(self, score_dict):
        with open(self.score_file, "wb") as f:
            pickle.dump(score_dict, f) 

    def setUpScore(self, uuid):
        # If it's a new day, or if the uuid hasn't existed, reset the score.
        score_dict = self.getScores()
        if self.getDate(uuid) != datetime.datetime.now().date() or uuid not in self.getScores():
            score_dict[uuid] = (0, 0, 0, datetime.datetime.now().date())
            self.writeToFile(score_dict)
    
    def getScore(self, uuid) -> (int, int, int, datetime.date):
        self.setUpScore(uuid)
        return self.getScores()[uuid]
    
    def getSuccesses(self, uuid) -> int:
        return self.getScore(uuid)[0]
    
    def getPartial(self, uuid) -> int:
        return self.getScore(uuid)[1]
    
    def getFailures(self, uuid) -> int:
        return self.getScore(uuid)[2]
    
    def getDate(self, uuid) -> datetime.date:
        return self.getScore(uuid)[3]
    
    def scoreSuccess(self, uuid):
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses() + 1, self.getPartial(), self.getFailures(), self.getDate())
        self.writeToFile()

    def scorePartial(self, uuid):
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses(), self.getPartial() + 1, self.getFailures(), self.getDate())
        self.writeToFile()

    def scoreFailed(self, uuid):
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses(), self.getPartial(), self.getFailures() + 1, self.getDate())
        self.writeToFile()

      


        