import sys
import importlib.util

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A

from MobileHelperCore.service_api import MobileHelperService as Service, as_developer

host: str = A.OS.host()

def checker(telephone_number: str) -> bool:
    if not A.D_C.empty(A.SRV.get_support_host_list(A.CT_SR.MOBILE_HELPER)):
        am_i_tester: bool = A.D.is_not_none(A.CT.TEST.USER) and A.D_TN.by_login(A.CT.TEST.USER) == telephone_number
        if as_developer() or A.D.contains(host, A.CT_H.DEVELOPER.NAME):
            return am_i_tester
        return not am_i_tester
    return True

Service(10, checker).start()