from django.shortcuts import render
from django.http import HttpResponse
from .models import Customers, Stock, Employee, CombineStock, Sale, SetSale, CusOwnSet, InStock, importReport, Shop, RegularBonus, Commission, CommLimit, MultiSevicePercent, SalarySelectEmp, SalaryResult
from .forms import cusForm, stockForm

comCodeNow = 0
saleCodeNow = 0
shopNow = ''
importCodeNow = 0

def login(request):
    shopAll = Shop.objects.all().order_by('shopCode')
    return render(request, 'login.html', locals())

def index(request, a):
    global shopNow
    shopNow = a
    damn = shopNow
    return render(request, 'index.html', locals())

def redirectIndex(request):
    global shopNow
    damn = shopNow

    if damn == 'SH00':
        return render(request, 'redirectAdmin.html', locals())

    return render(request, 'redirectIndex.html', locals())

def stock(request):
    global shopNow

    if request.method == 'POST':

        stockSearch = request.POST['stockSearch']

        queryRes = Stock.objects.filter(stockCode__contains = stockSearch)
        queryRes |= Stock.objects.filter(stockName__contains = stockSearch)
        queryRes |= Stock.objects.filter(stockType__contains = stockSearch)

        for res in queryRes:
            if not res.stockType == '課程':
                resStockCode = res.stockCode
                if not InStock.objects.filter(inStockCode = resStockCode, inStockShopCode = shopNow):
                    res.stockQua = 0
                else:
                    res.stockQua = InStock.objects.get(inStockCode = resStockCode, inStockShopCode = shopNow).inStockQua
            
        return render(request,'stock.html', locals())




    return render(request, 'stock.html', locals())

def editStock(request, a):
    global shopNow
    stockC = a
    queryRes = Stock.objects.get(stockCode = stockC)
    if queryRes.stockType == '課程' or '組合':
        stockQua = ''
    else:
        stockQua = InStock.objects.get(inStockCode=queryRes.stockCode, inStockShopCode=shopNow).inStockQua
    
    editStockType = Stock.objects.get(stockCode = stockC).stockType
    if editStockType == '組合':
        combineSet = CombineStock.objects.filter(comCode = stockC)
        stockSetInCombine = Stock.objects.filter(stockCode = '')
        for combine in combineSet:
            stockCodeInCombine = combine.comStockCode
            stockSetInCombine |= Stock.objects.filter(stockCode = stockCodeInCombine)
        
        if 'searchStock' in request.POST:
            search = request.POST['stockName']

            stockCombineSet = Stock.objects.filter(stockCode__contains = search)
            stockCombineSet |= Stock.objects.filter(stockName__contains = search)
            stockCombineSet |= Stock.objects.filter(stockType__contains = search)

        if 'save' in request.POST:
            editStockType = request.POST['stockType']
            editStockCode = request.POST['stockCode'] 
            editStockName = request.POST['stockName'] 
            editStockPrice = request.POST['stockPrice'] 
            editStockQua = request.POST['stockQua'] 
            
            Stock.objects.filter(stockCode=stockC).update(stockType=editStockType)
            Stock.objects.filter(stockCode=stockC).update(stockCode=editStockCode)
            Stock.objects.filter(stockCode=stockC).update(stockName=editStockName)
            Stock.objects.filter(stockCode=stockC).update(stockPrice=editStockPrice)
            return render(request, 'success.html', locals())
        
        return render(request, 'editCombineStock.html', locals())

    if request.method == 'POST':
        editStockType = request.POST['stockType']
        editStockCode = request.POST['stockCode'] 
        editStockName = request.POST['stockName'] 
        editStockPrice = request.POST['stockPrice'] 
        editStockQua = request.POST['stockQua'] 
        
        Stock.objects.filter(stockCode=queryRes.stockCode).update(stockType=editStockType)
        Stock.objects.filter(stockCode=queryRes.stockCode).update(stockCode=editStockCode)
        Stock.objects.filter(stockCode=queryRes.stockCode).update(stockName=editStockName)
        Stock.objects.filter(stockCode=queryRes.stockCode).update(stockPrice=editStockPrice)
        if not editStockType == '課程':
            InStock.objects.filter(inStockCode=stockC, inStockShopCode=shopNow).update(inStockQua=editStockQua)
        return render(request, 'success.html', locals())

    return render(request, 'editStock.html', locals())

def selectImport(request, a):
    global shopNow, importCodeNow
    importCode = 'IM' + format(importCodeNow, '03d')
    selectImportStock = Stock.objects.get(stockCode=a)
    selectImportInStockToQua = InStock.objects.get(inStockCode=a, inStockShopCode=shopNow).inStockQua
    shopAll = Shop.objects.order_by('shopCode')

    if 'completeImport' in request.POST:
        selectShop = request.POST['selectShop']
        importQua = request.POST['selectImportQua']

        selectImportInStockFromQua = InStock.objects.get(inStockCode=a, inStockShopCode=selectShop).inStockQua
        selectImportInStockToQua += int(importQua)
        selectImportInStockFromQua -= int(importQua)
        InStock.objects.filter(inStockCode=a, inStockShopCode=selectShop).update(inStockQua=selectImportInStockFromQua)
        InStock.objects.filter(inStockCode=a, inStockShopCode=shopNow).update(inStockQua=selectImportInStockToQua)

        importReport.objects.create(importCode=importCode, importStockCode=a, importFromShopCode=selectShop, importToShopCode=shopNow, importQua=importQua)
        importCodeNow += 1

        return render(request, 'success.html', locals())
    return render(request, 'selectImport.html', locals())

