from datetime import datetime
import pymongo
import pytz

class mongodb:
    def __init__(self, host):

        # ----------------Start Setup Data Base -------------------------------------------------------------------------------
        self.myclient = pymongo.MongoClient(f"mongodb://{host}/")
        self.dblist = self.myclient.list_database_names()

        if "UPCDB" in self.dblist:
            print("The UPC Database Exists.")
            self.mydb = self.myclient["UPCDB"]
            self.DB = self.mydb["UPC"]
        else:
            self.mydb = self.myclient["UPCDB"]
            self.DB = self.mydb["UPC"]
            print("Creating UPC Database")

        self.mydb = self.myclient["UPCDB"]
        self.DB = self.mydb["UPC"]

        print(f"Database's: {self.myclient.list_database_names()}")
        print(f"Collections's: {self.mydb.list_collection_names()}")

        # ----------------End Setup Data Base ----------------------------------------------------------------------------------



    def UpdateProduct(self, upc, name, available, price, url, timestamp, response):
        try:
            dict = {
                "upc": upc,"name": name,"salePrice": price, "available": available, "timestamp": timestamp,"vendor_url": url,"Response":response
            }
            x = self.DB.insert_one(dict)

            print(f"Added UPC: {upc} to database")
        except Exception as e:
            print(f"Update Product Error: {e} UPC: {upc}")


    def GetTimeStamp(self):
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        timezone = pytz.timezone("America/New_York")
        now = datetime.now()
        time = now.astimezone(timezone)
        return time.strftime(format)
