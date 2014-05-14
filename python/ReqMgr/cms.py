from WMCore.RequestManager.RequestDB.Settings.RequestStatus import StatusList, NextStatus
from WMCore.Services.SiteDB.SiteDB import SiteDBJSON

def next_status(status=None):
    "Return next ReqMgr status for given status"
    if  status:
        if  status in NextStatus:
            return NextStatus[status]
        else:
            return 'N/A'
    return StatusList

def sites():
    "Return known CMS site list from SiteDB"
    try:
        # Download a list of all the sites from SiteDB, uses v2 API.
        sitedb = SiteDBJSON()
        sites = sitedb.getAllCMSNames()
        sites.sort()
    except Exception as exc:
        msg = "ERROR: Could not retrieve sites from SiteDB, reason: %s" % str(exc)
        raise Exception(msg)
    return sites

def lfn_bases():
    "Return LFN Base list"
    storeResultLFNBase = [
        "/store/backfill/1",
        "/store/backfill/2",
        "/store/data",
        "/store/mc",
        "/store/generator",
        "/store/relval",
        "/store/hidata",
        "/store/himc",
        "/store/results/analysisops",
        "/store/results/b_physics",
        "/store/results/b_tagging",
        "/store/results/b2g",
        "/store/results/e_gamma_ecal",
        "/store/results/ewk",
        "/store/results/exotica",
        "/store/results/forward",
        "/store/results/heavy_ions",
        "/store/results/higgs",
        "/store/results/jets_met_hcal",
        "/store/results/muon",
        "/store/results/qcd",
        "/store/results/susy",
        "/store/results/tau_pflow",
        "/store/results/top",
        "/store/results/tracker_dpg",
        "/store/results/tracker_pog",
        "/store/results/trigger"]
    return storeResultLFNBase

def lfn_unmerged_bases():
    "Return list of LFN unmerged bases"
    out = ["/store/unmerged", "/store/temp"]
    return out

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
            "DQMSequences": "DQM sequences",
            "DataPileup": "Data Pileup",
            "FilterEfficiency": "Filter Efficiency",
            "GlobalTag": "Global tag",
            "MCPileup": "MonteCarlo Pileup",
            "PrimaryDataset": "Parimary dataset",
            "Acquisitionera": "Acquisition era",
            "CmsPath": "CMS path",
            "DBS": "DBS urls",
            "ProcessingVersion": "Processing version",
            "RequestType": "Request type",
            "ACDCDatabase": "ACDC database",
            "ACDCServer": "ACDC server",
            "CollectionName": "Collection name",
            "IgnoredOutputModules": "Ignored output modules",
            "InitialTaskPath": "Initial task path",
            "KeepStepOneOutput": "Keep step one output",
            "KeepStepTwoOutput": "Keep step two output",
            "StepOneConfigCacheID": "Step one config cache id",
            "StepOneOutputModuleName": "Step one output module name",
            "StepThreeConfigCacheID": "Step three config cache id",
            "StepTwoConfigCacheID": "Step two config cache id",
            "StepTwoOutputModuleName": "Step two output module name",
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

