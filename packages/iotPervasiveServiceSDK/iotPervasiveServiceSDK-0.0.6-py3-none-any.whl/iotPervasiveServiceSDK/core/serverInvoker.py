import copy
import json
from ..core import applicationContext
from ..utils import pathUtils as PathUtil

from .exception.serviceException import ServiceNotExistException
from .exception.serviceException import CapabilityNotExistException
from .exception.serviceException import ProxyNotExistException
from .exception.commonException import invalidParamsException
from ..model.ujinja.source import TemplateEngine
from ..proxy.thingProxy import thingProxy

class ServerInvoker:
  '''
  * 调用服务
  * serviceId  服务id
  * capabilityId 能力id
  * postJsonDict 消息的参数字典
  '''
  def invokeService(serviceId:str,capabilityId:str,requestJsonDict:dict):
    # 特判物模型读写服务    
    if (serviceId == "thingService"):
        return thingProxy({"operation":capabilityId}).handle(requestJsonDict)
    # 从服务字典读取服务信息
    if (serviceId==None):
        raise invalidParamsException("id",serviceId)
    if (capabilityId == None):
        raise invalidParamsException("capabilityId",capabilityId)
    service = applicationContext.serviceDict.get(serviceId,None)
    if (service == None):
        raise ServiceNotExistException(serviceId)
    capability = service.capabilityBeanDict.get(capabilityId,None)
    if (capability==None):
        raise CapabilityNotExistException(capabilityId)
    # jinja2 输入消息转换
    runData = None
    if(capability.inputMapper != None):
      if(capability.inputLanguage == "jinja2"):
          inputTemplateEngine = TemplateEngine()
          inputTemplateEngine.load_template(capability.inputMapper)
          runData = inputTemplateEngine.render_template(requestJsonDict)
          print(runData)
        
    initData =  copy.deepcopy(capability.attributes)
    # 如果是python代理则需要加载脚本所在位置
    if(capability.proxyType == "pythonServiceProxy"):
      scriptPath = PathUtil.joinPath(service.filePath,"script")
      initData["script"] = PathUtil.joinPath(scriptPath,initData["script"])
    response = ServerInvoker.invokeProxy(capability.proxyType,initData,runData)
    #输出消息转换
    if(capability.outputMapper != None):
      if(capability.outputLanguage == "jinja2"):
        outputTemplateEngine = TemplateEngine()
        outputTemplateEngine.load_template(capability.outputMapper)
        response = outputTemplateEngine.render_template(json.loads(response))
        print(response)
    return response


  '''
  * 运行代理
  * proxyName 代理名称
  * initData  初始化数据
  * runData   运行时数据
  '''
  def invokeProxy(proxyName:str,initData:any,runData):
      proxyModel = applicationContext.proxyDict.get(proxyName,None)
      if(proxyModel==None):
          raise ProxyNotExistException(proxyName)
      if(hasattr(proxyModel,proxyName)):
        proxyClass = getattr(proxyModel,proxyName)
        proxy = proxyClass(initData)
        return proxy.handle(runData)
  
    