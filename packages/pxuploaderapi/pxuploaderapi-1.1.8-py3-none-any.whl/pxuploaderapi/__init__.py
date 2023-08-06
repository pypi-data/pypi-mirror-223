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
        uuid = str(uuid)
        if uuid not in score_dict or score_dict[uuid][3] != datetime.datetime.now().date():
            score_dict[uuid] = (0, 0, 0, datetime.datetime.now().date())
            self.writeToFile(score_dict)
    
    def getScore(self, uuid) -> (int, int, int, datetime.date):
        uuid = str(uuid)
        self.setUpScore(uuid)
        return self.getScores()[uuid]
    
    def getSuccesses(self, uuid) -> int:
        uuid = str(uuid)
        return self.getScore(uuid)[0]
    
    def getPartial(self, uuid) -> int:
        uuid = str(uuid)
        return self.getScore(uuid)[1]
    
    def getFailures(self, uuid) -> int:
        uuid = str(uuid)
        return self.getScore(uuid)[2]
    
    def getDate(self, uuid) -> datetime.date:
        uuid = str(uuid)
        return self.getScore(uuid)[3]
    
    def scoreSuccess(self, uuid):
        uuid = str(uuid)
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses(uuid) + 1, self.getPartial(uuid), self.getFailures(uuid), self.getDate(uuid))
        self.writeToFile(score_dict)

    def scorePartial(self, uuid):
        uuid = str(uuid)
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses(uuid), self.getPartial(uuid) + 1, self.getFailures(uuid), self.getDate(uuid))
        self.writeToFile(score_dict)

    def scoreFailed(self, uuid):
        uuid = str(uuid)
        self.setUpScore(uuid)
        score_dict = self.getScores()
        score_dict[uuid] = (self.getSuccesses(uuid), self.getPartial(uuid), self.getFailures(uuid) + 1, self.getDate(uuid))
        self.writeToFile(score_dict)

    def removeScore(self, uuid):
        uuid = str(uuid)
        score_dict = self.getScores()
        del score_dict[uuid]
        self.writeToFile(score_dict)
        

      


        