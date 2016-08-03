#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

菜单添加窗口

'''

from application.controller.quxian import QuxianContorller
from application.controller.memberquery import MemberqueryContorller
from application.controller.tixian import TiXian
from application.controller.zhuanzhang import ZhuanzhangContorller
from application.controller.bangka import BangKa
from application.controller.bindingcard import BindingCardController
from application.controller.orderlist import OrderListController
from application.controller.goods import GoodsController
from application.controller.orderAdd import OrderAddController
from application.controller.suppliers import SuppliersController
from application.controller.membermanager import MembermanagerController
from application.controller.servicequery import ServiceQueryController
from application.controller.losingcard import LosingCardController
from application.controller.quyuxiaoshoutongji import QuYuScale
from application.controller.storagelist import StorageList
from application.controller.storagetypelist import StorageTypeListController
from application.controller.systemseting import Systemseting
from application.controller.showshot import Showshot
from application.controller.addcard import AddcardContorller
from application.controller.servicequery import ServiceQueryController
# from application.controller.shangpinxiaoshoumingxi import ShangPinXiaoShou

#from application.controller.editmember import EditMemberController
#from application.controller.congZhi import  CongZhiContorller
from application.controller.addMember import AddMemberController
#from application.controller.showshot import Showshot
#from application.controller.customerAccount import CustomerAccount
#from application.controller.companyreport import CompanyReportContorller
from application.controller.rateset import RateSet
from application.controller.rateslist import RatesList
from application.controller.grouplist import GroupListController
from application.controller.userlist import UserListController
from application.controller.interestclear import InterestClear
from application.controller.congZhi import CongZhiContorller
from application.controller.editmember import EditMemberController
from application.controller.companyreport import CompanyReportContorller
from application.controller.customerAccount import CustomerAccount
from application.controller.cardpwd import CardPwdContorller
from application.lib.Commethods import *
from application.controller.addcard import AddcardContorller
from application.controller.memberclear import MemberClearController
from application.controller.stocksearch import StockSearchController
from application.controller.shopgoods import ShopGoodsController
from application.controller.shopstockin import ShopStockInController
from application.controller.goodsscaleAccount import GoodsScaleAccount
from application.controller.shangchengdingdanAccount import ShangChengDingDanAccount
from application.controller.shopgoodsstockinlist import ShopGoodsStockInList
from application.controller.zhuanzhangAccount import ZhuanZhangAccount
from application.controller.setting import SettingController
from application.controller.payTypeSettings import PayTypeSettings
from application.controller.paymentManager import PaymentManager
from application.controller.alterMyPassword import AlterMyPassword
from application.controller.shopsys import ShopSysController
from application.controller.pushNews import PushNews
from application.controller.upver import upVerController

class MainOrder:
    _orderList = []
    def __init__(self):
        pass
    @staticmethod
    def _initOrder():
        if len(MainOrder._orderList) > 0:
            return
        
        #主页面
        mainBoard = []
        mainBoard.append({'img':"./img/newIcos/newMember.png","title":u"开户","window":AddMemberController})
        mainBoard.append({'img':"./img/newIcos/recharge.png","title":u"充值","window":CongZhiContorller})
        mainBoard.append({'img':"./img/newIcos/companyReport.png","title":u"公司资金管理","window":CompanyReportContorller})
        mainBoard.append({'img':"./img/newIcos/queryMember.png","title":u"客户查询","window":MemberqueryContorller})
        mainBoard.append({'img':"./img/newIcos/take.png","title":u"提现","window":QuxianContorller})
        mainBoard.append({'img':"./img/newIcos/memberReport.png","title":u"客户资金管理","window":CustomerAccount})
        
        #账户管理
        zhgl = []
        zhgl.append({'img':"./img/newIcos/newMember.png","title":u"开户","window":AddMemberController})
        zhgl.append({'img':"./img/newIcos/queryMember.png","title":u"客户查询","window":MemberqueryContorller})
        zhgl.append({'img':"./img/newIcos/alterMember.png","title":u"修改客户资料","window":EditMemberController})
        zhgl.append({'img':"./img/newIcos/alterMemberPassword.png","title":u"修改客户密码","window":CardPwdContorller})
        zhgl.append({'img':"./img/newIcos/logoff.png","title":u"注销","window":MemberClearController})

        #金荣卡管理
        jrkgl = []
        jrkgl.append({'img':'./img/newIcos/addCard.png', 'title':u'添加', 'window':AddcardContorller})
        jrkgl.append({'img':"./img/newIcos/bindCard.png", "title":u"绑定", "window":BindingCardController})
        jrkgl.append({'img':"./img/newIcos/queryCard.png", "title":u"查询", "window":ServiceQueryController})
        jrkgl.append({'img':"./img/newIcos/lossCard.png", "title":u"卡挂失", "window":LosingCardController})
        
        #资金管理
        zjgl = []
        zjgl.append({'img':"./img/newIcos/recharge.png","title":u"充值","window":CongZhiContorller})
        zjgl.append({'img':"./img/newIcos/take.png","title":u"提现","window":QuxianContorller})
        zjgl.append({'img':"./img/newIcos/transfer.png","title":u"转账","window":ZhuanzhangContorller})
        
        #报表管理
        bbgl = []
        bbgl.append({'img':"./img/newIcos/companyReport.png","title":u"公司资金管理","window":CompanyReportContorller})
        bbgl.append({'img':"./img/newIcos/memberReport.png","title":u"客户资金管理","window":CustomerAccount})
        bbgl.append({'img':"./img/newIcos/inAndOut.png","title":u"流水账","window":ZhuanZhangAccount})
#         bbgl.append({'img':"./img/newIcos/salesManager.png","title":u"销售管理","window":GoodsScaleAccount})
        
        #利息管理
        lxgl = []
        lxgl.append({'img':"./img/newIcos/setRate.png","title":u"设置利息","window":RateSet})
        lxgl.append({'img':"./img/newIcos/seeRate.png","title":u"查看利息","window":RatesList})
        lxgl.append({'img':"./img/newIcos/payRate.png","title":u"利息结算","window":InterestClear}) 
         
        # 缴费管理
        jfgl = []
        jfgl.append({'img':"./img/newIcos/setPaymentType.png","title":u"缴费项目设置","window":PayTypeSettings})
        jfgl.append({'img':"./img/newIcos/paymentManager.png","title":u"缴 费 管 理","window":PaymentManager})
        
        #基本资料设置
        jbzlwh = []
        jbzlwh.append({'img':"./img/newIcos/setMemberType.png","title":u"类别设置","window":Systemseting})
        jbzlwh.append({'img':"./img/newIcos/userGroup.png","title":u"用户组","window":GroupListController})
        jbzlwh.append({'img':"./img/newIcos/user.png","title":u"用户","window":UserListController})
        jbzlwh.append({'img':"./img/newIcos/storageList.png","title":u"仓库列表","window":StorageList})
        jbzlwh.append({'img':"./img/newIcos/alterMember.png","title":u"修改客户资料","window":EditMemberController})
        jbzlwh.append({'img':"./img/newIcos/storageTypeList.png","title":u"仓库类型列表","window":StorageTypeListController})
        jbzlwh.append({'img':"./img/newIcos/setMsg.png","title":u"短信设置","window":Showshot})
        jbzlwh.append({'img':"./img/newIcos/msgManager.png","title":u"短信管理","window":PushNews})
        
        #系统设置
        settings = []
        settings.append({'img':'./img/newIcos/settings.png', 'title':u'本机设置', 'window':SettingController})
        settings.append({'img':'./img/newIcos/alterMyPassword.png', 'title':u'修改用户密码', 'window':AlterMyPassword})
        settings.append({'img':'./img/newIcos/update.png', 'title':u'系统更新', 'window':upVerController})
        settings.append({'img':'./img/newIcos/clock.png', 'title':u'锁屏', 'window':ShopSysController})
        
        #商城
        shangcheng = []
        shangcheng.append({'img':"./img/shangchengdingdan.png","title":u"商城订单","window":ShangChengDingDanAccount})
        
        #进销存管理
        jxcgl = []
#         jxcgl.append({'img':"./img/ddgl.png","title":u"订单管理","window":OrderListController})
#         jxcgl.append({'img':"./img/ddfb.png","title":u"订单添加","window":OrderAddController})
#         jxcgl.append({'img':"./img/spzl.png","title":u"商品资料","window":GoodsController})
#         jxcgl.append({'img':"./img/gys.png","title":u"供应商列表","window":SuppliersController})
#         jxcgl.append({'img':"./img/btn_kucun.png","title":u"库存查询","window":StockSearchController})
        jxcgl.append({'img':"./img/gys.png","title":u"供应商列表","window":MembermanagerController})
        jxcgl.append({'img':"./img/newIcos/goods.png","title":u"商城商品资料","window":ShopGoodsController})
        jxcgl.append({'img':"./img/shangpinruku.png","title":u"商城商品入库","window":ShopStockInController})
        jxcgl.append({'img':"./img/stockinlist.png","title":u"商品入库列表","window":ShopGoodsStockInList})
        
        MainOrder._orderList.append(mainBoard)
        MainOrder._orderList.append(zhgl)
        MainOrder._orderList.append(jrkgl)
        MainOrder._orderList.append(zjgl)
        MainOrder._orderList.append(bbgl)
        MainOrder._orderList.append(lxgl)
        MainOrder._orderList.append(jfgl)
        if ControllerAction.appdata['user']['user_id'] == 1:
            MainOrder._orderList.append(jbzlwh)
        MainOrder._orderList.append(settings)
#         MainOrder._orderList.append(shangcheng)
        
    @staticmethod
    def getLeftOrder ():
        if ControllerAction.appdata['user']['user_id'] == 1:
            return [u'主页面',u"账户管理",u'金荣卡管理',u"资金管理",u"报表管理",
                    u"利息管理",u'缴费管理',u"基本资料设置",u"系统设置"]
        else:
            return [u'主页面',u"账户管理",u'金荣卡管理',u"资金管理",u"报表管理",
                    u"利息管理",u'缴费管理',u"系统设置"]
        
    @staticmethod
    def order(id):
        MainOrder._initOrder()
        try:
            return MainOrder._orderList[id]
        except:
            return ()
    
    @staticmethod
    def addMainTab(maintab):
        if(maintab.layout()) == None:
            maintab.gridLayout = QGridLayout(maintab)
        maintab.clearList()
        maintab.gridLayout = maintab.layout()
    