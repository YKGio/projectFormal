from django.db import models

class Customers(models.Model):
    cusName = models.CharField(max_length=50)
    cusCode = models.CharField(max_length=50)
    cusPhoneNum = models.CharField(max_length=50)
    #cusBirthDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    cusSex = models.CharField(max_length=50)
    cusShopCode = models.CharField(max_length=50, null=True)
    cusRemarks = models.CharField(max_length=200, null=True)

    
    def __str__(self):
        return self.cusName

class Stock(models.Model):
    stockType = models.CharField(max_length=50)
    stockCode = models.CharField(max_length=50)
    stockName = models.CharField(max_length=50)
    stockPrice = models.IntegerField()

    def __str__(self):
        return self.stockName

class InStock(models.Model):
    inStockCode = models.CharField(max_length=50)
    inStockShopCode = models.CharField(max_length=50)
    inStockQua = models.IntegerField()

    def __str__(self):
        return self.inStockCode

class Employee(models.Model):
    empName = models.CharField(max_length=50)
    empCode = models.CharField(max_length=50)
    empBirthDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    empPhoneNum = models.CharField(max_length=50)
    empAdd = models.CharField(max_length=100)
    empShop = models.CharField(max_length=50, null=True)
    empClass = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.empName

class CombineStock(models.Model):
    comCode = models.CharField(max_length=50)
    comStockCode = models.CharField(max_length=50)

    def __str__(self):
        return self.comCode

class Sale(models.Model):
    saleDate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    saleCode  = models.CharField(max_length=50, null=True)
    saleCusCode = models.CharField(max_length=50, null=True)
    saleStockCode = models.CharField(max_length=50, null=True)
    saleShopCode = models.CharField(max_length=50, null=True)
    saleQua = models.IntegerField(null=True)
    salePrice = models.IntegerField(null=True)
    saleEmpCode = models.CharField(max_length=50, null=True)
    salePoint = models.IntegerField(null=True)
    saleType = models.CharField(max_length=50, null=True)
    saleRemark = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.saleCode

class SetSale(models.Model):
    setSaleCode = models.CharField(max_length=50, null=True)
    setDate = models.DateField(auto_now=False, auto_now_add=False, null = True)
    setCode = models.CharField(max_length=50, null = True)
    setCusCode = models.CharField(max_length=50, null = True)
    setShopCode = models.CharField(max_length=50, null = True)
    setEmp1Code = models.CharField(max_length=50, null=True)
    setEmp2Code = models.CharField(max_length=50, null=True)
    setEmp3Code = models.CharField(max_length=50, null=True)
    setPrice = models.IntegerField(null = True)
    setPoint = models.IntegerField(null = True)
    setType = models.CharField(max_length=50, null=True)
    setRemark = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.setSaleCode

class importReport(models.Model):
    importCode = models.CharField(max_length=50)
    importStockCode = models.CharField(max_length=50)
    importFromShopCode = models.CharField(max_length=50)
    importToShopCode = models.CharField(max_length=50)
    importQua = models.IntegerField()

    def __str__(self):
        return self.importCode


class CusOwnSet(models.Model):
    ownCusCode = models.CharField(max_length=50)
    ownSetCode = models.CharField(max_length=50)
    ownQua = models.IntegerField()

    def __str__(self):
        return self.ownCusCode

class Shop(models.Model):
    shopName = models.CharField(max_length=50)
    shopCode = models.CharField(max_length=50)

    def __str__(self):
        return self.shopName

class RegularBonus(models.Model):
    bonusName = models.CharField(max_length=50)
    bonusCode = models.CharField(max_length=50)
    bonusValue = models.IntegerField()

    def __str__(self):
        return self.bonusName

class Commission(models.Model):
    commName = models.CharField(max_length=50)
    commCode = models.CharField(max_length=50)

    def __str__(self):
        return self.commName

class CommLimit(models.Model):
    comm_commCode = models.CharField(max_length=50)
    CLCode = models.CharField(max_length=50, null=True)
    CLIncomeLimit = models.IntegerField()
    CLBonusPercent = models.IntegerField()

    def __str__(self):
        return self.comm_commCode

class MultiSevicePercent(models.Model):
    MSPName = models.CharField(max_length=50)
    MSPCode = models.CharField(max_length=50)
    MSPemp1 = models.IntegerField()
    MSPemp2 = models.IntegerField()
    MSPemp3 = models.IntegerField()

    def __str__(self):
        return self.MSPName

class SalarySelectEmp(models.Model):
    SSEEmpCode = models.CharField(max_length=50)

    def __str__(self):
        return self.SSEEmpCode

class SalaryResult(models.Model):
    SRempName = models.CharField(max_length=50)
    SRsalary = models.IntegerField()
    SRpoint = models.IntegerField()
    SRpoint1 = models.IntegerField()
    SRpoint2 = models.IntegerField()
    SRpoint3 = models.IntegerField()
    SRstockIncomeComm = models.IntegerField()
    SRincome = models.IntegerField()
    SRSCIncomeComm = models.IntegerField()
    SRSCIncome = models.IntegerField()
    SRbarberIncomeComm = models.IntegerField()
    SRbarberIncome = models.IntegerField()
    SRresult = models.IntegerField()

    def __str__(self):
        return self.SRempName