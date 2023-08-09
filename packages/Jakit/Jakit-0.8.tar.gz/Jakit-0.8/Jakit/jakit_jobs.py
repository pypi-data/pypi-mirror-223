# designed by: Idriss Animashaun
import pymongo
from bson.objectid import ObjectId
from Dager.dager_data import Database
import requests
import datetime

Dager_client = "mongodb://DaggerData_rw:eEsQcKvMgKfH5Di@p1ir1mon019.ger.corp.intel.com:7174,p2ir1mon019.ger.corp.intel.com:7174,p3ir1mon019.ger.corp.intel.com:7174/DaggerData?ssl=true&replicaSet=mongo7174"
Dager_conn = 'DaggerData'
Jobs_status_coll = 'Jobs'

ConnectionStringDager = pymongo.MongoClient(Dager_client)
DatabaseDager = ConnectionStringDager[Dager_conn]
CollectionJobs = DatabaseDager[Jobs_status_coll]

Jakit_client = "mongodb://JakitDB_rw:6MiQ2Bf5kByS23c@p1ir1mon019.ger.corp.intel.com:7174,p2ir1mon019.ger.corp.intel.com:7174,p3ir1mon019.ger.corp.intel.com:7174/JakitDB?ssl=true&replicaSet=mongo7174"
Jakit_conn = 'JakitDB'
Reports_coll = 'Reports'
Tools_coll = 'Tools'

ConnectionStringJakit = pymongo.MongoClient(Jakit_client)
DatabaseJakit = ConnectionStringJakit[Jakit_conn]
CollectionReports = DatabaseJakit[Reports_coll]
CollectionTools = DatabaseJakit[Tools_coll]

class JakitJobs:
    """Jobs class"""

    def __init__(self):
        '''Initialize jobids'''

    def get_jobs(self,jobids):
        """ Read from Mongo and Store into DataFrame """

        jobs = CollectionJobs.find({"_id": {"$in": jobids}})
        list_jobs = list(jobs)

        return list_jobs
    
    def report_info(self,reportid,toolid):
        """call jakit api"""
        report_info = requests.get(f'https://JakitAPI.apps1-ir-int.icloud.intel.com/args?reportID={reportid}&toolID={toolid}', verify=False)
        
        if report_info.status_code == 200:
            return report_info.json()
        else:
            return None

    def job_info(self,jobids,indicator_names):
        jobids = [ObjectId(jobid) for jobid in jobids]
        dager_data = Database()
        jobs_info = self.get_jobs(jobids)


        for job in jobs_info:
            # Only keep indicators where 'Name' matches 'indicator_name'
            job['Indicators'] = [ind for ind in job['Indicators'] if ind['Name'] in indicator_names]

            lot = job['Lot']
            operation = job['Operation']
            wfrs = job['Wafers']

            # Initialize 'Data' field in job
            job['Data'] = {}

            for indicator in job['Indicators']:
                indicator_name = indicator['Name']
                for wfr in wfrs:
                    df_data = dager_data.pull_data(lot, indicator_name, operation, wfr, output_format='dataframe')

                    # Store dataframe in 'Data' field under corresponding wafer
                    if wfr not in job['Data']:
                        job['Data'][wfr] = {}
                    job['Data'][wfr][indicator_name] = df_data

        return jobs_info
    
    def report_info_direct(self, reportid):

        info = CollectionReports.find_one({"_id": ObjectId(reportid)})

        if info is not None:
            return info
        else:
            return None

    def get_toolid(self,indicator_name):
        tool = CollectionTools.find_one({"Name": indicator_name})
        return tool['_id']

    def get_args(self,name, params, description, defualtvalue, datatype, required = False, allowedValues = None, productid = None):
        args = {
            "ariesParameters": [
                {
                    "Name" : name,
                    "Status" : "NotStarted",
                    "Params" : params
                }
            ],
            "customArgs": [
                {
                    "name": name,
                    "description": description,
                    "defualtValue": defualtvalue,
                    "dataType": datatype,
                    "required": required,
                    "allowedValues": allowedValues
                }
            ]
        }
        return args
    
    def results_summary(self, reportid, IsPass = None, PassingItems = None, FailingItems = None, WarningItems = None):
        results = {
                "IsPass" : IsPass,
                "PassingItems" : PassingItems,
                "FailingItems" : FailingItems,
                "WarningItems" : WarningItems,
                "DateCreated" :datetime.datetime.now(),
                "ReportID": reportid
            }
        
        return results

    def get_summary(self, reportid, CollectionReportSummaries):
        summary = CollectionReportSummaries.find_one({"ReportID": reportid})
        if summary is not None:
            summary.pop('_id', None)  # Remove _id if it exists in the dictionary
        return summary
    
    def item_summary(self,name, description, target, result):
        
        item_dict = {
                'name': name,
                'description': description,
                'target': target,
                'result': result
            }
        return item_dict