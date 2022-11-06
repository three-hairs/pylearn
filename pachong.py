import requests
import datetime
date = str(datetime.datetime.now().strftime('%Y/%m/%d'))
print(date)
import  urllib
#
# # resp = requests.get('http://form.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq')
# # # print(resp.url)
# # # print(resp.headers)
# # cook = resp.headers['Set-Cookie']
# # print(cook)
#
# post_addr1 = "http://ids.hhu.edu.cn/amserver/UI/Login"
# params = {'goto': 'http://form.hhu.edu.cn/pdc/form/list'}
#
# #构造头部信息
# post_header1 = {
#      'Host': 'ids.hhu.edu.cn',
#      'Connection': 'keep-alive',
#      'Content-Length': '159',
#      'Cache-Control': 'max-age=0',
#      'Upgrade-Insecure-Requests': '1',
#      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#      'X-Requested-With': 'XMLHttpRequest',
#      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
#      'Content-Type': 'application/x-www-form-urlencoded',
#      'Origin': 'http://ids.hhu.edu.cn',
#      'Referer': 'http://form.hhu.edu.cn/pdc/form/list',
#      'Accept-Encoding': 'gzip, deflate',
#      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
# }
#
# #构造登录数据
# post_data1 = {'IDToken0': '',
#               'IDToken1': '1709040221',
#               'IDToken2': 'lyj123456',
#               'IDButton': 'Submit',
#               'gpto': 'http://form.hhu.edu.cn/pdc/form/list',
#               'encoded': 'true',
#               'inputCode': '',
#               'gx_charset': 'UTF-8',
#               }
#
# #发送post请求登录网页
# # z = requests.post(post_addr, data=post_data, headers=post_header)
# z1 = requests.post(post_addr1, headers=post_header1, data=post_data1, params=params)
# print(z1.headers)
# print(z1.status_code)
# print(z1.url)
# print(z1.headers)
# cook = z1.headers['Set-Cookie']
# print(cook)
# print(z1.text)
#
#
# # resp = requests.get('http://form.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq')
# # # print(resp.url)
# # print(resp.headers)
# # cook = resp.headers['Set-Cookie']
# # print(resp.status_code)
# # print(resp.text)


#登录地址
post_addr2 = "http://form.hhu.edu.cn/pdc/formDesignApi/dataFormSave?wid=A335B048C8456F75E0538101600A6A04&userId=1709040221"

#构造头部信息
post_header2 ={
    'Host': 'form.hhu.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '822',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://form.hhu.edu.cn',
    'Referer': 'http://form.hhu.edu.cn/pdc/formDesignApi/S/gUTwwojq',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'JSESSIONID=C37E738AE0632CCCD385F10897D412D8; amlbcookie=01; iPlanetDirectoryPro=AQIC5wM2LY4SfczGCNQ7RuC%2B2Ey0kS6XT34za6XJyGr1R%2FM%3D%40AAJTSQACMDE%3D%23',
}

#构造登录数据
post_data2 = {'DATETIME_CYCLE': date,
             'XGH_336526': '1709040221',
             'XM_1474': '梁云健',
             'SFZJH_859173': '130705199801050017',
             'SELECT_941320': '地学院',
             'SELECT_459666': '2017级',
             'SELECT_814855': '地信',
             'SELECT_525884': '地信17_2',
             'SELECT_125597': '江宁校区教学区24舍',
             'TEXT_950231': '623',
             'TEXT_937296': '15295773617',
             'RADIO_853789': '否',
             'RADIO_43840': '否',
             'RADIO_579935': '健康',
             'RADIO_138407': '否',
             'RADIO_546905': '否',
             'RADIO_314799': '否',
             'RADIO_209256': '否',
             'RADIO_836972': '否',
             'RADIO_302717': '否',
             'RADIO_701131': '否',
             'RADIO_438985': '否',
             'RADIO_467360': '是',
             'PICKER_956186': '河北省,张家口市,宣化区',
             'TEXT_434598': '',
             'TEXT_515297': '',
             'TEXT_752063': '',
             }

#发送post请求登录网页

z2 = requests.post(post_addr2, data=post_data2, headers=post_header2, allow_redirects=False)

print(z2.status_code)
h = z2.text
print(h)

