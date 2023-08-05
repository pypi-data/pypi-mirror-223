from ..core.scheduleService import ScheduleService
from ..systemService.mqttService import MqttService
from .loader.hardwareInfoLoader import HardwareInfoLoader




# 代理加载存储字典
proxyDict:dict = None

# 服务加载存储字典
serviceDict:dict = None

# mqtt客户端
pervasiveMqttClient:MqttService = None


# 定时器
taskServer:ScheduleService = None

# 硬件信息加载器
hardwareInfoLoader:HardwareInfoLoader = None


def getServiceListInfo():
    services = []
    for key in serviceDict.keys():
        serviceItem= serviceDict[key].__dict__
        serviceItem =  {
            'versionCode': serviceItem['versionCode'],
            'id': serviceItem['url'],
            'serviceId': serviceItem['url']
        }
        services.append(serviceItem)
    return services
