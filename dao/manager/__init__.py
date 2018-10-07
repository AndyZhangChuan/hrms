from company_manager import CompanyManager
from wage_manager import WageManager
from wage_raw_data_manager import WageRawDataManager
from fine_manager import FineManager
from dao.manager.crew.crew_level_manager import CrewLevelManager
from dao.manager.crew.crew_manager import CrewManager
from dao.manager.crew.crew_proj_map_manager import CrewProjMapManager

CompanyMgr = CompanyManager()
FineMgr = FineManager()
WageRawDataMgr = WageRawDataManager()
WageMgr = WageManager()
CrewMgr = CrewManager()
CrewLevelMgr = CrewLevelManager()
CrewProjMapMgr = CrewProjMapManager()