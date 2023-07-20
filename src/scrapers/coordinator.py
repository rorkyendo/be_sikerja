from .jobs_id import data_lowongan_jobsid
from .glints import data_lowongan_glints
from .jobstreet import data_lowongan_jobstreet
from .karir import data_lowongan_karir
from .loker import data_lowongan_loker

def get_new_jobs(keyword: str, taggar: str):
    return (data_lowongan_jobsid(keyword, taggar) + 
            data_lowongan_glints(keyword, taggar) + 
            data_lowongan_jobstreet(keyword, taggar) + 
            data_lowongan_karir(keyword, taggar) + 
            data_lowongan_loker(keyword, taggar))