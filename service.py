import pd_cal_new as pcl
import dao

def process(f):
    
    df = pcl.pd_dataFrame(f)
    msg = dao.save(df)
    
    if msg=='success':
        return df
    elif msg=='error 1':
        return 'error in connection'
    elif msg=='error 2':
        return 'error in insert'
    
def searchCif(cif):
    return dao.searchCif(cif)
    
def home():
    return dao.home()