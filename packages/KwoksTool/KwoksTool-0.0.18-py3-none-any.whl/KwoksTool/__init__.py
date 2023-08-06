from KwoksTool.info import (welcome,how)
from KwoksTool.function import (GetCityNumFromLiepin,
                                GetCityNumFromBossZhiPing,
                                GetCityNameFromLiepin,
                                YesOrNot,
                                CheckIp,
                                IntoZip,
                                ZipOut,
                                SendEmail,
                                GetEmail,
                                ProgressBar,
                                MergeTable,
                                ChoiceColumn)
from KwoksTool.source.IpPool import GetIpPool
from KwoksTool.model import (GetProbMatrix,ToMat)
from KwoksTool.spider import (Browser, PlateComponentStocks)
from KwoksTool.Spider.stock import GetStocksData
class spider:
    from KwoksTool.Spider.function import (find_diffrent_key_from_str)
    from KwoksTool.source.IpPool import (get_ip_from_shop)
class show:
    from KwoksTool.Show.function import (SelecTHead,px_to_percent)
dependencies=[
    'selenium',
    'tushare',
    'pyexecjs',
    'requests',
    'pandas',
    'numpy',
    'twine==4.0.2',
    'build==0.10.0',
    'pyecharts'
]