def adminImport(request, a):
    global shopNow, importCodeNow
    importCode = 'IM' + format(importCodeNow, '03d')
    selectImportStock = Stock.objects.get(stockCode=a)

    if 'completeImport' in request.POST:
        importQua = request.POST['selectImportQua']

        selectInStockQua = InStock.objects.get(inStockCode=a, inStockShopCode=shopNow).inStockQua
        selectInStockQua += int(importQua)
        InStock.objects.filter(inStockCode=a, inStockShopCode=shopNow).update(inStockQua=selectInStockQua)

        importReport.objects.create(importCode=importCode, importStockCode=a, importFromShopCode='外部', importToShopCode=shopNow, importQua=importQua)
        importCodeNow += 1

        return render(request, 'success.html')
    
    return render(request, 'adminImport.html', locals())


def editCombineStockAdd(request, a, b):
    combineStock = a
    stockCode = b

    CombineStock.objects.create(comCode = combineStock, comStockCode = stockCode)

    return render(request, 'backToEditStock.html', locals())
    

def editCombineStockDelete(request, a, b):
    combineStock = a
    stockCode = b

    CombineStock.objects.get(comStockCode = stockCode, comCode = combineStock).delete()

    return render(request, 'backToEditStock.html', locals())

def addStock(request):
    if request.method == 'POST':
        addStockType = request.POST['stockType']
        addStockCode = request.POST['stockCode'] 
        addStockName = request.POST['stockName'] 
        addStockPrice = request.POST['stockPrice'] 

        Stock.objects.create(stockType=addStockType, stockCode=addStockCode, stockName=addStockName, stockPrice=addStockPrice)
        InStock.objects.create(inStockCode=addStockCode, inStockShopCode='SH00', inStockQua=0)
        InStock.objects.create(inStockCode=addStockCode, inStockShopCode='SH01', inStockQua=0)
        InStock.objects.create(inStockCode=addStockCode, inStockShopCode='SH02', inStockQua=0)

        return render(request, 'success.html', locals())

    return render(request, 'addStock.html', locals())

def emp(request):
    global shopNow

    if 'searchEmp' in request.POST:
        search = request.POST['empSearch']
    
        queryRes = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'searchAllEmp' in request.POST:
        search = request.POST['empSearch']
    
        queryRes = Employee.objects.filter(empName__contains = search)
        queryRes |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    return render(request,'emp.html', locals())

def editEmp(request, a):
    empC = a
    queryRes = Employee.objects.get(empCode = empC)

    if request.method == 'POST':
        editEmpName = request.POST['empName']
        editEmpCode = request.POST['empCode'] 
        editEmpPhoneNum = request.POST['empPhoneNum'] 
        editEmpAdd = request.POST['empAdd'] 
        editEmpClass = request.POST['empClass'] 
        
        Employee.objects.filter(empCode=queryRes.empCode).update(empName=editEmpName)
        Employee.objects.filter(empCode=queryRes.empCode).update(empCode=editEmpCode)
        Employee.objects.filter(empCode=queryRes.empCode).update(empPhoneNum=editEmpPhoneNum)
        Employee.objects.filter(empCode=queryRes.empCode).update(empAdd=editEmpAdd)
        Employee.objects.filter(empCode=queryRes.empCode).update(empClass=editEmpClass)
        return render(request, 'success.html', locals())

    return render(request, 'editEmp.html', locals())

def addEmp(request):
    global shopNow
    if request.method == 'POST':
        addCusName = request.POST['empName']
        addCusCode = request.POST['empCode'] 
        addCusPhoneNum = request.POST['empPhoneNum'] 
        addCusBirthDate = request.POST['empBirthDate'] 
        addEmpAdd = request.POST['empAdd'] 
        addEmpClass = request.POST['empClass']

        Employee.objects.create(empName=addCusName, empCode=addCusCode, empPhoneNum=addCusPhoneNum, empBirthDate=addCusBirthDate, empAdd=addEmpAdd, empClass=addEmpClass, empShop=shopNow)
        return render(request, 'success.html', locals())

    return render(request, 'addEmp.html', locals())

def cus(request):
    if request.method == 'POST':
        cusF = cusForm(request.POST)
        if cusF.is_valid():
            cusSearch = cusF.cleaned_data['查詢顧客']

            queryRes = Customers.objects.filter(cusName__contains = cusSearch)
            queryRes |= Customers.objects.filter(cusPhoneNum__contains = cusSearch)
            queryRes |= Customers.objects.filter(cusCode__contains = cusSearch)

            return render(request,'cus.html', locals())
    else:
        cusF = cusForm()

    return render(request,'cus.html', {'cusF': cusF})

