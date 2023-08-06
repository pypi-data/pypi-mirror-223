import json
import time
import shutil
import string
import random
import re
import configparser
from pathlib import Path
from wfsx.parseexcel import ParseExcel
from wfsx.apivalid import Validations
from wfsx.ghelper import update_values_nested
from datetime import date
from cdxg import testdata

mypath = Path.cwd()  # .parent
# print(mypath)
config = configparser.ConfigParser()
data_file_path = mypath / 'config.ini'
config.read(mypath / 'config.ini')


def dumpData(apiselect, getalljson):
    with open(apiselect, 'w', encoding='utf-8') as jsonfile:
        json.dump(getalljson, jsonfile, ensure_ascii=False, indent=4)
    time.sleep(1)
    # log.info(getalljson)
    with open(apiselect) as data_json_file:
        data_loaded = json.load(data_json_file)
    # print(data_loaded)
    return data_loaded


def data_required(datafile):
    # print('*******' + str(datafile) + '*********')
    # testdata_file = str(datafile) + '.json'
    with open(datafile) as data_json_file:
        data_loaded = json.load(data_json_file)
    # print(data_loaded)
    return data_loaded


def get_domain_id(datafile):
    getdata, get_data = data_required(datafile), None
    getdomain = getdata['data']['userInfo']['domain']
    for lenx in range(0, len(getdomain)):
        if getdomain[lenx]['current']:
            get_data = getdomain[lenx]['id']
            break
    return get_data


