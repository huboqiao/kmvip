# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 2.7 (r27:82525, Jul  4 2010, 09:01:59) [MSC v.1500 32 bit (Intel)]
# From type library '{D95CB779-00CB-4B49-97B9-9F0B61CAB3C1}'
# On Mon Apr 27 18:29:35 2015
'ZKSoftware ZKFinger Engine 4.x'
makepy_version = '0.5.01'
python_version = 0x20700f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{D95CB779-00CB-4B49-97B9-9F0B61CAB3C1}')
MajorVersion = 4
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class IZKFPEngX(DispatchBaseClass):
	'Dispatch interface for ZKFPEngX Control'
	CLSID = IID('{161A8D2D-3DDE-4744-BA38-08F900D10D6D}')
	coclass_clsid = IID('{CA69969C-2F27-41D3-954D-A48B941C3BA7}')

	def AddBitmap(self, BitmapHandle=defaultNamedNotOptArg, ValidRectX1=defaultNamedNotOptArg, ValidRectY1=defaultNamedNotOptArg, ValidRectX2=defaultNamedNotOptArg
			, ValidRectY2=defaultNamedNotOptArg, DPI=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),BitmapHandle
			, ValidRectX1, ValidRectY1, ValidRectX2, ValidRectY2, DPI
			)

	def AddImageFile(self, AFileName=defaultNamedNotOptArg, ADPI=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(63, LCID, 1, (11, 0), ((8, 1), (3, 1)),AFileName
			, ADPI)

	def AddRegTemplateFileToFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, pRegTemplateFile=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1)),fpcHandle
			, FPID, pRegTemplateFile)

	def AddRegTemplateFileToFPCacheDBEx(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, pRegTemplateFile=defaultNamedNotOptArg, pRegTemplate10File=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1), (8, 1)),fpcHandle
			, FPID, pRegTemplateFile, pRegTemplate10File)

	def AddRegTemplateStrToFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, ARegTemplateStr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(35, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1)),fpcHandle
			, FPID, ARegTemplateStr)

	def AddRegTemplateStrToFPCacheDBEx(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, ARegTemplateStr=defaultNamedNotOptArg, ARegTemplate10Str=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1), (8, 1)),fpcHandle
			, FPID, ARegTemplateStr, ARegTemplate10Str)

	def AddRegTemplateToFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, pRegTemplate=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (3, 0), ((3, 1), (3, 1), (12, 1)),fpcHandle
			, FPID, pRegTemplate)

	def AddRegTemplateToFPCacheDBEx(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg, pRegTemplate=defaultNamedNotOptArg, pRegTemplate10=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (3, 0), ((3, 1), (3, 1), (12, 1), (12, 1)),fpcHandle
			, FPID, pRegTemplate, pRegTemplate10)

	def BeginCapture(self):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

	def BeginEnroll(self):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (24, 0), (),)

	def CancelCapture(self):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	def CancelEnroll(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (),)

	def CompressTemplate(self, ATemplate=defaultNamedNotOptArg):
		return self._ApplyTypes_(68, 1, (12, 0), ((8, 1),), u'CompressTemplate', None,ATemplate
			)

	def ControlSensor(self, ACode=defaultNamedNotOptArg, AValue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (3, 0), ((3, 1), (3, 1)),ACode
			, AValue)

	def ConvertAttTemplate(self, ATemplate=defaultNamedNotOptArg):
		return self._ApplyTypes_(70, 1, (12, 0), ((12, 1),), u'ConvertAttTemplate', None,ATemplate
			)

	def ConvertToBiokey(self, OriTemplate=defaultNamedNotOptArg):
		return self._ApplyTypes_(204, 1, (12, 0), ((12, 1),), u'ConvertToBiokey', None,OriTemplate
			)

	def CreateFPCacheDB(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), (),)

	def CreateFPCacheDBEx(self):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (3, 0), (),)

	def DecodeTemplate(self, ASour=defaultNamedNotOptArg, ADest=defaultNamedNotOptArg):
		return self._ApplyTypes_(2, 1, (11, 0), ((8, 1), (16396, 3)), u'DecodeTemplate', None,ASour
			, ADest)

	def DecodeTemplate1(self, ASour=defaultNamedNotOptArg):
		return self._ApplyTypes_(31, 1, (12, 0), ((8, 1),), u'DecodeTemplate1', None,ASour
			)

	def DongleIsExist(self):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (11, 0), (),)

	def DongleMemRead(self, p1=defaultNamedNotOptArg, p2=defaultNamedNotOptArg, buf=defaultNamedNotOptArg):
		return self._ApplyTypes_(30, 1, (11, 0), ((16387, 3), (16387, 3), (16396, 3)), u'DongleMemRead', None,p1
			, p2, buf)

	def DongleMemWrite(self, p1=defaultNamedNotOptArg, p2=defaultNamedNotOptArg, buf=defaultNamedNotOptArg):
		return self._ApplyTypes_(38, 1, (11, 0), ((16387, 3), (16387, 3), (16396, 3)), u'DongleMemWrite', None,p1
			, p2, buf)

	def DongleSeed(self, lp2=defaultNamedNotOptArg, p1=defaultNamedNotOptArg, p2=defaultNamedNotOptArg, p3=defaultNamedNotOptArg
			, p4=defaultNamedNotOptArg):
		return self._ApplyTypes_(29, 1, (11, 0), ((16387, 3), (16387, 3), (16387, 3), (16387, 3), (16387, 3)), u'DongleSeed', None,lp2
			, p1, p2, p3, p4)

	def DongleUserID(self):
		return self._oleobj_.InvokeTypes(28, LCID, 1, (3, 0), (),)

	def EncodeTemplate(self, ASour=defaultNamedNotOptArg, ADest=defaultNamedNotOptArg):
		return self._ApplyTypes_(3, 1, (11, 0), ((12, 1), (16392, 3)), u'EncodeTemplate', None,ASour
			, ADest)

	def EncodeTemplate1(self, ASour=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(33, LCID, 1, (8, 0), ((12, 1),),ASour
			)

	def EndEngine(self):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), (),)

	def ExtractImageFromTerminal(self, AOriImage=defaultNamedNotOptArg, Size=defaultNamedNotOptArg, AAutoIdentify=defaultNamedNotOptArg, iResult=defaultNamedNotOptArg):
		return self._ApplyTypes_(211, 1, (3, 0), ((12, 1), (3, 1), (11, 1), (16396, 3)), u'ExtractImageFromTerminal', None,AOriImage
			, Size, AAutoIdentify, iResult)

	def ExtractImageFromURU(self, AOriImageStr=defaultNamedNotOptArg, Size=defaultNamedNotOptArg, AAutoIdentify=defaultNamedNotOptArg, iResult=defaultNamedNotOptArg):
		return self._ApplyTypes_(691, 1, (3, 0), ((8, 1), (3, 1), (11, 1), (16396, 3)), u'ExtractImageFromURU', None,AOriImageStr
			, Size, AAutoIdentify, iResult)

	def ExtractImageFromURU4000(self, AOriImageBuf=defaultNamedNotOptArg, Size=defaultNamedNotOptArg, AAutoIdentify=defaultNamedNotOptArg, iResult=defaultNamedNotOptArg):
		return self._ApplyTypes_(69, 1, (3, 0), ((30, 1), (3, 1), (11, 1), (16396, 3)), u'ExtractImageFromURU4000', None,AOriImageBuf
			, Size, AAutoIdentify, iResult)

	def FlushFPImages(self):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), (),)

	def FreeFPCacheDB(self, fpcHandle=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), ((3, 1),),fpcHandle
			)

	def FreeFPCacheDBEx(self, fpcHandle=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (24, 0), ((3, 1),),fpcHandle
			)

	def GenRegTemplateAsStringFromFile(self, AImageFileName=defaultNamedNotOptArg, ADPI=defaultNamedNotOptArg, ADest=defaultNamedNotOptArg):
		return self._ApplyTypes_(205, 1, (11, 0), ((8, 1), (3, 1), (16392, 3)), u'GenRegTemplateAsStringFromFile', None,AImageFileName
			, ADPI, ADest)

	def GenVerTemplateAsStringFromFile(self, AImageFileName=defaultNamedNotOptArg, ADPI=defaultNamedNotOptArg, ADest=defaultNamedNotOptArg):
		return self._ApplyTypes_(206, 1, (11, 0), ((8, 1), (3, 1), (16392, 3)), u'GenVerTemplateAsStringFromFile', None,AImageFileName
			, ADPI, ADest)

	def GetFingerImage(self, AFingerImage=defaultNamedNotOptArg):
		return self._ApplyTypes_(46, 1, (11, 0), ((16396, 3),), u'GetFingerImage', None,AFingerImage
			)

	def GetTemplate(self):
		return self._ApplyTypes_(45, 1, (12, 0), (), u'GetTemplate', None,)

	def GetTemplateAsString(self):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(39, LCID, 1, (8, 0), (),)

	def GetTemplateAsStringEx(self, AFPEngineVersion=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(219, LCID, 1, (8, 0), ((8, 1),),AFPEngineVersion
			)

	def GetTemplateCount(self, AFPHandle=defaultNamedNotOptArg, AOneToOneCnt=defaultNamedNotOptArg, ATotalCnt=defaultNamedNotOptArg):
		return self._ApplyTypes_(62, 1, (24, 0), ((3, 1), (16387, 3), (16387, 3)), u'GetTemplateCount', None,AFPHandle
			, AOneToOneCnt, ATotalCnt)

	def GetTemplateEx(self, AFPEngineVersion=defaultNamedNotOptArg):
		return self._ApplyTypes_(217, 1, (12, 0), ((8, 1),), u'GetTemplateEx', None,AFPEngineVersion
			)

	def GetVerScore(self):
		return self._oleobj_.InvokeTypes(60, LCID, 1, (3, 0), (),)

	def GetVerTemplate(self):
		return self._ApplyTypes_(59, 1, (12, 0), (), u'GetVerTemplate', None,)

	def GetVerTemplateEx(self, AFPEngineVersion=defaultNamedNotOptArg):
		return self._ApplyTypes_(220, 1, (12, 0), ((8, 1),), u'GetVerTemplateEx', None,AFPEngineVersion
			)

	def IdentificationFromFileInFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, pVerTemplateFile=defaultNamedNotOptArg, Score=defaultNamedNotOptArg, ProcessedFPNumber=defaultNamedNotOptArg):
		return self._ApplyTypes_(65, 1, (3, 0), ((3, 1), (8, 1), (16387, 3), (16387, 3)), u'IdentificationFromFileInFPCacheDB', None,fpcHandle
			, pVerTemplateFile, Score, ProcessedFPNumber)

	def IdentificationFromStrInFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, AVerTemplateStr=defaultNamedNotOptArg, Score=defaultNamedNotOptArg, ProcessedFPNumber=defaultNamedNotOptArg):
		return self._ApplyTypes_(66, 1, (3, 0), ((3, 1), (8, 1), (16387, 3), (16387, 3)), u'IdentificationFromStrInFPCacheDB', None,fpcHandle
			, AVerTemplateStr, Score, ProcessedFPNumber)

	def IdentificationInFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, pVerTemplate=defaultNamedNotOptArg, Score=defaultNamedNotOptArg, ProcessedFPNumber=defaultNamedNotOptArg):
		return self._ApplyTypes_(64, 1, (3, 0), ((3, 1), (12, 1), (16387, 3), (16387, 3)), u'IdentificationInFPCacheDB', None,fpcHandle
			, pVerTemplate, Score, ProcessedFPNumber)

	def InitEngine(self):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (3, 0), (),)

	def IsOneToOneTemplate(self, ATemplate=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), ((12, 1),),ATemplate
			)

	def IsOneToOneTemplateFile(self, ATemplateFileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 1, (11, 0), ((8, 1),),ATemplateFileName
			)

	def IsOneToOneTemplateStr(self, ATemplate=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(48, LCID, 1, (11, 0), ((8, 1),),ATemplate
			)

	def MF_GET_SNR(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, mode=defaultNamedNotOptArg, RDM_halt=defaultNamedNotOptArg
			, snr=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(221, LCID, 1, (11, 0), ((3, 1), (3, 1), (17, 1), (17, 1), (16401, 1), (16401, 1)),commHandle
			, DeviceAddress, mode, RDM_halt, snr, Value
			)

	def MF_GetSerNum(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, buffer=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(222, LCID, 1, (11, 0), ((3, 1), (3, 1), (16401, 1)),commHandle
			, DeviceAddress, buffer)

	def MF_GetVersionNum(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, VersionNum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(224, LCID, 1, (11, 0), ((3, 1), (3, 1), (16401, 1)),commHandle
			, DeviceAddress, VersionNum)

	def MF_PCDRead(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, mode=defaultNamedNotOptArg, blkIndex=defaultNamedNotOptArg
			, blkNum=defaultNamedNotOptArg, key=defaultNamedNotOptArg, buffer=defaultNamedNotOptArg):
		return self._ApplyTypes_(225, 1, (11, 0), ((3, 1), (3, 1), (17, 1), (17, 1), (17, 1), (16401, 3), (16401, 3)), u'MF_PCDRead', None,commHandle
			, DeviceAddress, mode, blkIndex, blkNum, key
			, buffer)

	def MF_PCDWrite(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, mode=defaultNamedNotOptArg, blkIndex=defaultNamedNotOptArg
			, blkNum=defaultNamedNotOptArg, key=defaultNamedNotOptArg, buffer=defaultNamedNotOptArg):
		return self._ApplyTypes_(226, 1, (11, 0), ((3, 1), (3, 1), (17, 1), (17, 1), (17, 1), (16401, 3), (16401, 3)), u'MF_PCDWrite', None,commHandle
			, DeviceAddress, mode, blkIndex, blkNum, key
			, buffer)

	def MF_SetSerNum(self, commHandle=defaultNamedNotOptArg, DeviceAddress=defaultNamedNotOptArg, newValue=defaultNamedNotOptArg, buffer=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(223, LCID, 1, (11, 0), ((3, 1), (3, 1), (16401, 1), (16401, 1)),commHandle
			, DeviceAddress, newValue, buffer)

	def ModifyTemplate(self, ATemplate=defaultNamedNotOptArg, AOneToOne=defaultNamedNotOptArg):
		return self._ApplyTypes_(25, 1, (24, 0), ((16396, 3), (11, 1)), u'ModifyTemplate', None,ATemplate
			, AOneToOne)

	def ModifyTemplateFile(self, ATemplateFileName=defaultNamedNotOptArg, AOneToOne=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(58, LCID, 1, (24, 0), ((8, 1), (11, 1)),ATemplateFileName
			, AOneToOne)

	def ModifyTemplateStr(self, ATemplate=defaultNamedNotOptArg, AOneToOne=defaultNamedNotOptArg):
		return self._ApplyTypes_(57, 1, (24, 0), ((16392, 3), (11, 1)), u'ModifyTemplateStr', None,ATemplate
			, AOneToOne)

	def PrintImageAt(self, hdc=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, aWidth=defaultNamedNotOptArg
			, aHeight=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),hdc
			, x, y, aWidth, aHeight)

	def PrintImageEllipseAt(self, hdc=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, aWidth=defaultNamedNotOptArg
			, aHeight=defaultNamedNotOptArg, bkColor=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (24, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (19, 1)),hdc
			, x, y, aWidth, aHeight, bkColor
			)

	def RemoveRegTemplateFromFPCacheDB(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), ((3, 1), (3, 1)),fpcHandle
			, FPID)

	def RemoveRegTemplateFromFPCacheDBEx(self, fpcHandle=defaultNamedNotOptArg, FPID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (3, 0), ((3, 1), (3, 1)),fpcHandle
			, FPID)

	def SaveBitmap(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SaveJPG(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SaveTemplate(self, FileName=defaultNamedNotOptArg, ATemplate=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (11, 0), ((8, 1), (12, 1)),FileName
			, ATemplate)

	def SaveTemplateStr(self, FileName=defaultNamedNotOptArg, ATemplateStr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(61, LCID, 1, (24, 0), ((8, 1), (8, 1)),FileName
			, ATemplateStr)

	def SetAutoIdentifyPara(self, AAutoIdentify=defaultNamedNotOptArg, ACacheDBHandle=defaultNamedNotOptArg, AScore=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), ((11, 1), (3, 1), (3, 1)),AAutoIdentify
			, ACacheDBHandle, AScore)

	def SetImageDirection(self, AIsImageChange=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(41, LCID, 1, (24, 0), ((11, 1),),AIsImageChange
			)

	def SetOneToOnePara(self, ADoLearning=defaultNamedNotOptArg, AMatchSecurity=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(67, LCID, 1, (24, 0), ((3, 1), (3, 1)),ADoLearning
			, AMatchSecurity)

	def SetTemplateLen(self, ATemplate=defaultNamedNotOptArg, ALen=defaultNamedNotOptArg):
		return self._ApplyTypes_(208, 1, (3, 0), ((16396, 3), (3, 1)), u'SetTemplateLen', None,ATemplate
			, ALen)

	def UsingXTFTemplate(self, ADoUsingXTFTemplate=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (24, 0), ((11, 1),),ADoUsingXTFTemplate
			)

	def VerFinger(self, regTemplate=defaultNamedNotOptArg, verTemplate=defaultNamedNotOptArg, ADoLearning=defaultNamedNotOptArg, ARegFeatureChanged=defaultNamedNotOptArg):
		return self._ApplyTypes_(8, 1, (11, 0), ((16396, 3), (12, 1), (11, 1), (16395, 3)), u'VerFinger', None,regTemplate
			, verTemplate, ADoLearning, ARegFeatureChanged)

	def VerFingerFromFile(self, regTemplateFile=defaultNamedNotOptArg, verTemplateFile=defaultNamedNotOptArg, ADoLearning=defaultNamedNotOptArg, ARegFeatureChanged=defaultNamedNotOptArg):
		return self._ApplyTypes_(42, 1, (11, 0), ((8, 1), (8, 1), (11, 1), (16395, 3)), u'VerFingerFromFile', None,regTemplateFile
			, verTemplateFile, ADoLearning, ARegFeatureChanged)

	def VerFingerFromStr(self, regTemplateStr=defaultNamedNotOptArg, verTemplateStr=defaultNamedNotOptArg, ADoLearning=defaultNamedNotOptArg, ARegFeatureChanged=defaultNamedNotOptArg):
		return self._ApplyTypes_(36, 1, (11, 0), ((16392, 3), (8, 1), (11, 1), (16395, 3)), u'VerFingerFromStr', None,regTemplateStr
			, verTemplateStr, ADoLearning, ARegFeatureChanged)

	def VerRegFingerFile(self, regTemplateFile=defaultNamedNotOptArg, verTemplate=defaultNamedNotOptArg, ADoLearning=defaultNamedNotOptArg, ARegFeatureChanged=defaultNamedNotOptArg):
		return self._ApplyTypes_(10, 1, (11, 0), ((8, 1), (12, 1), (11, 1), (16395, 3)), u'VerRegFingerFile', None,regTemplateFile
			, verTemplate, ADoLearning, ARegFeatureChanged)

	_prop_map_get_ = {
		"Active": (32, 2, (11, 0), (), "Active", None),
		"EngineValid": (56, 2, (11, 0), (), "EngineValid", None),
		"EnrollCount": (6, 2, (3, 0), (), "EnrollCount", None),
		"EnrollIndex": (47, 2, (3, 0), (), "EnrollIndex", None),
		"FPEngineVersion": (51, 2, (8, 0), (), "FPEngineVersion", None),
		"ForceSecondMatch": (71, 2, (11, 0), (), "ForceSecondMatch", None),
		"ImageHeight": (53, 2, (3, 0), (), "ImageHeight", None),
		"ImageWidth": (52, 2, (3, 0), (), "ImageWidth", None),
		"IsRegister": (40, 2, (11, 0), (), "IsRegister", None),
		"IsReturnNoLic": (227, 2, (11, 0), (), "IsReturnNoLic", None),
		"IsSupportAuxDevice": (210, 2, (3, 0), (), "IsSupportAuxDevice", None),
		"OneToOneThreshold": (49, 2, (3, 0), (), "OneToOneThreshold", None),
		"ProduceName": (207, 2, (8, 0), (), "ProduceName", None),
		"RegTplFileName": (44, 2, (8, 0), (), "RegTplFileName", None),
		"ReservedParam": (228, 2, (3, 0), (), "ReservedParam", None),
		"SensorCount": (54, 2, (3, 0), (), "SensorCount", None),
		"SensorIndex": (37, 2, (3, 0), (), "SensorIndex", None),
		"SensorSN": (50, 2, (8, 0), (), "SensorSN", None),
		"TemplateLen": (55, 2, (3, 0), (), "TemplateLen", None),
		"Threshold": (21, 2, (3, 0), (), "Threshold", None),
		"Vendor": (203, 2, (8, 0), (), "Vendor", None),
		"VerTplFileName": (43, 2, (8, 0), (), "VerTplFileName", None),
	}
	_prop_map_put_ = {
		"Active": ((32, LCID, 4, 0),()),
		"EngineValid": ((56, LCID, 4, 0),()),
		"EnrollCount": ((6, LCID, 4, 0),()),
		"EnrollIndex": ((47, LCID, 4, 0),()),
		"FPEngineVersion": ((51, LCID, 4, 0),()),
		"ForceSecondMatch": ((71, LCID, 4, 0),()),
		"ImageHeight": ((53, LCID, 4, 0),()),
		"ImageWidth": ((52, LCID, 4, 0),()),
		"IsRegister": ((40, LCID, 4, 0),()),
		"IsReturnNoLic": ((227, LCID, 4, 0),()),
		"OneToOneThreshold": ((49, LCID, 4, 0),()),
		"RegTplFileName": ((44, LCID, 4, 0),()),
		"SensorCount": ((54, LCID, 4, 0),()),
		"SensorIndex": ((37, LCID, 4, 0),()),
		"SensorSN": ((50, LCID, 4, 0),()),
		"TemplateLen": ((55, LCID, 4, 0),()),
		"Threshold": ((21, LCID, 4, 0),()),
		"VerTplFileName": ((43, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IZKFPEngXEvents:
	'Events interface for ZKFPEngX Control'
	CLSID = CLSID_Sink = IID('{8AEE2E53-7EBE-4B51-A964-009ADC68D107}')
	coclass_clsid = IID('{CA69969C-2F27-41D3-954D-A48B941C3BA7}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        8 : "OnImageReceived",
		        9 : "OnEnroll",
		        3 : "OnFingerLeaving",
		        2 : "OnCaptureToFile",
		        1 : "OnFingerTouching",
		       11 : "OnEnrollToFile",
		       10 : "OnCapture",
		        5 : "OnFeatureInfo",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnImageReceived(self, AImageValid=defaultNamedNotOptArg):
#	def OnEnroll(self, ActionResult=defaultNamedNotOptArg, ATemplate=defaultNamedNotOptArg):
#	def OnFingerLeaving(self):
#	def OnCaptureToFile(self, ActionResult=defaultNamedNotOptArg):
#	def OnFingerTouching(self):
#	def OnEnrollToFile(self, ActionResult=defaultNamedNotOptArg):
#	def OnCapture(self, ActionResult=defaultNamedNotOptArg, ATemplate=defaultNamedNotOptArg):
#	def OnFeatureInfo(self, AQuality=defaultNamedNotOptArg):


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'ZKFPEngXControl.ZKFPEngX'
class ZKFPEngX(CoClassBaseClass): # A CoClass
	# ZKFPEngX Control
	CLSID = IID('{CA69969C-2F27-41D3-954D-A48B941C3BA7}')
	coclass_sources = [
		IZKFPEngXEvents,
	]
	default_source = IZKFPEngXEvents
	coclass_interfaces = [
		IZKFPEngX,
	]
	default_interface = IZKFPEngX

IZKFPEngX_vtables_dispatch_ = 1
IZKFPEngX_vtables_ = [
	(( u'EnrollCount' , u'Value' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 28 , (3, 0, None, None) , 0 , )),
	(( u'EnrollCount' , u'Value' , ), 6, (6, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( u'VerFinger' , u'regTemplate' , u'verTemplate' , u'ADoLearning' , u'ARegFeatureChanged' , 
			u'Value' , ), 8, (8, (), [ (16396, 3, None, None) , (12, 1, None, None) , (11, 1, None, None) , 
			(16395, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 36 , (3, 0, None, None) , 0 , )),
	(( u'VerRegFingerFile' , u'regTemplateFile' , u'verTemplate' , u'ADoLearning' , u'ARegFeatureChanged' , 
			u'Value' , ), 10, (10, (), [ (8, 1, None, None) , (12, 1, None, None) , (11, 1, None, None) , 
			(16395, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( u'PrintImageAt' , u'hdc' , u'x' , u'y' , u'aWidth' , 
			u'aHeight' , ), 12, (12, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 44 , (3, 0, None, None) , 0 , )),
	(( u'PrintImageEllipseAt' , u'hdc' , u'x' , u'y' , u'aWidth' , 
			u'aHeight' , u'bkColor' , ), 13, (13, (), [ (3, 1, None, None) , (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (19, 1, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( u'BeginEnroll' , ), 14, (14, (), [ ], 1 , 1 , 4 , 0 , 52 , (3, 0, None, None) , 0 , )),
	(( u'SaveTemplate' , u'FileName' , u'ATemplate' , u'Value' , ), 18, (18, (), [ 
			(8, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( u'SaveBitmap' , u'FileName' , ), 22, (22, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 60 , (3, 0, None, None) , 0 , )),
	(( u'SaveJPG' , u'FileName' , ), 24, (24, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( u'InitEngine' , u'Value' , ), 26, (26, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 68 , (3, 0, None, None) , 0 , )),
	(( u'SensorIndex' , u'Value' , ), 37, (37, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( u'SensorIndex' , u'Value' , ), 37, (37, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 76 , (3, 0, None, None) , 0 , )),
	(( u'CancelEnroll' , ), 1, (1, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( u'CreateFPCacheDB' , u'Value' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 84 , (3, 0, None, None) , 0 , )),
	(( u'FreeFPCacheDB' , u'fpcHandle' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateToFPCacheDB' , u'fpcHandle' , u'FPID' , u'pRegTemplate' , u'Value' , 
			), 15, (15, (), [ (3, 1, None, None) , (3, 1, None, None) , (12, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 92 , (3, 0, None, None) , 0 , )),
	(( u'RemoveRegTemplateFromFPCacheDB' , u'fpcHandle' , u'FPID' , u'Value' , ), 16, (16, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateFileToFPCacheDB' , u'fpcHandle' , u'FPID' , u'pRegTemplateFile' , u'Value' , 
			), 20, (20, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 100 , (3, 0, None, None) , 0 , )),
	(( u'Threshold' , u'Value' , ), 21, (21, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( u'Threshold' , u'Value' , ), 21, (21, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 108 , (3, 0, None, None) , 0 , )),
	(( u'DongleIsExist' , u'Value' , ), 23, (23, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( u'DongleUserID' , u'Value' , ), 28, (28, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 116 , (3, 0, None, None) , 0 , )),
	(( u'DongleSeed' , u'lp2' , u'p1' , u'p2' , u'p3' , 
			u'p4' , u'Value' , ), 29, (29, (), [ (16387, 3, None, None) , (16387, 3, None, None) , 
			(16387, 3, None, None) , (16387, 3, None, None) , (16387, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( u'DongleMemRead' , u'p1' , u'p2' , u'buf' , u'Value' , 
			), 30, (30, (), [ (16387, 3, None, None) , (16387, 3, None, None) , (16396, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 124 , (3, 0, None, None) , 0 , )),
	(( u'DongleMemWrite' , u'p1' , u'p2' , u'buf' , u'Value' , 
			), 38, (38, (), [ (16387, 3, None, None) , (16387, 3, None, None) , (16396, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( u'VerFingerFromFile' , u'regTemplateFile' , u'verTemplateFile' , u'ADoLearning' , u'ARegFeatureChanged' , 
			u'Value' , ), 42, (42, (), [ (8, 1, None, None) , (8, 1, None, None) , (11, 1, None, None) , 
			(16395, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 132 , (3, 0, None, None) , 0 , )),
	(( u'VerTplFileName' , u'Value' , ), 43, (43, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( u'VerTplFileName' , u'Value' , ), 43, (43, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 140 , (3, 0, None, None) , 0 , )),
	(( u'RegTplFileName' , u'Value' , ), 44, (44, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( u'RegTplFileName' , u'Value' , ), 44, (44, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 148 , (3, 0, None, None) , 0 , )),
	(( u'GetTemplate' , u'Value' , ), 45, (45, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( u'GetFingerImage' , u'AFingerImage' , u'Value' , ), 46, (46, (), [ (16396, 3, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 156 , (3, 0, None, None) , 0 , )),
	(( u'OneToOneThreshold' , u'Value' , ), 49, (49, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( u'OneToOneThreshold' , u'Value' , ), 49, (49, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 164 , (3, 0, None, None) , 0 , )),
	(( u'IsOneToOneTemplate' , u'ATemplate' , u'Value' , ), 7, (7, (), [ (12, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( u'ModifyTemplate' , u'ATemplate' , u'AOneToOne' , ), 25, (25, (), [ (16396, 3, None, None) , 
			(11, 1, None, None) , ], 1 , 1 , 4 , 0 , 172 , (3, 0, None, None) , 0 , )),
	(( u'FlushFPImages' , ), 19, (19, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( u'Active' , u'Value' , ), 32, (32, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 180 , (3, 0, None, None) , 0 , )),
	(( u'Active' , u'Value' , ), 32, (32, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( u'IsRegister' , u'Value' , ), 40, (40, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 188 , (3, 0, None, None) , 0 , )),
	(( u'IsRegister' , u'Value' , ), 40, (40, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( u'EnrollIndex' , u'Value' , ), 47, (47, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 196 , (3, 0, None, None) , 0 , )),
	(( u'EnrollIndex' , u'Value' , ), 47, (47, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( u'SensorSN' , u'Value' , ), 50, (50, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 204 , (3, 0, None, None) , 0 , )),
	(( u'SensorSN' , u'Value' , ), 50, (50, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( u'FPEngineVersion' , u'Value' , ), 51, (51, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 212 , (3, 0, None, None) , 0 , )),
	(( u'FPEngineVersion' , u'Value' , ), 51, (51, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( u'ImageWidth' , u'Value' , ), 52, (52, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 220 , (3, 0, None, None) , 0 , )),
	(( u'ImageWidth' , u'Value' , ), 52, (52, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( u'ImageHeight' , u'Value' , ), 53, (53, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 228 , (3, 0, None, None) , 0 , )),
	(( u'ImageHeight' , u'Value' , ), 53, (53, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( u'SensorCount' , u'Value' , ), 54, (54, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 236 , (3, 0, None, None) , 0 , )),
	(( u'SensorCount' , u'Value' , ), 54, (54, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( u'TemplateLen' , u'Value' , ), 55, (55, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 244 , (3, 0, None, None) , 0 , )),
	(( u'TemplateLen' , u'Value' , ), 55, (55, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( u'EngineValid' , u'Value' , ), 56, (56, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 252 , (3, 0, None, None) , 0 , )),
	(( u'EngineValid' , u'Value' , ), 56, (56, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( u'DecodeTemplate' , u'ASour' , u'ADest' , u'Value' , ), 2, (2, (), [ 
			(8, 1, None, None) , (16396, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 260 , (3, 0, None, None) , 0 , )),
	(( u'EncodeTemplate' , u'ASour' , u'ADest' , u'Value' , ), 3, (3, (), [ 
			(12, 1, None, None) , (16392, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( u'BeginCapture' , ), 4, (4, (), [ ], 1 , 1 , 4 , 0 , 268 , (3, 0, None, None) , 0 , )),
	(( u'CancelCapture' , ), 5, (5, (), [ ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( u'EndEngine' , ), 27, (27, (), [ ], 1 , 1 , 4 , 0 , 276 , (3, 0, None, None) , 0 , )),
	(( u'DecodeTemplate1' , u'ASour' , u'Value' , ), 31, (31, (), [ (8, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( u'EncodeTemplate1' , u'ASour' , u'Value' , ), 33, (33, (), [ (12, 1, None, None) , 
			(16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 284 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateStrToFPCacheDB' , u'fpcHandle' , u'FPID' , u'ARegTemplateStr' , u'Value' , 
			), 35, (35, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( u'VerFingerFromStr' , u'regTemplateStr' , u'verTemplateStr' , u'ADoLearning' , u'ARegFeatureChanged' , 
			u'Value' , ), 36, (36, (), [ (16392, 3, None, None) , (8, 1, None, None) , (11, 1, None, None) , 
			(16395, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 292 , (3, 0, None, None) , 0 , )),
	(( u'GetTemplateAsString' , u'Value' , ), 39, (39, (), [ (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( u'IsOneToOneTemplateStr' , u'ATemplate' , u'Value' , ), 48, (48, (), [ (8, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 300 , (3, 0, None, None) , 0 , )),
	(( u'ModifyTemplateStr' , u'ATemplate' , u'AOneToOne' , ), 57, (57, (), [ (16392, 3, None, None) , 
			(11, 1, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( u'SaveTemplateStr' , u'FileName' , u'ATemplateStr' , ), 61, (61, (), [ (8, 1, None, None) , 
			(8, 1, None, None) , ], 1 , 1 , 4 , 0 , 308 , (3, 0, None, None) , 0 , )),
	(( u'GetTemplateCount' , u'AFPHandle' , u'AOneToOneCnt' , u'ATotalCnt' , ), 62, (62, (), [ 
			(3, 1, None, None) , (16387, 3, None, None) , (16387, 3, None, None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( u'IdentificationInFPCacheDB' , u'fpcHandle' , u'pVerTemplate' , u'Score' , u'ProcessedFPNumber' , 
			u'Value' , ), 64, (64, (), [ (3, 1, None, None) , (12, 1, None, None) , (16387, 3, None, None) , 
			(16387, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 316 , (3, 0, None, None) , 0 , )),
	(( u'IdentificationFromFileInFPCacheDB' , u'fpcHandle' , u'pVerTemplateFile' , u'Score' , u'ProcessedFPNumber' , 
			u'Value' , ), 65, (65, (), [ (3, 1, None, None) , (8, 1, None, None) , (16387, 3, None, None) , 
			(16387, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( u'IdentificationFromStrInFPCacheDB' , u'fpcHandle' , u'AVerTemplateStr' , u'Score' , u'ProcessedFPNumber' , 
			u'Value' , ), 66, (66, (), [ (3, 1, None, None) , (8, 1, None, None) , (16387, 3, None, None) , 
			(16387, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 324 , (3, 0, None, None) , 0 , )),
	(( u'SetAutoIdentifyPara' , u'AAutoIdentify' , u'ACacheDBHandle' , u'AScore' , ), 17, (17, (), [ 
			(11, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( u'SetImageDirection' , u'AIsImageChange' , ), 41, (41, (), [ (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 332 , (3, 0, None, None) , 0 , )),
	(( u'IsOneToOneTemplateFile' , u'ATemplateFileName' , u'Value' , ), 34, (34, (), [ (8, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( u'ModifyTemplateFile' , u'ATemplateFileName' , u'AOneToOne' , ), 58, (58, (), [ (8, 1, None, None) , 
			(11, 1, None, None) , ], 1 , 1 , 4 , 0 , 340 , (3, 0, None, None) , 0 , )),
	(( u'GetVerTemplate' , u'Value' , ), 59, (59, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( u'GetVerScore' , u'Value' , ), 60, (60, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 348 , (3, 0, None, None) , 0 , )),
	(( u'AddImageFile' , u'AFileName' , u'ADPI' , u'Value' , ), 63, (63, (), [ 
			(8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( u'SetOneToOnePara' , u'ADoLearning' , u'AMatchSecurity' , ), 67, (67, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , ], 1 , 1 , 4 , 0 , 356 , (3, 0, None, None) , 0 , )),
	(( u'CompressTemplate' , u'ATemplate' , u'Value' , ), 68, (68, (), [ (8, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( u'ConvertAttTemplate' , u'ATemplate' , u'Value' , ), 70, (70, (), [ (12, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 364 , (3, 0, None, None) , 0 , )),
	(( u'ForceSecondMatch' , u'Value' , ), 71, (71, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( u'ForceSecondMatch' , u'Value' , ), 71, (71, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 372 , (3, 0, None, None) , 0 , )),
	(( u'AddBitmap' , u'BitmapHandle' , u'ValidRectX1' , u'ValidRectY1' , u'ValidRectX2' , 
			u'ValidRectY2' , u'DPI' , u'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( u'UsingXTFTemplate' , u'ADoUsingXTFTemplate' , ), 202, (202, (), [ (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 380 , (3, 0, None, None) , 0 , )),
	(( u'ExtractImageFromURU4000' , u'AOriImageBuf' , u'Size' , u'AAutoIdentify' , u'iResult' , 
			u'Value' , ), 69, (69, (), [ (30, 1, None, None) , (3, 1, None, None) , (11, 1, None, None) , 
			(16396, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( u'ConvertToBiokey' , u'OriTemplate' , u'NewTemlate' , ), 204, (204, (), [ (12, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 388 , (3, 0, None, None) , 0 , )),
	(( u'GenRegTemplateAsStringFromFile' , u'AImageFileName' , u'ADPI' , u'ADest' , u'Value' , 
			), 205, (205, (), [ (8, 1, None, None) , (3, 1, None, None) , (16392, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( u'GenVerTemplateAsStringFromFile' , u'AImageFileName' , u'ADPI' , u'ADest' , u'Value' , 
			), 206, (206, (), [ (8, 1, None, None) , (3, 1, None, None) , (16392, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 396 , (3, 0, None, None) , 0 , )),
	(( u'ExtractImageFromURU' , u'AOriImageStr' , u'Size' , u'AAutoIdentify' , u'iResult' , 
			u'Value' , ), 691, (691, (), [ (8, 1, None, None) , (3, 1, None, None) , (11, 1, None, None) , 
			(16396, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( u'Vendor' , u'Value' , ), 203, (203, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 404 , (3, 0, None, None) , 0 , )),
	(( u'ProduceName' , u'Value' , ), 207, (207, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( u'SetTemplateLen' , u'ATemplate' , u'ALen' , u'Value' , ), 208, (208, (), [ 
			(16396, 3, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 412 , (3, 0, None, None) , 0 , )),
	(( u'ControlSensor' , u'ACode' , u'AValue' , u'Value' , ), 209, (209, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( u'IsSupportAuxDevice' , u'Value' , ), 210, (210, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 420 , (3, 0, None, None) , 0 , )),
	(( u'ExtractImageFromTerminal' , u'AOriImage' , u'Size' , u'AAutoIdentify' , u'iResult' , 
			u'Value' , ), 211, (211, (), [ (12, 1, None, None) , (3, 1, None, None) , (11, 1, None, None) , 
			(16396, 3, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( u'CreateFPCacheDBEx' , u'Value' , ), 212, (212, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 428 , (3, 0, None, None) , 0 , )),
	(( u'FreeFPCacheDBEx' , u'fpcHandle' , ), 213, (213, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateToFPCacheDBEx' , u'fpcHandle' , u'FPID' , u'pRegTemplate' , u'pRegTemplate10' , 
			u'Value' , ), 214, (214, (), [ (3, 1, None, None) , (3, 1, None, None) , (12, 1, None, None) , 
			(12, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 436 , (3, 0, None, None) , 0 , )),
	(( u'RemoveRegTemplateFromFPCacheDBEx' , u'fpcHandle' , u'FPID' , u'Value' , ), 215, (215, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateFileToFPCacheDBEx' , u'fpcHandle' , u'FPID' , u'pRegTemplateFile' , u'pRegTemplate10File' , 
			u'Value' , ), 216, (216, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , 
			(8, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 444 , (3, 0, None, None) , 0 , )),
	(( u'GetTemplateEx' , u'AFPEngineVersion' , u'Value' , ), 217, (217, (), [ (8, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( u'AddRegTemplateStrToFPCacheDBEx' , u'fpcHandle' , u'FPID' , u'ARegTemplateStr' , u'ARegTemplate10Str' , 
			u'Value' , ), 218, (218, (), [ (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , 
			(8, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 452 , (3, 0, None, None) , 0 , )),
	(( u'GetTemplateAsStringEx' , u'AFPEngineVersion' , u'Value' , ), 219, (219, (), [ (8, 1, None, None) , 
			(16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( u'GetVerTemplateEx' , u'AFPEngineVersion' , u'Value' , ), 220, (220, (), [ (8, 1, None, None) , 
			(16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 460 , (3, 0, None, None) , 0 , )),
	(( u'MF_GET_SNR' , u'commHandle' , u'DeviceAddress' , u'mode' , u'RDM_halt' , 
			u'snr' , u'Value' , u'pVal' , ), 221, (221, (), [ (3, 1, None, None) , 
			(3, 1, None, None) , (17, 1, None, None) , (17, 1, None, None) , (16401, 1, None, None) , (16401, 1, None, None) , 
			(16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( u'MF_GetSerNum' , u'commHandle' , u'DeviceAddress' , u'buffer' , u'pVal' , 
			), 222, (222, (), [ (3, 1, None, None) , (3, 1, None, None) , (16401, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 468 , (3, 0, None, None) , 0 , )),
	(( u'MF_SetSerNum' , u'commHandle' , u'DeviceAddress' , u'newValue' , u'buffer' , 
			u'pVal' , ), 223, (223, (), [ (3, 1, None, None) , (3, 1, None, None) , (16401, 1, None, None) , 
			(16401, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( u'MF_GetVersionNum' , u'commHandle' , u'DeviceAddress' , u'VersionNum' , u'pVal' , 
			), 224, (224, (), [ (3, 1, None, None) , (3, 1, None, None) , (16401, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 476 , (3, 0, None, None) , 0 , )),
	(( u'MF_PCDRead' , u'commHandle' , u'DeviceAddress' , u'mode' , u'blkIndex' , 
			u'blkNum' , u'key' , u'buffer' , u'pVal' , ), 225, (225, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (17, 1, None, None) , (17, 1, None, None) , (17, 1, None, None) , 
			(16401, 3, None, None) , (16401, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( u'MF_PCDWrite' , u'commHandle' , u'DeviceAddress' , u'mode' , u'blkIndex' , 
			u'blkNum' , u'key' , u'buffer' , u'pVal' , ), 226, (226, (), [ 
			(3, 1, None, None) , (3, 1, None, None) , (17, 1, None, None) , (17, 1, None, None) , (17, 1, None, None) , 
			(16401, 3, None, None) , (16401, 3, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 484 , (3, 0, None, None) , 0 , )),
	(( u'ReservedParam' , u'Value' , ), 228, (228, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( u'IsReturnNoLic' , u'Value' , ), 227, (227, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 492 , (3, 0, None, None) , 0 , )),
	(( u'IsReturnNoLic' , u'Value' , ), 227, (227, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{CA69969C-2F27-41D3-954D-A48B941C3BA7}' : ZKFPEngX,
	'{161A8D2D-3DDE-4744-BA38-08F900D10D6D}' : IZKFPEngX,
	'{8AEE2E53-7EBE-4B51-A964-009ADC68D107}' : IZKFPEngXEvents,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{161A8D2D-3DDE-4744-BA38-08F900D10D6D}' : 'IZKFPEngX',
}


NamesToIIDMap = {
	'IZKFPEngXEvents' : '{8AEE2E53-7EBE-4B51-A964-009ADC68D107}',
	'IZKFPEngX' : '{161A8D2D-3DDE-4744-BA38-08F900D10D6D}',
}