def editCus(request, a):
    cusC = a
    queryRes = Customers.objects.get(cusCode = cusC)

    if request.method == 'POST':
        editCusName = request.POST['cusName']
        editCusCode = request.POST['cusCode'] 
        editCusPhoneNum = request.POST['cusPhoneNum'] 
        editCusSex = request.POST['cusSex'] 
        editCusRemarks = request.POST['cusRemarks'] 

        Customers.objects.filter(cusCode=queryRes.cusCode).update(cusName=editCusName)
        Customers.objects.filter(cusCode=queryRes.cusCode).update(cusCode=editCusCode)
        Customers.objects.filter(cusCode=queryRes.cusCode).update(cusPhoneNum=editCusPhoneNum)
        Customers.objects.filter(cusCode=queryRes.cusCode).update(cusSex=editCusSex)
        Customers.objects.filter(cusCode=queryRes.cusCode).update(cusRemarks=editCusRemarks)
        return render(request, 'success.html', locals())

    return render(request, 'editCus.html', locals())

def addCus(request):
    if request.method == 'POST':
        addCusName = request.POST['cusName']
        addCusCode = request.POST['cusCode'] 
        addCusPhoneNum = request.POST['cusPhoneNum'] 
        # addCusBirthDate = request.POST['cusBirthDate'] 
        addCusSex = request.POST['cusSex'] 
        addCusRemarks = request.POST['cusRemarks'] 

        Customers.objects.create(cusName=addCusName, cusCode=addCusCode, cusPhoneNum=addCusPhoneNum, cusSex=addCusSex, cusRemarks=addCusRemarks)
        return render(request, 'success.html', locals())

    return render(request, 'addCus.html', locals())

def delete(request, a):
    deleteCode = a

    try:
        Customers.objects.get(cusCode=deleteCode).delete()
    except:
        try:
            Employee.objects.get(empCode=deleteCode).delete()
        except:
            return HttpResponse("操作失敗")

    return render(request, 'success.html', locals())

def deleteStock(reqest, a):
    deleteCode = a

    if Stock.objects.get(stockCode=deleteCode).stockType == '組合':
        CombineStock.objects.filter(comCode=deleteCode).delete()

    Stock.objects.get(stockCode=deleteCode).delete()
    InStock.objects.filter(inStockCode=deleteCode).delete()

    return render(reqest, 'success.html', locals())
    

def combineStock(request):
    global comCodeNow

    completeComCode = "P" + format(comCodeNow, '03d')
    combinedAll = CombineStock.objects.filter(comCode = completeComCode)

    stockSetInCombine = Stock.objects.filter(stockCode = '')
    for combine in combinedAll:
        stockCodeInCombine = combine.comStockCode
        stockSetInCombine |= Stock.objects.filter(stockCode = stockCodeInCombine)

    if request.POST:
        if 'searchStock' in request.POST:
            search = request.POST['stockName']

            queryRes = Stock.objects.filter(stockCode__contains = search)
            queryRes |= Stock.objects.filter(stockName__contains = search)
            queryRes |= Stock.objects.filter(stockType__contains = search)

            return render(request,'combineStock.html', locals())
        
        if 'completeCombine' in request.POST:
            comCodeComplete = "P" + format(comCodeNow, '03d')
            combineStockName = request.POST['combineName']
            combineStockPrice = request.POST['combinePrice']
            comCodeNow += 1

            Stock.objects.create(stockType = '組合', stockCode = comCodeComplete, stockName = combineStockName, stockPrice = combineStockPrice)
            InStock.objects.create(inStockCode=comCodeComplete, inStockShopCode='SH00', inStockQua=0)
            InStock.objects.create(inStockCode=comCodeComplete, inStockShopCode='SH01', inStockQua=0)
            InStock.objects.create(inStockCode=comCodeComplete, inStockShopCode='SH02', inStockQua=0)

            return render(request, 'success.html', locals())

    return render(request, 'combineStock.html', locals())

def combining(request, a):
    combine = a

    comCodeComplete = "P" + format(comCodeNow, '03d')
    
    CombineStock.objects.create(comCode = comCodeComplete, comStockCode = combine)

    return render(request, 'backToCombine.html', locals())

def combineStockDelete(request, a, b):
    combineStock = a
    stockCode = b

    CombineStock.objects.get(comStockCode = stockCode, comCode = combineStock).delete()

    return render(request, 'backToCombine.html', locals())

def sucCombine(request):
    global comCodeNow
    comCodeNow += 1
    return render(request, 'success.html', locals())

