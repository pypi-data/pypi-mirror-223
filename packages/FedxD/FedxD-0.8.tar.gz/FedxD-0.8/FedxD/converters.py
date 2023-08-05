class Time:
    @staticmethod
    def DaytoSec(days):
        sec = days * 24 * 60 * 60
        return sec
    @staticmethod
    def SectoDay(sec):
        days = sec / 24 / 60 / 60
        return days


class Bytes:
    @staticmethod
    def MBtoB(MB):
        B=MB*1024*1024
        return B
    @staticmethod
    def GBtoB(GB):
        B = GB*1024*1024*1024
        return B
    @staticmethod
    def TBtoB(TB):
        B = TB*1024*1024*1024*1024
        return B
    @staticmethod
    def KBtoB(KB):
        B = KB*1024
        return B
    @staticmethod
    def BtoKB(B):
        KB = B/1024
        return KB
    @staticmethod
    def BtoMB(B):
        MB = B/1024/1024
        return MB
    @staticmethod
    def BtoGB(B):
        GB = B/1024/1024/1024
        return GB
    @staticmethod
    def BtoTB(B):
        TB = B/1024/1024/1024/1024
        return TB
class Weight:
    @staticmethod
    def KGtoP(KG):
        P = KG*2.2
        return P
    @staticmethod
    def PtoKG(P):
        KG = P/2.2
        return
class Temperature:
    @staticmethod
    def CtoF(C):
        F = (C*9/5)+32
        return F
    @staticmethod
    def FtoC(F):
        C = (F-32)*5/9
        return C
    @staticmethod
    def CtoK(C):
        K = C+273.15
        return K
    @staticmethod
    def KtoC(K):
        C = K-273.15
        return C
    @staticmethod
    def FtoK(F):
        C=(F-32)*5/9
        K=C+273.15
        return K
    @staticmethod
    def KtoF(K):
        C = K-273.15
        F = (C*9/5)+32
        return F
class Length:
    @staticmethod
    def MtoF(M):
        F = M*3.28084
        return F
    @staticmethod
    def FtoM(F):
        M = F/3.28084
        return M
    @staticmethod
    def CmtoI(Cm):
        I = Cm/2.54
        return I
    @staticmethod
    def ItoCm(I):
        Cm = I*2.54
        return Cm
    @staticmethod
    def FtoY(F):
        Y = F*3
        return Y
    @staticmethod
    def YtoF(Y):
        F = Y/3
        return F
    @staticmethod
    def MtoY(M):
        Y = M*1.09361
        return Y
    @staticmethod
    def YtoM(Y):
        M = Y/1.09361
        return M
