from company_manager import CompanyManager
from wage_manager import WageManager
from wage_raw_data_manager import WageRawDataManager
from fine_manager import FineManager
from data.manager.crew.crew_level_manager import CrewLevelManager
from data.manager.crew.crew_manager import CrewManager
from data.manager.crew.crew_proj_map_manager import CrewProjMapManager

from data.manager.framework.dao_relation_map_manager import DaoRelationMapManager
from data.manager.framework.fe_configure_manager import FeConfigureManager


DaoRelationMapMgr = DaoRelationMapManager()
FeConfigureMgr = FeConfigureManager()

CompanyMgr = CompanyManager()
FineMgr = FineManager()
WageRawDataMgr = WageRawDataManager()
WageMgr = WageManager()
CrewMgr = CrewManager()
CrewLevelMgr = CrewLevelManager()
CrewProjMapMgr = CrewProjMapManager()