def sale(request):
    global saleCodeNow, shopNow
    damn = shopNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')
    Sale.objects.get_or_create(saleCode = saleCodeComplete)

    saleAll = Sale.objects.get(saleCode = saleCodeComplete)

    if not saleAll.saleCusCode:
        saleAll.saleCusCode = ''
    if not saleAll.saleStockCode:
        saleAll.saleStockCode = ''
    if not saleAll.saleEmpCode:
        saleAll.saleEmpCode = ''

    if saleAll.saleStockCode:
        sStockCode = saleAll.saleStockCode
        stockNow = Stock.objects.get(stockCode = sStockCode)
        stockPoint = int(stockNow.stockPrice/10)

    if request.method == 'POST':
        if 'cusBut' in request.POST:
            search = request.POST['cusSearch']

            queryRes1 = Customers.objects.filter(cusName__contains = search)
            queryRes1 |= Customers.objects.filter(cusPhoneNum__contains = search)
            queryRes1 |= Customers.objects.filter(cusCode__contains = search)

            return render(request,'sale.html', locals())

        if 'empBut' in request.POST:
            search = request.POST['empSearch']
        
            queryRes2 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
            queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
            queryRes2 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

            for res in queryRes2:
                if res.empShop == 'SH01':
                    res.empShop = '旗艦店'
                else:
                    res.empShop = '崇德店' 

        if 'empAllBut' in request.POST:
            search = request.POST['empSearch']
        
            queryRes2 = Employee.objects.filter(empName__contains = search)
            queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search)
            queryRes2 |= Employee.objects.filter(empCode__contains = search)

            for res in queryRes2:
                if res.empShop == 'SH01':
                    res.empShop = '旗艦店'
                else:
                    res.empShop = '崇德店' 

        if 'stockBut' in request.POST:
            search = request.POST['stockSearch']

            queryRes3 = Stock.objects.filter(stockCode__contains = search)
            queryRes3 |= Stock.objects.filter(stockName__contains = search)
            queryRes3 |= Stock.objects.filter(stockType__contains = search)

            for res3 in queryRes3:
                if not InStock.objects.filter(inStockCode=res3.stockCode, inStockShopCode=shopNow):
                    res3.stockQua = ''
                else:
                    stockQua = InStock.objects.get(inStockCode=res3.stockCode, inStockShopCode=shopNow).inStockQua
                    res3.stockQua = stockQua

            return render(request,'sale.html', locals())
        
        if 'completeSale' in request.POST:
            saleDateForm = request.POST['saleDate']
            saleShopForm = request.POST['saleShop']
            saleQuaForm = request.POST['saleQua']
            salePriceForm = request.POST['salePrice']
            salePointForm = request.POST['salePoint']
            saleTypeForm = request.POST['selectSaleType']
            saleRemarkForm = request.POST['saleRemark']

            saleStockSet = Sale.objects.get(saleCode = saleCodeComplete)
            saleStockCodeNow = saleStockSet.saleStockCode
            saleCusCodeNow = saleStockSet.saleCusCode
            saleStockType = Stock.objects.get(stockCode = saleStockCodeNow).stockType

            if saleStockType == '課程':
                CusOwnSet.objects.create(ownCusCode = saleCusCodeNow, ownSetCode = saleStockCodeNow, ownQua = 12)

            if saleStockType == '組合':
                combineStockSet = CombineStock.objects.filter(comCode = saleStockCodeNow)

                for combineStock in combineStockSet:
                    stockCodeInCombine = combineStock.comStockCode
                    saleCombineStockQuaNow = InStock.objects.get(inStockCode = stockCodeInCombine, inStockShopCode=shopNow).inStockQua
                    saleCombineStockQuaNow -= int(saleQuaForm)
                    InStock.objects.filter(inStockCode = stockCodeInCombine, inStockShopCode=shopNow).update(inStockQua = saleCombineStockQuaNow)

            Sale.objects.filter(saleCode = saleCodeComplete).update(saleDate = saleDateForm, saleShopCode = saleShopForm, saleQua = saleQuaForm, salePrice = salePriceForm, salePoint = salePointForm, saleType=saleTypeForm, saleRemark = saleRemarkForm)
            return render(request,'completeSale.html', locals())
    
    return render(request, 'sale.html', locals())

def saleCus(request, a):
    selectCus = a
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    Sale.objects.filter(saleCode = saleCodeComplete).update(saleCusCode = selectCus)
    return render(request,'selectSuc.html', locals())

def setSaleCus(request, a):
    selectCus = a
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setCusCode = selectCus)
    return render(request,'backToSericeSale.html', locals())
    
def saleStock(request, a):
    selectStock = a
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    Sale.objects.filter(saleCode = saleCodeComplete).update(saleStockCode = selectStock)
    return render(request,'selectSuc.html', locals())

def setSaleStock(request, a):
    selectStock = a
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setCode = selectStock)
    return render(request,'backToSericeSale.html', locals())

def saleEmp(request, a):
    selectEmp = a
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    Sale.objects.filter(saleCode = saleCodeComplete).update(saleEmpCode = selectEmp)
    return render(request,'selectSuc.html', locals())

def completeSale(request):
    global saleCodeNow, shopNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    sellingStock = Sale.objects.get(saleCode = saleCodeComplete)
    if not Stock.objects.get(stockCode=sellingStock.saleStockCode).stockType == '課程':
        inStockNow = InStock.objects.get(inStockCode=sellingStock.saleStockCode, inStockShopCode=shopNow)
        InStock.objects.filter(inStockCode = sellingStock.saleStockCode, inStockShopCode=shopNow).update(inStockQua = inStockNow.inStockQua - sellingStock.saleQua)

    saleCodeNow += 1

    return render(request,'success.html', locals())

def setSale(request):
    if request.method == 'POST':
        search = request.POST['cusSearch']

        queryRes = Customers.objects.filter(cusName__contains = search)
        queryRes |= Customers.objects.filter(cusPhoneNum__contains = search)
        queryRes |= Customers.objects.filter(cusCode__contains = search)

        return render(request,'setSale.html', locals())

    return render(request, 'setSale.html', locals())

def setllingSet(request, a):
    sellingCus = a

    cusOwnSetSet = CusOwnSet.objects.filter(ownCusCode = sellingCus)

    return render(request, 'sellingSet.html', locals())

