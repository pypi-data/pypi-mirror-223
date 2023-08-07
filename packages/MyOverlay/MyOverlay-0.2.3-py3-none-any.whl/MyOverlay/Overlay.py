from MyOverlay.funcs import myfunctions

def InnitOverlay():
    return myfunctions.StartOverlay()
    
def settext(text: str, PosX: int, PosY: int):
    myfunctions.settext(text, PosX, PosY)
    
def KillOverlay():
    myfunctions.KillOverlay()
    
def StatusOverlay():
    return myfunctions.StatusOverlay()

def GetJobDirectory(JobName: str):
    return myfunctions.GetJobDirectory(JobName)