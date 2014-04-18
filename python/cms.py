def web_ui_names():
    "Return dict of web UI JSON naming conventions"
    maps = {"InputDataset": "Input Dataset",
            "IncludeParents": "Include Parents",
            "PrepID": "Optional Prep ID String",
            "BlockBlacklist": "Block black list",
            "RequestPriority": "Request Priority",
            "TimePerEvent": "Time per event (Seconds)",
            "RunWhitelist": "Run white list",
            "BlockWhitelist": "Block white list",
            "OpenRunningTimeout": "Open Running Timeout",
            "DQLUploadURL": "DQM URL",
            "DqmSequences": "DQM Sequences",
            "SizePerEvent": "Size per event (KBytes)",
            "ScramArch": "Architecture",
            "EnableHarvesting": "Enable DQM Harvesting",
            "DQMConfigCacheID": "DQM Config CacheID",
            "Memory": "Memory (MBytes)",
            "RunBlacklist": "Run black list",
            "RequestString": "Optional Request ID String",
            "CMSSWVersion": "Software Releases",
            "DQMUploadURL":"DQM URL",
            "DQMSequences": "DQM sequences"
            }
    return maps

def dqm_urls():
    "Return list of DQM urls"
    urls = [
            "https://cmsweb.cern.ch/dqm/dev",
            "https://cmsweb.cern.ch/dqm/offline",
            "https://cmsweb.cern.ch/dqm/relval",
            "https://cmsweb-testbed.cern.ch/dqm/dev",
            "https://cmsweb-testbed.cern.ch/dqm/offline",
            "https://cmsweb-testbed.cern.ch/dqm/relval",
            ]
    return urls

def dbs_urls():
    "Return list of DBS urls"
    urls = []
    base = "https://cmsweb.cern.ch/dbs/prod/global/DBSReader/"
    for inst in ["prod", "phys01", "phys02", "phys03"]:
        urls.append(base.replace("prod", inst))
    return urls

def releases():
    "Return list of CMSSW releases"
    releases=["CMSSW_7_0_0", "CMSSW_6_8_1"]
    return releases

def architectures():
    "Return list of CMSSW architectures"
    arch=["slc5_amd64_gcc472", "slc5_ad4_gcc481"]
    return arch

def scenarios():
    "Return list of scenarios"
    slist = ["pp", "cosmics", "hcalnzs", "preprodmc", "prodmc"]
    return slist

def cms_groups():
    "Return list of CMS data-ops groups"
    groups = ["DATAOPS"]
    return groups