def deduct(request, a, b):
    global saleCodeNow, shopNow
    damn = shopNow

    sellingCus = a
    sellingSet = b

    saleCodeComplete = 'S' + format(saleCodeNow, '03d')
    SetSale.objects.get_or_create(setSaleCode = saleCodeComplete, setCode = sellingSet, setCusCode = sellingCus)

    saleAll = SetSale.objects.get(setSaleCode = saleCodeComplete)
    if not saleAll.setEmp1Code:
        saleAll.setEmp1Code = ''
    if not saleAll.setEmp2Code:
        saleAll.setEmp2Code = ''
    if not saleAll.setEmp3Code:
        saleAll.setEmp3Code = ''

    tmp = Stock.objects.get(stockCode = sellingSet).stockPrice
    tmp /= 12
    tmp += 0.5
    oneCoursePrice = int(tmp)
    

    if 'empBut1' in request.POST:
        search = request.POST['empSearch']
    
        queryRes1 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes1 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes1 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes1:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut1' in request.POST:
        search = request.POST['empSearch']
    
        queryRes1 = Employee.objects.filter(empName__contains = search)
        queryRes1 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes1 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes1:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empBut2' in request.POST:
        search = request.POST['empSearch']
    
        queryRes2 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes2 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes2:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut2' in request.POST:
        search = request.POST['empSearch']
    
        queryRes2 = Employee.objects.filter(empName__contains = search)
        queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes2 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes2:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empBut3' in request.POST:
        search = request.POST['empSearch']
    
        queryRes3 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes3 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes3 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes3:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut3' in request.POST:
        search = request.POST['empSearch']
    
        queryRes3 = Employee.objects.filter(empName__contains = search)
        queryRes3 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes3 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes3:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 
    if 'completeDeduct' in request.POST:
        saleDateForm = request.POST['saleDate']
        saleShopForm = request.POST['saleShop']
        salePriceForm = request.POST['salePrice']
        salePointForm = request.POST['salePoint']
        saleTypeForm  = request.POST['selectSaleType']
        saleRemarkForm = request.POST['saleRemark']

        SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setDate = saleDateForm, setShopCode = saleShopForm, setPrice = salePriceForm, setPoint=salePointForm, setType=saleTypeForm, setRemark = saleRemarkForm)

        ownQuaNow = CusOwnSet.objects.get(ownCusCode = sellingCus, ownSetCode = sellingSet).ownQua
        ownQuaNow -= 1
        CusOwnSet.objects.filter(ownCusCode = sellingCus, ownSetCode = sellingSet).update(ownQua = ownQuaNow)
        saleCodeNow += 1

        return render(request,'success.html', locals())

    return render(request, 'deduct.html', locals())

def deductEmp1(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp1 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp1Code = selectEmp1)

    return render(request,'deductEmpSelectSuc.html', locals())

def sercieSaleEmp1(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp1 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp1Code = selectEmp1)

    return render(request,'backToSericeSale.html', locals())

def deductEmp2(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp2 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp2Code = selectEmp2)

    return render(request,'deductEmpSelectSuc.html', locals())

def sercieSaleEmp2(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp2 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp2Code = selectEmp2)

    return render(request,'backToSericeSale.html', locals())

def deductEmp3(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp3 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp3Code = selectEmp3)

    return render(request,'deductEmpSelectSuc.html', locals())   

def sercieSaleEmp3(request, a):
    global saleCodeNow
    saleCodeComplete = 'S' + format(saleCodeNow, '03d')

    setCusNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCusCode
    setCodeNow = SetSale.objects.get(setSaleCode = saleCodeComplete).setCode
    selectEmp3 = a
    SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setEmp3Code = selectEmp3)

    return render(request,'backToSericeSale.html', locals())

def administrator(request):
    global shopNow
    shopNow = 'SH00'
    return render(request, 'administrator.html', locals())

def stockAdmin(request):
    if 'stockSearchBut' in request.POST:
        searchStock = request.POST['stockSearch']

        queryRes = Stock.objects.filter(stockCode__contains=searchStock) | Stock.objects.filter(stockName__contains=searchStock)

        for res in queryRes:
            if not InStock.objects.filter(inStockCode=res.stockCode, inStockShopCode='SH00'):
                res.stockQua = ''
            elif Stock.objects.get(stockCode=res.stockCode).stockType == '組合':
                res.stockQua = ''
            else:
                resInStockQua = InStock.objects.get(inStockCode=res.stockCode, inStockShopCode='SH00').inStockQua
                res.stockQua = resInStockQua

    return render(request, 'stockAdmin.html', locals())

def report(request):
    if 'exportReport' in request.POST:
        selectSection = request.POST['selectSection']
        selectOrder = request.POST['selectOrder']

        if selectSection == 'seleReport':
            if selectOrder == 'orderDateFromOld':
                saleAll = Sale.objects.all().order_by('saleDate')
            elif selectOrder == 'orderDateFromNew':
                saleAll = Sale.objects.all().order_by('-saleDate')
            return render(request, 'saleReport.html', locals())

        elif selectSection == 'setSaleReport':
            if selectOrder == 'orderDateFromOld':
                saleAll = SetSale.objects.all().order_by('setDate')
            elif selectOrder == 'orderDateFromNew':
                saleAll = SetSale.objects.all().order_by('-setDate')
            return render(request, 'setSaleReport.html', locals())
        
        elif selectSection == 'importReport':
            importAll = importReport.objects.all()
            return render(request, 'importRecord.html', locals())

    return render(request, 'report.html', locals())

