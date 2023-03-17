# 发邮件相关的库
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
# 抓数据相关的库
import requests
from bs4 import BeautifulSoup
import xlwt
import time


# 获取第一页的内容
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


tcshuju = []
fcshuju = []

html = get_one_page('https://www.17500.cn/')
soup = BeautifulSoup(html, 'lxml')

tc = []
for item in soup.find_all(lotid="pl5"):
    tc.append(item.select('b'))
newtc = tc[0][0].text + ':' + tc[0][1].text + tc[0][2].text + tc[0][3].text + tc[0][4].text + tc[0][5].text

fc = []
for item in soup.find_all(lotid="3d"):
    fc.append(item.select('b'))
newfc = fc[0][0].text + ':' + fc[0][1].text + fc[0][2].text + fc[0][3].text

f = open("tcpl5.txt", 'r')
tcshuju = f.read().splitlines()
for cc in tcshuju:
    if cc=='':
        tcshuju.remove(cc)
if newtc != tcshuju[99]:
    tcshuju.append(newtc)  # 追加新的一行
    del tcshuju[0]  # 删除第一行
    fw = open('tcpl5.txt', 'w')
    sj: str
    for sj in tcshuju:
        fw.write(sj + '\n')
    fw.close()
f.close()

f = open("fc3d.txt", 'r')
fcshuju = f.read().splitlines()
for cc in fcshuju:
    if cc=='':
        fcshuju.remove(cc)
if newfc != fcshuju[99]:
    fcshuju.append(newfc)  # 追加新的一行
    del fcshuju[0]  # 删除第一行
    fw = open('fc3d.txt', 'w')
    sj: str
    for sj in fcshuju:
        fw.write(sj + '\n')
    fw.close()
f.close()

fcall = []
for fu in fcshuju:
    qihao = fu[0:7]
    kaijianghao = fu[-3:]
    spaixu = "".join((lambda x: (x.sort(), x)[1])(list(kaijianghao)))
    # 计算跨 和尾
    hw = int(spaixu[0]) + int(spaixu[1]) + int(spaixu[2])
    if hw >= 20:
        hw = hw - 20
    if hw >= 10 and hw < 20:
        hw = hw - 10
    kua = int(spaixu[2]) - int(spaixu[0])
    spaixu = spaixu + ' ' + str(kua) + ' ' + str(hw)
    # 定位两码
    m1 = int(kaijianghao[0]) + int(kaijianghao[1])
    if m1 >= 10:
        m1 = m1 - 10
    m2 = int(kaijianghao[0]) + int(kaijianghao[2])
    if m2 >= 10:
        m2 = m2 - 10
    m3 = int(kaijianghao[1]) + int(kaijianghao[2])
    if m3 >= 10:
        m3 = m3 - 10
    m = str(m1) + str(m2) + str(m3)
    # 组装
    fcall.append(qihao + ':' + spaixu + ' ' + kaijianghao + ' ' + m)
fcall.reverse()

tcall = []
for ti in tcshuju:
    qihao = ti[0:7]
    kaijianghao = ti[-5:]
    spaixu = kaijianghao[0:3]
    spaixu = "".join((lambda x: (x.sort(), x)[1])(list(spaixu)))
    # 计算跨 和尾
    hw = int(spaixu[0]) + int(spaixu[1]) + int(spaixu[2])
    if hw >= 20:
        hw = hw - 20
    if hw >= 10 and hw < 20:
        hw = hw - 10
    kua = int(spaixu[2]) - int(spaixu[0])
    spaixu = spaixu + ' ' + str(kua) + ' ' + str(hw)
    # 定位两码
    m1 = int(kaijianghao[0]) + int(kaijianghao[1])
    if m1 >= 10:
        m1 = m1 - 10
    m2 = int(kaijianghao[0]) + int(kaijianghao[2])
    if m2 >= 10:
        m2 = m2 - 10
    m3 = int(kaijianghao[1]) + int(kaijianghao[2])
    if m3 >= 10:
        m3 = m3 - 10
    m = str(m1) + str(m2) + str(m3)
    # 组装
    tcall.append(qihao + ':' + spaixu + ' ' + kaijianghao + ' ' + m)
tcall.reverse()


# 格式化出需要的数据
def shuchu(caipiao):
    resaultStr = []
    jieguo = ''
    for j in range(1, 11):
        for i in range(0, j * 4, j):
            resaultStr.append(caipiao[i + j - 1])
    resaultStrList = resaultStr
    for c in range(39, -1, -1):
        jieguo = jieguo + resaultStrList[c] + '\n'
        if c % 4 == 0:
            jieguo = jieguo + '\n'
    return jieguo


# 准备发邮件
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def readySendmail(jieguo):
    from_addr = '12975520@qq.com'
    password = 'nuxemtsztrnjbjhd'  # 密码算法
    to_addr = '793450641@qq.com'
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(jieguo, 'plain', 'utf-8')
    msg['From'] = _format_addr('神龙 <%s>' % from_addr)
    msg['To'] = _format_addr('观察员 <%s>' % to_addr)
    msg['Subject'] = Header('最新数据', 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def run_Task():
    fucaijieguo = shuchu(fcall)
    ticaijieguo = shuchu(tcall)
    #readySendmail('福彩3D' + '\n' + fucaijieguo + '\n' + '体彩排列三' + '\n' + ticaijieguo + '\n' + '\n' + '数据来自乐彩网')
    print('福彩3D' + '\n' + fucaijieguo + '\n' + '体彩排列三' + '\n' + ticaijieguo + '\n' + '\n' + '数据来自乐彩网')




run_Task()