def get_data_json_info(getalljson, datafile):
    with open('./test_data/json_data/' + str(datafile) + '_json_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(getalljson, jsonfile, ensure_ascii=False, indent=4)
    time.sleep(1)


def getcURL(methd, url, data, param):
    if param != 'None' and methd == 'GET':
        url = url + '?' + param

    if data == 'None' or data == {}:
        data = ''

    command = "curl -X '" + str(methd) + "' '" + str(url) + "'"
    for key, value in json.loads(config.get("Cookie_Headers", "xHeaders")).items():
        command += " -H '" + str(key) + ":" + str(value) + "'"
    if methd != 'GET':
        command += " -d '" + str(data) + "'"
    return command


def get_results(xlcreate, roles, testcase, tendpoint, testdata, testparams, exResults, acResults, results, fontx,
                elapsed_secs, comments='', sprints=''):
    reportpath = ParseExcel(excel_path=xlcreate)
    reportpath.set_sheet_by_name('API_Results')
    get_total_rows = reportpath.get_max_row_no()
    try:
        reportpath.write_cell_content_colored(get_total_rows + 1, 1, get_total_rows - 2)
        reportpath.write_cell_content_colored(get_total_rows + 1, 2, roles)
        reportpath.write_cell_content_colored(get_total_rows + 1, 3, testcase)
        reportpath.write_cell_content_colored(get_total_rows + 1, 4, tendpoint)
        reportpath.write_cell_content_colored(get_total_rows + 1, 5, testdata)
        reportpath.write_cell_content_colored(get_total_rows + 1, 6, testparams)
        reportpath.write_cell_content_colored(get_total_rows + 1, 7, str(exResults))
        reportpath.write_cell_content_colored(get_total_rows + 1, 8, str(acResults))
        if results == 'PASSED':
            reportpath.write_cell_content_colored(get_total_rows + 1, 9, '✅', font=fontx)
        else:
            reportpath.write_cell_content_colored(get_total_rows + 1, 9, '❌', font=fontx)
        # reportpath.write_cell_content_colored(get_total_rows + 1, 9, results, font=fontx)
        reportpath.write_cell_content_colored(get_total_rows + 1, 10, comments)
        reportpath.write_cell_content_colored(get_total_rows + 1, 11, elapsed_secs)
        reportpath.write_cell_content_colored(get_total_rows + 1, 12, sprints)
    except Exception as e:
        if ValueError:
            for xna in acResults:
                reportpath.write_cell_content_colored(get_total_rows + 1, 5, xna)
        # print(str(e))


def Create_New_Report(report):
    otime = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    reportfolderpath = report + "_" + otime + ".xlsx"
    shutil.copy(mypath / 'reports' / 'api_results.xlsx', mypath / 'reports' / reportfolderpath)
    return mypath / 'reports' / reportfolderpath


def get_tags(rtype='Smoke'):
    config.read(data_file_path)
    gettag = config['Tags']
    test_tags = gettag['run_type']
    if rtype is not None:
        rty = rtype.split(',')
        ttags = test_tags.split(',')
        if len(rty) == 1 and len(ttags) >= 1:
            if test_tags.find(rty[0]) != -1:
                t_xgs = None
                for txgs in ttags:
                    if txgs == rty[0]:
                        t_xgs = txgs
                return t_xgs
        else:
            xtype, txn = [], None
            for tgs in ttags:
                for rxt in rty:
                    if rxt == tgs:
                        txn = rxt
                        break
                if txn == tgs:
                    xtype.append('Y')
                else:
                    xtype.append('N')
            if 'Y' in list(set(xtype)):
                return rtype


def getTypesplit(xType, get_data, gtd, tdata):
    global charsx, gxdatax
    today = date.today()
    date_string = today.strftime('%Y_%m_%d')
    if xType.startswith('@'):
        gSplit = xType.split('^')
        for xlen in range(1, len(gSplit[1])):
            xSplit = gSplit[1].split(',')
            pSplit = gSplit[2].split(',')
            for xlenn in range(0, len(xSplit)):
                if xSplit[xlenn] == 'Addx':
                    gcspt = pSplit[xlenn].split('=')
                    if '|' in gcspt[1]:
                        getcharsx = gcspt[1].split('*')
                        mxchars = mixedcharacters(k=int(getcharsx[1]))
                    else:
                        mxchars = gcspt[1] + '_' + date_string
                    get_data[str(gcspt[0])] = str(mxchars)
                elif xSplit[xlenn] == 'Add':
                    gkey, gvalue = pSplit[xlenn].split('=')
                    if '|' in gvalue and '*' in gvalue and '.' not in gkey:
                        getcharsx = gvalue.split('*')
                        charsx = mixedcharacters(k=int(getcharsx[1]))
                        get_data[str(gkey)] = charsx
                    elif '.' in gkey:
                        cname, kname = gkey.split('.')
                        charsx = update_values_nested(get_data, cname, kname, gvalue)
                        get_data = charsx
                    else:
                        mxchars = gvalue
                        if mxchars == '[]':
                            charsx = []
                        else:
                            charsx = str(mxchars)
                        get_data[str(gkey)] = charsx
                elif xSplit[xlenn] == 'Extract':
                    gcspt = pSplit[xlenn].split('=')
                    # print(gcspt)
                    gxdatax = getExtract(xdata=gcspt[1], tdata=tdata)
                    get_data[str(gcspt[0])] = gxdatax
                elif xSplit[xlenn] == 'Dadd':
                    keyx, valuesx = pSplit[xlenn].split('=')
                    rpl = valuesx.replace('*', ',')
                    xType_dict = json.loads(rpl)
                    get_data[keyx] = xType_dict
                elif xSplit[xlenn] == 'Ladd':
                    grt = []
                    gcspt = pSplit[xlenn].split('=')
                    gmt = gcspt[1].split('-')
                    try:
                        for xgmt in gmt:
                            if '.' in xgmt:
                                grt.append(float(xgmt))
                            else:
                                grt.append(int(xgmt))
                    except Exception:
                        for xgmt in gmt:
                            grt.append(xgmt)
                    get_data[str(gcspt[0])] = grt
                else:
                    if xSplit[xlenn] == 'Remove':
                        if '=' in pSplit[xlenn]:
                            gcspt = pSplit[xlenn].split('=')
                            if '*' in gcspt[0]:
                                attrN = gcspt[0].split('*')
                                for xattr in attrN:
                                    gxdatax = getremove(xdata=gcspt[1], tdata=tdata, getn=get_data)
                                delgtx = attrN
                            else:
                                gxdatax = getremove(xdata=gcspt[1], tdata=tdata, getn=get_data)
                                delgtx = gcspt[0]
                            ggx = []
                            for xgtx in gxdatax:
                                if type(delgtx) == list:
                                    for delg in delgtx:
                                        del xgtx[delg]
                                        ggx.append(xgtx)
                                else:
                                    if type(xgtx) == dict:
                                        del xgtx[delgtx]
                                        ggx.append(xgtx)
                                    else:
                                        for xgt in xgtx:
                                            del xgt[delgtx]
                                            ggx.append(xgt)
                            if len(ggx) >= tdata:
                                ggx = random.sample(ggx, tdata)
                                # print(ggx)
                            if '|' in gcspt[1]:
                                aName = gcspt[1].split('|')
                                get_data[str(aName[3])] = ggx
                            else:
                                get_data[str(gcspt[1])] = ggx
                        else:
                            del get_data[pSplit[xlenn]]
            return json.dumps(dict(get_data))
    else:
        if gtd:
            return json.dumps(dict(get_data))
        else:
            return xType

def generate_test_api(generate_test_api, sheetname=None, exeLine=None):
    sLine, eLine = 2, None
    getxcl = ParseExcel(generate_test_api)
    getallxm = getxcl.get_sheetnames()
    getxmall = []
    if sheetname:
        for y in eval(sheetname):
            for x in range(0, len(getallxm)):
                if x == y or getallxm[x] == y:
                    getxmall.append(getallxm[x])
                    break
        getallxm = getxmall
    if exeLine:
        if ',' in exeLine:
            sLine, eLine = str(exeLine).split(',')
        else:
            sLine, eLine = exeLine, None
    pathdata_file = mypath / 'test_dir' / 'test_onefms_api.py'
    with open(pathdata_file, 'w') as f:
        f.write('from cdxg import file_data\n')
        f.write('from utils.api import *\n')
        f.write('from cdxg.logging import log\n')
        f.write('from wfsx.common import get_tags, Create_New_Report, get_results, getepoint\n')
        f.write('from utils.apiexecutor import apiSteps\n\n')

        f.write('mypath = Path.cwd()\n')
        f.write('config = configparser.ConfigParser()\n')
        f.write('config.read(mypath / "config.ini")\n')
        f.write('test_case_data = config.get("test_data_xl", "test_case_data_xl")\n')
        f.write('generate_test_ap = mypath / test_case_data\n')
        f.write('xHeaders = json.loads(config.get("Cookie_Headers", "xHeaders"))\n')
        f.write('xreport = config.get("App_Sys", "vehiclems")\n')
        f.write('reportpath = Create_New_Report(report=xreport)\n')
        f.write('test_tags = config.get("Tags", "run_type")\n')
        f.write('line = ' + str(sLine) + '\n')
        f.write('end_line = ' + str(eLine) + '\n\n\n')

        for getxl in getallxm:
            if getxl != 'Usage':
                f.write('class Api_Onefms_' + str(getxl) + '(apicall):\n\n')
                f.write('\tdef start(self):\n')
                f.write('\t\tself.maxDiff = None\n\n')
                f.write(
                    '\t@file_data(str(generate_test_ap), line=line, end_line=end_line, sheet="' + str(getxl) + '")\n')
                f.write(
                    '\tdef test_' + getxl + '_api(self, testcase, tcdef, xendpoint, xmethod, payload, params, testdata,\n')
                f.write('\t\t\t\t\t\t\texresults, scvarib, ctype, results, rtype, depend, sprints):\n')
                f.write('\t\t"""*"""\n')
                f.write('\t\tlog.info("***" + str(tcdef) + "_" + str(testcase) + "***")\n')
                f.write('\t\tconfig.read(mypath / "utils" / "endpointapi.ini")\n')
                f.write("\t\tif '/' in xendpoint:\n")
                f.write("\t\t\txpoint = str(xendpoint).split('/')\n")
                f.write("\t\t\trolepoint = getepoint(xpoint)  # xpoint[len(xpoint)-1]\n")
                f.write('\t\telse:\n')
                f.write("\t\t\trolepoint = xendpoint\n")
                f.write('\t\troles = config.get("apiEndpoint", rolepoint)\n')
                # f.write('\t\tprint(roles)\n')
                f.write("\t\troles, cxUrl = roles.split(',')\n")
                f.write('\t\tif rtype != "skip" and rtype == get_tags(rtype) and rtype is not None:\n')
                f.write("\t\t\tgetallx = None\n")
                f.write("\t\t\tgtdata = get_sheetnames_excel(generate_test_ap, itemdata=depend, ustory=tcdef)\n")
                f.write("\t\t\tfor xlen in range(0, len(gtdata)):\n")
                f.write("\t\t\t\tgetallx = excel_row_data(gtdata[xlen][0], depend)\n")
                f.write("\t\t\t\tif depend is not None:\n")
                f.write("\t\t\t\t\tapiSteps().execute_steps(getallx)\n")
                f.write("\t\t\t\telse:\n")
                f.write("\t\t\t\t\tapiSteps().execute_steps(getallx)\n")
                f.write('\t\telse:\n')
                f.write(
                    "\t\t\tget_results(reportpath, roles, testcase, xendpoint, payload, params, exresults, 'Testcase Skipped',\n")
                f.write(
                    "\t\t\t\t\t\t\tresults='SKIPPED', fontx='F4D25A', elapsed_secs='', comments=scvarib, sprints=sprints)\n")
                f.write('\t\t\tif rtype == "skip":\n')
                f.write('\t\t\t\tself.xSkip(testcase + ": Testcase Skipped, Due to not much information")\n')
                f.write('\t\t\telse:\n')
                f.write(
                    '\t\t\t\tself.skipTest(reason="Test execution based on Tags :" + str(test_tags) + ": Excludes the rest")\n')
                f.write('\n\n')
    f.close()


def get_generate_data_exl(reportpath, sheetname, testcase, tendpoint, method, payload, apiresponse, schvariables,
                          sfvalidations, runtype, case, exresults, rpri, get_total_rows_x=0):
    reportpath.set_sheet_by_name(sheetname)
    get_total_rows = reportpath.get_max_row_no()
    try:
        if get_total_rows == get_total_rows_x:
            get_total_rows = 0
        reportpath.write_cell_content_colored(get_total_rows + 1, 1, testcase)
        reportpath.write_cell_content_colored(get_total_rows + 1, 2, tendpoint)
        reportpath.write_cell_content_colored(get_total_rows + 1, 3, method)
        reportpath.write_cell_content_colored(get_total_rows + 1, 4, payload)
        reportpath.write_cell_content_colored(get_total_rows + 1, 5, apiresponse)
        reportpath.write_cell_content_colored(get_total_rows + 1, 6, str(schvariables))
        reportpath.write_cell_content_colored(get_total_rows + 1, 7, str(sfvalidations))
        reportpath.write_cell_content_colored(get_total_rows + 1, 8, runtype)
        reportpath.write_cell_content_colored(get_total_rows + 1, 9, case)
        reportpath.write_cell_content_colored(get_total_rows + 1, 10, exresults)
        reportpath.write_cell_content_colored(get_total_rows + 1, 11, str(rpri))
    except Exception as e:
        if ValueError:
            pass


def get_sheetnames_excel(generate_test_ap, itemdata='COE_001', ustory=None):
    get_excel_data, gtdata = None, []
    getxcl = ParseExcel(generate_test_ap)
    getallxm = getxcl.get_sheetnames()
    if itemdata:
        getdata_item = itemdata.split(',')
        getdata_item.append(ustory)
        for gdata in range(0, len(getdata_item)):
            for xallm in getallxm:
                get_excel_data = ParseExcel(generate_test_ap).get_row_all_col_data(sheetname=xallm,
                                                                                   columnname="TC_Def",
                                                                                   pagename=getdata_item[gdata])
                if get_excel_data:
                    gtdata.append(get_excel_data)
    else:
        for xallm in getallxm:
            get_excel_data = ParseExcel(generate_test_ap).get_row_all_col_data(sheetname=xallm, columnname="TC_Def",
                                                                               pagename=ustory)
            if get_excel_data:
                gtdata.append(get_excel_data)
    return gtdata


def excel_row_data(gtdata, depend):
    testcase = gtdata["Test Case"]
    testdef = gtdata["TC_Def"]
    xendpoint = gtdata["EndPoint"]
    xmethod = gtdata["Method"]
    payload = gtdata["Payload"]
    params = gtdata["Params"]
    testdata = gtdata["Test_Data"]
    exresults = gtdata["API Response"]
    scvarib = gtdata["Schema Variables"]
    ctype = gtdata["SType|Format|Validation"]
    results = gtdata["Expected_Results"]
    sprints = gtdata["IncidentIds"]
    if depend is not None and testdef in depend:
        exestp = None
    else:
        exestp = 'Y'
    return testcase, xendpoint, xmethod, payload, params, testdata, exresults, scvarib, \
        ctype, results, sprints, exestp


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def mixedcharacters(k=5):
    mixed_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
    return mixed_chars


def getlister(xnum, data=None, datex=None):
    my_list = []
    x = xnum
    for i in range(x):
        if data:
            char_type = data
        else:
            char_type = testdata.username() + id_generator(4) + '_' + str(datex)
        my_list.append(char_type)
    return my_list


def getExtracterx(data, xdata, tdata):
    getdata = data_required(datafile=data)
    if tdata == '!res' or '@' in tdata:
        datapack = Validations().get_json_string_results('data.' + str(xdata), getdata)
        if '.item.' in xdata:
            getxdata = datapack
        else:
            getxdata = str(getdata['data'][xdata])
    else:
        datapack = Validations().get_json_string_results(xdata, getdata)
        getxdata = datapack[0]
    return getxdata


def getExtract(xdata, tdata):
    fpath, aName, apiname, evalue = xdata.split('|')
    # print(fpath, aName, apiname, evalue)
    apiname = str(apiname) + '.json'
    getfile = mypath / 'test_data' / 'json_data' / fpath / apiname
    getdata = data_required(datafile=getfile)
    datapack = Validations().get_json_string_results(aName, getdata)
    if evalue == '':
        return datapack
    else:
        return datapack[0]


def getremove(xdata, tdata, getn=None):
    if '|' in xdata:
        fpath, aName, apiname, atname = xdata.split('|')
        apiname = str(apiname) + '.json'
        getfile = mypath / 'test_data' / 'json_data' / fpath / apiname
        getdata = data_required(datafile=getfile)
    else:
        getdata = getn
        aName = xdata
    datapack = Validations().get_json_string_results(aName, getdata)
    return datapack


def getbaseUrl(ddata, urlString, repl=None):
    match = re.search(r'{(.*?)}', ddata)
    if match:
        extracted_string = match.group(1)
        replaced_string = ddata.replace(str('{' + extracted_string + '}'), str(urlString))
        return replaced_string
    else:
        replaced_string = ddata.replace(str(repl), str(urlString))
        return replaced_string


def getepoint(getnbx):
    global progress, epointx
    config.read(mypath / "utils" / "endpointapi.ini")
    getslx = getnbx  # .split('/')
    for xlx in getslx[::-1]:
        timeout_start = time.time()
        timeout = 1 * 2
        progress = None
        while not progress:
            delta = time.time() - timeout_start
            try:
                progress = config.get("apiEndpoint", xlx)
                epointx = xlx
            except Exception:
                progress = None
            if progress is not None:
                progress = epointx
            if delta >= timeout:
                break
        if progress is not None:
            progress = epointx
            break
    return progress