def addShop(request):
    shopCodeNow = Shop.objects.all().order_by('-shopCode')[0].shopCode

    if 'completeAddShop' in request.POST:
        shopName = request.POST['shopName']
        shopCode = request.POST['shopCode']

        stockAll = Stock.objects.all()

        for stock in stockAll:
            InStock.objects.create(inStockCode=stock.stockCode, inStockShopCode=shopCode, inStockQua=0)

        
        Shop.objects.create(shopName=shopName, shopCode=shopCode)

    return render(request, 'addShop.html', locals())

def salarySetting(request):
    return render(request, 'salarySetting.html', locals())

def salarySettingING(request, a):
    if a == 'regular':
        if 'searchButt' in request.POST:
            search = request.POST['searchBonusCode']

            searchRes = RegularBonus.objects.filter(bonusName__contains=search) | RegularBonus.objects.filter(bonusCode__contains=search)
        return render(request, 'salarySettingRegular.html', locals())

    if a == 'commission':
        if 'searchButt' in request.POST:
            search = request.POST['searchBonusCode']

            searchRes = Commission.objects.filter(commName__contains=search) | Commission.objects.filter(commCode__contains=search)
        return render(request, 'salarySettingCommission.html', locals())

    if a == 'multiServicePercent':
        if 'searchButt' in request.POST:
            search = request.POST['searchBonusCode']

            searchRes = MultiSevicePercent.objects.filter(MSPName__contains=search) | MultiSevicePercent.objects.filter(MSPCode__contains=search)
        return render(request, 'salarySettingMSP.html', locals())

    return render(request, 'salarySettingING.html', locals())

def editSalarySetting(request, a, b):
    if a == 'regular':
        editSalaryNow = RegularBonus.objects.get(bonusCode=b)
        if 'completeEdit' in request.POST:
            bonusName = request.POST['bonusName']
            bonusCode = request.POST['bonusCode']
            bonusValue = request.POST['bonusValue']

            RegularBonus.objects.filter(bonusCode=b).update(bonusName=bonusName, bonusCode=bonusCode, bonusValue=bonusValue)
            return render(request, 'success.html', locals())

        return render(request, 'editSalaryRegular.html', locals())

    if a == 'MSP':
        editSalaryNow = MultiSevicePercent.objects.get(MSPCode=b)
        if 'completeEdit' in request.POST:
            MSPName = request.POST['MSPName']
            MSPCode = request.POST['MSPCode']
            MSPemp1 = request.POST['MSPemp1']
            MSPemp2 = request.POST['MSPemp2']
            MSPemp3 = request.POST['MSPemp3']

            MultiSevicePercent.objects.filter(MSPCode=b).update(MSPName=MSPName, MSPCode=MSPCode, MSPemp1=MSPemp1, MSPemp2=MSPemp2, MSPemp3=MSPemp3)
            return render(request, 'success.html', locals())

        return render(request, 'editSalaryMSP.html', locals())

    if a == 'commission':
        editCommNow = Commission.objects.get(commCode=b)
        editCLNow = CommLimit.objects.filter(comm_commCode=editCommNow.commCode).order_by('CLIncomeLimit')
        if 'addNewCL' in request.POST:
            newCLLimit = request.POST['newCLLimit']
            newCLPercent = request.POST['newCLPercent']

            CLCodeNow = CommLimit.objects.all().order_by('-CLCode')[0].CLCode
            CLCode = int(CLCodeNow) + 1
            CommLimit.objects.create(comm_commCode=editCommNow.commCode, CLCode=CLCode, CLIncomeLimit=newCLLimit, CLBonusPercent=newCLPercent)

        if 'completeEdit' in request.POST:
            commName = request.POST['commName']
            commCode = request.POST['commCode']

            Commission.objects.filter(commCode=b).update(commName=commName, commCode=commCode)
            return render(request, 'success.html', locals())
        
        return render(request, 'editSalaryCommission.html',  locals())

