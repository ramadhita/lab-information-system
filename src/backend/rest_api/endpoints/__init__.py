from .token import token_namespace
from .signup import signup_namespace
from .pasien import pasien_namespace
from .check_in import checkin_namespace
from .check_out import check_out_namespace
from .check_in_PasienBaru import checkinpasienbaru_namespace
from .list_alat import listalat_namespace

all_namespaces= [
    token_namespace,
    signup_namespace,
    pasien_namespace,
    checkin_namespace,
    check_out_namespace,
    checkinpasienbaru_namespace,
    listalat_namespace
]