import yaml
import re
import copy
import warnings

def getYamlConfName(pyFileName):
    return pyFileName.split(".")[0] + ".config.yaml";


def getSubExpId(pyFileName):
    pattern = r'^p\d+\.py$'
    if re.match(pattern, pyFileName):
        subExpId = int(pyFileName[1:-3])
    else:
        subExpId = 0;
    return subExpId;


def unpackAggrParam(param):
    pattern = r'^aggr_\d+$'
    delList = [];
    aggrParam = {};
    for strKey in param.keys():
        if re.match(pattern, strKey):
            param2 = param[strKey]
            delList.append(strKey)
            for strKey2 in param2.keys():
                aggrParam[strKey2] = param2[strKey2]
    for strKey in delList:
        del param[strKey]

    for strKey in aggrParam.keys():
        param[strKey] = aggrParam[strKey]
    return param


def convParam2Setting(param):
    configRes = {};
    for strKey in param.keys():
        val = param[strKey]
        keys = strKey.split('__');
        config = configRes
        for i in range(len(keys) - 1):
            ks = keys[i];
            if not ks in config:
                config[ks] = {};
            config = config[ks]
        config[keys[-1]] = val
    return configRes;


def dictConv(orgDict, updatedDict):
    for key1 in updatedDict:
        val = updatedDict[key1]
        if isinstance(val, dict):
            if not key1 in orgDict or orgDict[key1] is None:
                orgDict[key1] = {}
            dictConv(orgDict[key1], val);
        else:
            orgDict[key1] = val;


def loadSettingFromYaml(backgroundYamlFile, dynamicYamlFile, activeBackgroundYamlId=0, activeDynamicYamlId=0,
                        varSettings={}, isOptionParse=False):
    with open(backgroundYamlFile, 'r', encoding='utf-8') as c:
        defConfigs = list(yaml.load_all(c, Loader=yaml.FullLoader))
        theConfig = defConfigs[activeBackgroundYamlId]
    with open(dynamicYamlFile, 'r', encoding='utf-8') as c:
        dyConfig = list(yaml.load_all(c, Loader=yaml.FullLoader))
    if activeDynamicYamlId < 0 or activeDynamicYamlId >= len(dyConfig):
        raise RuntimeError(
            f'activeBackgroundYamlId的范围错误，activeBackgroundYamlId = {activeDynamicYamlId}, 应该在[0, {len(dyConfig)}) 内')
        return None;
    dyConfig = dyConfig[activeDynamicYamlId]
    dictConv(theConfig, dyConfig)
    if isOptionParse:
        theConfig=optionParse(theConfig)
    dictConv(theConfig, varSettings)
    return theConfig, varSettings

def optionParse(config):
    config=copy.deepcopy(config)
    while True:
        (config,nSuc,nFail)=_optionParse(config, config,'');
        if nSuc==0 and nFail==0:
            return config
        if nSuc==0 and nFail>0:
            raise SyntaxError(f'存在{nFail}个引用路径为非字符串类型！')
    return config

def _optionParse(config, orgConfig, path):
    nSuc=0
    nFail=0
    if isinstance(config, dict):
        if '$' in config:
            refPath=config['$']
            keys = refPath.split('.');
            tmpConfig=orgConfig
            for ks in keys:
                tmpConfig=tmpConfig[ks]
            if not isinstance(tmpConfig,str):
                nFail=1
                return (config,nSuc,nFail)

            if tmpConfig in config:
                nSuc = 1
                return (config[tmpConfig], nSuc, nFail)
            else:
                for key in config:
                    if re.match(key, tmpConfig):
                        warnings.warn(f"配置路径{path}不存在关键词{tmpConfig}，但通过正则表达式匹配到关键词{key}！")
                        nSuc = 1
                        return (config[key], nSuc, nFail)
                if 'default' in config:
                    warnings.warn(f"配置路径{path}不存在关键词{tmpConfig}，但使用了default标签的内容！")
                    nSuc = 1
                    return (config['default'], nSuc, nFail)
                raise SyntaxError(f'配置路径{path}不存在关键词{tmpConfig}，请检查{refPath}的值！')

        else:
            nSuc=0
            nFail=0
            for key in config:
                (res,nSuc0,nFail0)=_optionParse(config[key],orgConfig, (path+'.' if path!="" else "")+key)
                config[key]=res
                nSuc+=nSuc0
                nFail+=nFail0
    return (config,nSuc,nFail)


def loadSettingFromYamlSimple(backgroundYamlFile, varSettings={}):
    with open(backgroundYamlFile, 'r', encoding='utf-8') as c:
        defConfigs = list(yaml.load_all(c, Loader=yaml.FullLoader))
        theConfig = defConfigs[0]
    dictConv(theConfig, varSettings)
    return theConfig


def removeNoneSetting(param):
    rmKeys = []
    for key1 in param:
        val = param[key1]
        if val is None:
            rmKeys.append(key1)
        elif isinstance(val, dict):
            removeNoneSetting(val);
    for key1 in rmKeys:
        del param[key1]