def addSalarySetting(request, a):
    if a == 'regular':
        codeNow = RegularBonus.objects.all().order_by('-bonusCode')[0].bonusCode
        if 'completeAdd' in request.POST:
            bonusName = request.POST['bonusName']
            bonusCode = request.POST['bonusCode']
            bonusValue = request.POST['bonusValue']

            RegularBonus.objects.create(bonusName=bonusName, bonusCode=bonusCode, bonusValue=bonusValue)
            return render(request, 'success.html', locals())
        return render(request, 'addRegularSalary.html', locals())

    if a == 'MSP':
        codeNow = MultiSevicePercent.objects.all().order_by('-MSPCode')[0].MSPCode
        if 'completeAdd' in request.POST:
            MSPName = request.POST['MSPName']
            MSPCode = request.POST['MSPCode']
            MSPemp1 = request.POST['MSPemp1']
            MSPemp2 = request.POST['MSPemp2']
            MSPemp3 = request.POST['MSPemp3']

            MultiSevicePercent.objects.create(MSPName=MSPName, MSPCode=MSPCode, MSPemp1=MSPemp1, MSPemp2=MSPemp2, MSPemp3=MSPemp3)

            return render(request, 'success.html', locals())
        return render(request, 'addMSPSalary.html', locals())

    if a == 'commission':
        CLCodeNow = 1
        codeNow = Commission.objects.all().order_by('-commCode')[0].commCode
        CLNow = CommLimit.objects.filter(comm_commCode='tmp').order_by('CLIncomeLimit')
        if 'addNewCL' in request.POST:
            newCLLimit = request.POST['newCLLimit']
            newCLPercent = request.POST['newCLPercent']

            CommLimit.objects.create(comm_commCode='tmp', CLCode=CLCodeNow, CLIncomeLimit=newCLLimit, CLBonusPercent=newCLPercent)

        if 'completeAdd' in request.POST:
            commName = request.POST['commName']
            commCode = request.POST['commCode']
            
            CommLimit.objects.filter(comm_commCode='tmp').update(comm_commCode=commCode)
            Commission.objects.create(commName=commName, commCode=commCode)
            return render(request, 'success.html', locals())
        return render(request, 'addCommissionSalary.html', locals())

def deleteCL(request, a, b):
    CommLimit.objects.filter(comm_commCode=a, CLCode=b).delete()
    return render(request, 'blackToEditComm.html', locals())
        
def deleteSalarySetting(request, a, b):
    if a == 'regular':
        RegularBonus.objects.filter(bonusCode=b).delete()
        return render(request, 'backToRegular.html')

    elif a == 'MSP':
        MultiSevicePercent.objects.filter(MSPCode=b).delete()
        return render(request, 'backToMSP.html')

    elif a == 'commission':
        Commission.objects.filter(commCode=b).delete()
        CommLimit.objects.filter(comm_commCode=b).delete()
        return render(request, 'backToCommission.html')

def salaryCount(request):
    global shopNow

    if 'searchThis' in request.POST:
        search = request.POST['searchEmp']
        queryRes = Employee.objects.filter(empCode__contains=search, empShop=shopNow) | Employee.objects.filter(empName__contains=search, empShop=shopNow) | Employee.objects.filter(empPhoneNum__contains=search, empShop=shopNow)

    selectedEmp = SalarySelectEmp.objects.all()

    for emp in selectedEmp:
        empData = Employee.objects.get(empCode=emp.SSEEmpCode)
        emp.empName = empData.empName
        emp.empCode = empData.empCode

    if 'compute' in request.POST:
        dateFrom = request.POST['dateFrom']
        dateTo = request.POST['dateTo']
        SalaryResult.objects.all().delete()
        SalarySelectEmp.objects.all().delete()
        for emp in selectedEmp:
            empName = emp.empName
            salary = 22000  #底薪

            empSale = Sale.objects.filter(saleEmpCode=emp.empCode)
            income = 0
            point = 0
            for sale in empSale:   
                if not sale.saleType == 'set':
                    income += sale.salePrice
                point += sale.salePoint  #商品計積結果
            
            CL003 = CommLimit.objects.filter(comm_commCode='CMM003')
            percentNow = 10
            for cl in CL003:
                if income >= cl.CLIncomeLimit:
                    percentNow = cl.CLBonusPercent
                elif income < cl.CLIncomeLimit:
                    break
            stockIncomeComm = income * percentNow / 100    #商品收入提成結果

            emp1SetSale = SetSale.objects.filter(setEmp1Code=emp.empCode)
            SCIncome1 = 0
            barberIncome1 = 0
            point1 = 0
            for setSale in emp1SetSale:
                if setSale.setType == 'scalpCare':
                    point1 += setSale.setPoint * 50 / 100       
                    SCIncome1 += setSale.setPrice * 50 / 100
                elif setSale.setType == 'barber':
                    point1 += setSale.setPoint * 0 / 100        #專業操作計積結果
                    barberIncome1 += setSale.setPrice * 0 / 100

            emp2SetSale = SetSale.objects.filter(setEmp2Code=emp.empCode)
            SCIncome2 = 0
            barberIncome2 = 0
            point2 = 0
            for setSale in emp2SetSale:
                if setSale.setType == 'scalpCare':
                    point2 += setSale.setPoint * 20 / 100      
                    SCIncome2 += setSale.setPrice * 20 / 100
                elif setSale.setType == 'barber': 
                    point2 += setSale.setPoint * 30 / 100       #洗頭計積結果
                    barberIncome2 += setSale.setPrice * 30 / 100

            emp3SetSale = SetSale.objects.filter(setEmp3Code=emp.empCode)
            SCIncome3 = 0
            barberIncome3 = 0
            point3 = 0
            for setSale in emp3SetSale:
                if setSale.setType == 'scalpCare':
                    point3 += setSale.setPoint * 30 / 100      
                    SCIncome3 += setSale.setPrice * 30 / 100
                elif setSale.setType == 'barber':
                    point3 += setSale.setPoint * 70 / 100       #吹整造型計積結果
                    barberIncome3 += setSale.setPrice * 70 / 100

            SCIncome = SCIncome1 + SCIncome2 + SCIncome3
            CL001 = CommLimit.objects.filter(comm_commCode='CMM001')
            percentNow = 0
            for cl in CL001:
                if SCIncome >= cl.CLIncomeLimit:
                    percentNow = cl.CLBonusPercent
                elif SCIncome < cl.CLIncomeLimit:
                    break
            SCIncomeComm = SCIncome * percentNow / 100    #頭皮護理收入提成結果

            barberIncome = barberIncome1 + barberIncome2 + barberIncome3
            percentNow = 0
            CL002 = CommLimit.objects.filter(comm_commCode='CMM002')
            for cl in CL002:
                if barberIncome >= cl.CLIncomeLimit:
                    percentNow = cl.CLBonusPercent
                elif barberIncome < cl.CLIncomeLimit:
                    break
            barberIncomeComm = barberIncome * percentNow / 100    #洗剪染燙收入提成結果

            result = salary + point + stockIncomeComm + point1 + point2 + point3 + SCIncomeComm + barberIncomeComm

            SalaryResult.objects.create(SRempName=empName, SRsalary=salary, SRpoint=point, SRpoint1=point1, SRpoint2=point2, SRpoint3=point3, SRstockIncomeComm=stockIncomeComm, SRincome=income, SRSCIncomeComm=SCIncomeComm, SRSCIncome=SCIncome, SRbarberIncomeComm=barberIncomeComm, SRbarberIncome=barberIncome, SRresult=result)
        
        SR = SalaryResult.objects.all()
        return render(request, 'countResult.html', locals())

    return render(request, 'salaryCount.html', locals())

