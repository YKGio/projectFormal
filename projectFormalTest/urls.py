"""projectFormalTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appFormalTest import views as appViews

urlpatterns = [
    path('', appViews.login),
    path('index/<str:a>', appViews.index),
    path('redirectIndex/', appViews.redirectIndex),

    path('administrator/', appViews.administrator),
    path('stockAdmin/', appViews.stockAdmin),
    path('adminImport/<str:a>', appViews.adminImport),
    path('addShop/', appViews.addShop),
    
    path('cus/', appViews.cus),
    path('editCus/<str:a>/', appViews.editCus),
    path('addCus/', appViews.addCus),

    path('emp/', appViews.emp),
    path('editEmp/<str:a>/', appViews.editEmp),
    path('addEmp/', appViews.addEmp),

    path('stock/', appViews.stock),
    path('editStock/<str:a>/', appViews.editStock),
    path('addStock/', appViews.addStock),
    path('selectImport/<str:a>', appViews.selectImport),
    path('editCombineStockAdd/<str:a>/<str:b>/', appViews.editCombineStockAdd),
    path('editCombineStockDelete/<str:a>/<str:b>/', appViews.editCombineStockDelete),

    path('combineStock/', appViews.combineStock),
    path('combineStock/<str:a>/', appViews.combining),
    path('sucCombine/', appViews.sucCombine),
    path('combineStockDelete/<str:a>/<str:b>', appViews.combineStockDelete),
    
    path('sale/', appViews.sale),
    path('saleCus/<str:a>/', appViews.saleCus),
    path('saleStock/<str:a>/', appViews.saleStock),
    path('saleEmp/<str:a>/', appViews.saleEmp),
    path('completeSale/', appViews.completeSale),

    path('serviceSale/', appViews.serviceSale),
    path('setSaleCus/<str:a>/', appViews.setSaleCus),
    path('setSaleStock/<str:a>/', appViews.setSaleStock),
    path('sercieSaleEmp1/<str:a>/', appViews.sercieSaleEmp1),
    path('sercieSaleEmp2/<str:a>/', appViews.sercieSaleEmp2),
    path('sercieSaleEmp3/<str:a>/', appViews.sercieSaleEmp3),
    
    path('setSale/', appViews.setSale),
    path('sellingSet/<str:a>', appViews.setllingSet),
    path('deduct/<str:a>/<str:b>/', appViews.deduct),
    path('deductEmp1/<str:a>/', appViews.deductEmp1),
    path('deductEmp2/<str:a>/', appViews.deductEmp2),
    path('deductEmp3/<str:a>/', appViews.deductEmp3),

    path('report/', appViews.report),
    path('salarySetting/', appViews.salarySetting),
    path('salarySetting/<str:a>/', appViews.salarySettingING),
    path('editSalarySetting/<str:a>/<str:b>/', appViews.editSalarySetting),
    path('addSalarySetting/<str:a>/', appViews.addSalarySetting),
    path('deleteCL/<str:a>/<str:b>/', appViews.deleteCL),
    path('deleteSalarySetting/<str:a>/<str:b>/', appViews.deleteSalarySetting),

    path('salaryCount/', appViews.salaryCount),
    path('salarySelectEmp/<str:a>', appViews.salarySelectEmp),

    path('delete/<str:a>/', appViews.delete),
    path('deleteStock/<str:a>/', appViews.deleteStock),

    path('admin/', admin.site.urls),
]