def salarySelectEmp(request, a):
    SalarySelectEmp.objects.get_or_create(SSEEmpCode=a)
    return render(request, 'backToSalaryCount.html', locals())

def serviceSale(request):
    global saleCodeNow, shopNow
    damn = shopNow

    saleCodeComplete = 'S' + format(saleCodeNow, '03d')
    SetSale.objects.get_or_create(setSaleCode=saleCodeComplete, setShopCode=shopNow)

    saleAll = SetSale.objects.get(setSaleCode = saleCodeComplete)
    if not saleAll.setCusCode:
        saleAll.setCusCode = ''
    if not saleAll.setCode:
        saleAll.setCode = ''
    if not saleAll.setEmp1Code:
        saleAll.setEmp1Code = ''
    if not saleAll.setEmp2Code:
        saleAll.setEmp2Code = ''
    if not saleAll.setEmp3Code:
        saleAll.setEmp3Code = ''
    
    if saleAll.setCode: 
        stockCode = SetSale.objects.get(setSaleCode=saleCodeComplete).setCode
        tmp = Stock.objects.get(stockCode = stockCode).stockPrice
        oneCoursePrice = int(tmp)

    if 'cusBut' in request.POST:
        searchCus = request.POST['cusSearch']
        cusSearchRes = Customers.objects.filter(cusCode__contains=searchCus) | Customers.objects.filter(cusName__contains=searchCus) | Customers.objects.filter(cusPhoneNum__contains=searchCus) 

    if 'searchBut' in request.POST:
        searchSevice = request.POST['searchSevice']
        searchRes = Stock.objects.filter(stockCode__contains=searchSevice, stockType='服務') | Stock.objects.filter(stockName__contains=searchSevice, stockType='服務')

    if 'empBut1' in request.POST:
        search = request.POST['empSearch']
    
        queryRes1 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes1 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes1 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes1:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut1' in request.POST:
        search = request.POST['empSearch']
    
        queryRes1 = Employee.objects.filter(empName__contains = search)
        queryRes1 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes1 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes1:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empBut2' in request.POST:
        search = request.POST['empSearch']
    
        queryRes2 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes2 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes2:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut2' in request.POST:
        search = request.POST['empSearch']
    
        queryRes2 = Employee.objects.filter(empName__contains = search)
        queryRes2 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes2 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes2:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empBut3' in request.POST:
        search = request.POST['empSearch']
    
        queryRes3 = Employee.objects.filter(empName__contains = search, empShop = shopNow)
        queryRes3 |= Employee.objects.filter(empPhoneNum__contains = search, empShop = shopNow)
        queryRes3 |= Employee.objects.filter(empCode__contains = search, empShop = shopNow)

        for res in queryRes3:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 

    if 'empAllBut3' in request.POST:
        search = request.POST['empSearch']
    
        queryRes3 = Employee.objects.filter(empName__contains = search)
        queryRes3 |= Employee.objects.filter(empPhoneNum__contains = search)
        queryRes3 |= Employee.objects.filter(empCode__contains = search)

        for res in queryRes3:
            if res.empShop == 'SH01':
                res.empShop = '旗艦店'
            else:
                res.empShop = '崇德店' 
    if 'completeDeduct' in request.POST:
        saleDateForm = request.POST['saleDate']
        saleShopForm = request.POST['saleShop']
        salePriceForm = request.POST['salePrice']
        salePointForm = request.POST['salePoint']
        saleTypeForm  = request.POST['selectSaleType']
        saleRemarkForm = request.POST['saleRemark']

        SetSale.objects.filter(setSaleCode = saleCodeComplete).update(setDate = saleDateForm, setShopCode = saleShopForm, setPrice = salePriceForm, setPoint=salePointForm, setType=saleTypeForm, setRemark = saleRemarkForm)

        saleCodeNow += 1

        return render(request,'success.html', locals())

    return render(request, 'serviceSale.html', locals())
