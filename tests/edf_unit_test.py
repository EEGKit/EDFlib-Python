#!/usr/bin/env python3

import sys
sys.path.append("../")
import io
import numpy as np
from struct import *
from datetime import datetime
from edfreader import EDFreader
from edfreader import EDFexception
from edfwriter import EDFwriter

if sys.version_info[0] != 3 or sys.version_info[1] < 5:
  print("Must be using Python version >= 3.5.0")
  sys.exit()

if np.__version__ < "1.17.0":
  print("Must be using NumPy version >= 1.17.0")
  sys.exit()

def dblcmp(val1, val2):
  diff = val1 - val2

  if diff > 1e-13:
    return 1
  else:
   if -diff > 1e-13:
     return -1
   else:
     return 0

def dblcmp_lim(val1, val2, lim):
  diff = val1 - val2

  if diff > lim:
    return 1
  else:
    if -diff > lim:
      return -1
    else:
      return 0

def modify_and_try(path, offset, b):

  fp = open(path, "rb+")

  fp.seek(offset, io.SEEK_SET)

  fp.write(b)

  fp.close()

  try:
    hdl = EDFreader(path)
  except EDFexception:
    return 3

  if hdl.close() != 0:
    return 6

  return 7

################################### EDF writing ###############################

dbuf = np.zeros(10240, dtype = np.float64)

sbuf = np.zeros(300, dtype = np.int16)

ibuf = np.zeros(300, dtype = np.int32)

hdl_out = EDFwriter("test4.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 1)

assert(hdl_out.version() == 106)

assert(hdl_out.setSampleFrequency(0, 10239) == 0)
assert(hdl_out.setPhysicalMaximum(0, -10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -30000) == 0)
assert(hdl_out.setDigitalMaximum(0, 10000) == 0)
assert(hdl_out.setDigitalMinimum(0, -10000) == 0)
assert(hdl_out.setPatientName("Xohn Doe") == 0)
assert(hdl_out.setPatientCode("X1234") == 0)
assert(hdl_out.setAdditionalPatientInfo("Xop") == 0)
assert(hdl_out.setAdministrationCode("X89") == 0)
assert(hdl_out.setTechnician("Xichard Roe") == 0)
assert(hdl_out.setEquipment("Xevice") == 0)
assert(hdl_out.writeSamples(dbuf) == 0)
assert(hdl_out.close() == 0)

hdl_out = EDFwriter("test.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 512)

for i in range(0, 512):
  assert(hdl_out.setSampleFrequency(i, 10239) == 0)
  assert(hdl_out.setPhysicalMaximum(i, -10000) == 0)
  assert(hdl_out.setPhysicalMinimum(i, -30000) == 0)
  assert(hdl_out.setDigitalMaximum(i, 10000) == 0)
  assert(hdl_out.setDigitalMinimum(i, -10000) == 0)
assert(hdl_out.writeSamples(dbuf) == 0)
assert(hdl_out.close() == 0)

hdl_out = EDFwriter("test.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 512)

for i in range(0, 512):
  assert(hdl_out.setSampleFrequency(i, 10240) == 0)
  assert(hdl_out.setPhysicalMaximum(i, -10000) == 0)
  assert(hdl_out.setPhysicalMinimum(i, -30000) == 0)
  assert(hdl_out.setDigitalMaximum(i, 10000) == 0)
  assert(hdl_out.setDigitalMinimum(i, -10000) == 0)
assert(hdl_out.writeSamples(dbuf) == hdl_out.EDFLIB_DATARECORD_SIZE_TOO_BIG)
assert(hdl_out.close() == 0)

chns = 2

hdl_out = EDFwriter("test.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, chns)

assert(hdl_out.setSampleFrequency(0, 20) == 0)
assert(hdl_out.setSampleFrequency(1, 23) == 0)
assert(hdl_out.setPhysicalMaximum(0, 10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -5000) == 0)
assert(hdl_out.setPhysicalMaximum(1, -10000) == 0)
assert(hdl_out.setPhysicalMinimum(1, -30000) == 0)
assert(hdl_out.setDigitalMaximum(0, 10000) == 0)
assert(hdl_out.setDigitalMinimum(0, -10000) == 0)
assert(hdl_out.setDigitalMaximum(1, 30000) == 0)
assert(hdl_out.setDigitalMinimum(1, 10000) == 0)
assert(hdl_out.setSignalLabel(0, "trace1") == 0)
assert(hdl_out.setSignalLabel(1, "trace2") == 0)
assert(hdl_out.setPreFilter(0, "qwerty") == 0)
assert(hdl_out.setPreFilter(1, "zxcvbn") == 0)
assert(hdl_out.setTransducer(0, "asdfgh") == 0)
assert(hdl_out.setTransducer(1, "poklhyg") == 0)
assert(hdl_out.setPhysicalDimension(0, "\xb5Vxxxxxxxxxxxxxxxxxxxx") == 0)
assert(hdl_out.setPhysicalDimension(1, "\xb0\xf8xxxxxxxxxxxxxxxxxxxx") == 0)
assert(hdl_out.setStartDateTime(2017, 12, 5, 12, 23, 8, 0) == 0)
assert(hdl_out.setPatientName("John Doe") == 0)
assert(hdl_out.setPatientCode("01234") == 0)
assert(hdl_out.setPatientGender(1) == 0)
assert(hdl_out.setPatientBirthDate(2010, 7, 4) == 0)
assert(hdl_out.setAdditionalPatientInfo("nop") == 0)
assert(hdl_out.setAdministrationCode("789") == 0)
assert(hdl_out.setTechnician("Richard Roe") == 0)
assert(hdl_out.setEquipment("device") == 0)
assert(hdl_out.setNumberOfAnnotationSignals(3) == 0)
assert(hdl_out.setDataRecordDuration(130000) == 0)
assert(hdl_out.writeAnnotation(0, -1, "Recording starts") == 0)
assert(hdl_out.writeAnnotation(9000, 1000, "Test 1") == 0)
assert(hdl_out.writeAnnotation(13000, -1, "Recording ends") == 0)
assert(hdl_out.writeAnnotation(8200, 1653, "Test 2") == 0)

for i in range(0, 20):
  dbuf[i] = -5100 + (i * 800)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 23):
  dbuf[i] = -30100 + (i * 909)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 20):
  dbuf[i] = -5100 + (i * 800)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 23):
  dbuf[i] = -30100 + (i * 909)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 20):
  sbuf[i] = -10100 + (i * 1053)
assert(hdl_out.writeSamples(sbuf) == 0)

for i in range(0, 23):
  sbuf[i] = 9900 + (i * 1053)
assert(hdl_out.writeSamples(sbuf) == 0)

for i in range(0, 20):
  sbuf[i] = -10100 + (i * 1053)
assert(hdl_out.writeSamples(sbuf) == 0)

for i in range(0, 23):
  sbuf[i] = 9900 + (i * 1053)
assert(hdl_out.writeSamples(sbuf) == 0)

for i in range(0, 20):
  ibuf[i] = -10100 + (i * 1053)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 9900 + (i * 1053)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 20):
  ibuf[i] = -10100 + (i * 1053)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 9900 + (i * 1053)
assert(hdl_out.writeSamples(ibuf) == 0)

ival1 = -10100

ival2 = 9900

for j in range(0, 4):
  for i in range(0, 20):
    ibuf[i] = ival1
    ival1 += 253

  assert(hdl_out.writeSamples(ibuf) == 0)

  for i in range(0, 23):
    ibuf[i] = ival2
    ival2 += 253
  assert(hdl_out.writeSamples(ibuf) == 0)

assert(hdl_out.close() == 0)

################################### BDF writing ###############################

hdl_out = EDFwriter("test.bdf", EDFwriter.EDFLIB_FILETYPE_BDFPLUS, 512)

for i in range(0, 512):
  assert(hdl_out.setSampleFrequency(i, 10239) == 0)
  assert(hdl_out.setPhysicalMaximum(i, -10000) == 0)
  assert(hdl_out.setPhysicalMinimum(i, -30000) == 0)
  assert(hdl_out.setDigitalMaximum(i, 10000) == 0)
  assert(hdl_out.setDigitalMinimum(i, -10000) == 0)
assert(hdl_out.writeSamples(dbuf) == 0)
assert(hdl_out.close() == 0)

hdl_out = EDFwriter("test.bdf", EDFwriter.EDFLIB_FILETYPE_BDFPLUS, 512)

for i in range(0, 512):
  assert(hdl_out.setSampleFrequency(i, 10240) == 0)
  assert(hdl_out.setPhysicalMaximum(i, -10000) == 0)
  assert(hdl_out.setPhysicalMinimum(i, -30000) == 0)
  assert(hdl_out.setDigitalMaximum(i, 10000) == 0)
  assert(hdl_out.setDigitalMinimum(i, -10000) == 0)
assert(hdl_out.writeSamples(dbuf) == hdl_out.EDFLIB_DATARECORD_SIZE_TOO_BIG)
assert(hdl_out.close() == 0)

hdl_out = EDFwriter("test.bdf", EDFwriter.EDFLIB_FILETYPE_BDFPLUS, chns)

assert(hdl_out.setSampleFrequency(0, 20) == 0)
assert(hdl_out.setSampleFrequency(1, 23) == 0)
assert(hdl_out.setPhysicalMaximum(0, 10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -5000) == 0)
assert(hdl_out.setPhysicalMaximum(1, -10000) == 0)
assert(hdl_out.setPhysicalMinimum(1, -30000) == 0)
assert(hdl_out.setDigitalMaximum(0, 1000000) == 0)
assert(hdl_out.setDigitalMinimum(0, -1000000) == 0)
assert(hdl_out.setDigitalMaximum(1, 3000000) == 0)
assert(hdl_out.setDigitalMinimum(1, 1000000) == 0)
assert(hdl_out.setSignalLabel(0, "trace1") == 0)
assert(hdl_out.setSignalLabel(1, "trace2") == 0)
assert(hdl_out.setPreFilter(0, "qwerty") == 0)
assert(hdl_out.setPreFilter(1, "zxcvbn") == 0)
assert(hdl_out.setTransducer(0, "asdfgh") == 0)
assert(hdl_out.setTransducer(1, "poklhyg") == 0)
assert(hdl_out.setPhysicalDimension(0, "\xb5Vxxxxxxxxxxxxxxxxxxxx") == 0)
assert(hdl_out.setPhysicalDimension(1, "\xb0\xf8xxxxxxxxxxxxxxxxxxxx") == 0)
assert(hdl_out.setStartDateTime(2017, 12, 5, 12, 23, 8, 0) == 0)
assert(hdl_out.setPatientName("John Doe") == 0)
assert(hdl_out.setPatientCode("01234") == 0)
assert(hdl_out.setPatientGender(1) == 0)
assert(hdl_out.setPatientBirthDate(2010, 7, 4) == 0)
assert(hdl_out.setAdditionalPatientInfo("nop") == 0)
assert(hdl_out.setAdministrationCode("789") == 0)
assert(hdl_out.setTechnician("Richard Roe") == 0)
assert(hdl_out.setEquipment("device") == 0)
assert(hdl_out.setNumberOfAnnotationSignals(3) == 0)
assert(hdl_out.setDataRecordDuration(117000) == 0)
assert(hdl_out.writeAnnotation(0, -1, "Recording starts") == 0)
assert(hdl_out.writeAnnotation(6000, 2000, "Test 2") == 0)
assert(hdl_out.writeAnnotation(11700, -1, "Recording ends") == 0)

for i in range(0, 20):
  dbuf[i] = -5100 + (i * 800)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 23):
  dbuf[i] = -30100 + (i * 909)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 20):
  dbuf[i] = -5100 + (i * 800)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 23):
  dbuf[i] = -30100 + (i * 909)
assert(hdl_out.writeSamples(dbuf) == 0)

for i in range(0, 20):
  ibuf[i] = -1010000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 990000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 20):
  ibuf[i] = -1010000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 990000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 20):
  ibuf[i] = -1010000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 990000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 20):
  ibuf[i] = -1010000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

for i in range(0, 23):
  ibuf[i] = 990000 + (i * 105300)
assert(hdl_out.writeSamples(ibuf) == 0)

ival1 = -1010000

ival2 = 990000

for j in range(0, 4):
  for i in range(0, 20):
    ibuf[i] = ival1
    ival1 += 25300

  assert(hdl_out.writeSamples(ibuf) == 0)

  for i in range(0, 23):
    ibuf[i] = ival2
    ival2 += 25300
  assert(hdl_out.writeSamples(ibuf) == 0)

assert(hdl_out.close() == 0)

################################### EDF reading ###############################

hdl_in = EDFreader("test4.edf")

assert(hdl_in.version() == 106)
assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_EDFPLUS)
assert(hdl_in.getNumSignals() == 1)
assert(hdl_in.getPatientName() == "Xohn Doe")
assert(hdl_in.getPatientCode() == "X1234")
assert(hdl_in.getPatientAdditional()[0 : 3] == "Xop")
assert(hdl_in.getAdministrationCode() == "X89")
assert(hdl_in.getTechnician() == "Xichard Roe")
assert(hdl_in.getEquipment() == "Xevice")
assert(hdl_in.close() == 0)

hdl_in = EDFreader("test.edf")

assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_EDFPLUS)
assert(hdl_in.getNumSignals() == 2)
assert(dblcmp_lim(hdl_in.getSampleFrequency(0), 153.8461538, 1e-6) == 0)
assert(dblcmp_lim(hdl_in.getSampleFrequency(1), 176.9230769, 1e-6) == 0)
assert(hdl_in.getTotalSamples(0) == 200)
assert(hdl_in.getTotalSamples(1) == 230)
assert((hdl_in.getNumDataRecords() * hdl_in.getLongDataRecordDuration()) == 13000000)
assert(hdl_in.getStartDateDay() == 5)
assert(hdl_in.getStartDateMonth() == 12)
assert(hdl_in.getStartDateYear() == 2017)
assert(hdl_in.getStartTimeSecond() == 8)
assert(hdl_in.getStartTimeMinute() == 23)
assert(hdl_in.getStartTimeHour() == 12)
assert(hdl_in.getStartTimeSubSecond() == 0)
dt = hdl_in.getStartDateTime()
assert(dt.day == 5)
assert(dt.month == 12)
assert(dt.year == 2017)
assert(dt.second == 8)
assert(dt.minute == 23)
assert(dt.hour == 12)
assert(dt.microsecond == 0)
assert(hdl_in.getPatientName() == "John Doe")
assert(hdl_in.getPatientCode() == "01234")
assert(hdl_in.getPatientGender() == "Male")
assert(hdl_in.getPatientBirthDate() == "04 jul 2010")
assert(hdl_in.getPatientAdditional()[0 : 3] == "nop")
assert(hdl_in.getAdministrationCode() == "789")
assert(hdl_in.getTechnician() == "Richard Roe")
assert(hdl_in.getEquipment() == "device")
assert(hdl_in.getLongDataRecordDuration() == 1300000)
assert(hdl_in.getNumDataRecords() == 10)
assert(hdl_in.getSignalLabel(0) == "trace1          ")
assert(hdl_in.getSignalLabel(1) == "trace2          ")
assert(hdl_in.getPhysicalMaximum(0) == 10000)
assert(hdl_in.getPhysicalMaximum(1) == -10000)
assert(hdl_in.getPhysicalMinimum(0) == -5000)
assert(hdl_in.getPhysicalMinimum(1) == -30000)
assert(hdl_in.getDigitalMaximum(0) == 10000)
assert(hdl_in.getDigitalMaximum(1) == 30000)
assert(hdl_in.getDigitalMinimum(0) == -10000)
assert(hdl_in.getDigitalMinimum(1) == 10000)
assert(hdl_in.getSampelsPerDataRecord(0) == 20)
assert(hdl_in.getSampelsPerDataRecord(1) == 23)
assert(hdl_in.getPhysicalDimension(0) == "uVxxxxxx")
assert(hdl_in.getPhysicalDimension(1) == " 0xxxxxx")
assert(hdl_in.getPreFilter(0)[0 : 9] == "qwerty   ")
assert(hdl_in.getPreFilter(1)[0 : 9] == "zxcvbn   ")
assert(hdl_in.getTransducer(0)[0 : 9] == "asdfgh   ")
assert(hdl_in.getTransducer(1)[0 : 9] == "poklhyg  ")
assert(len(hdl_in.annotationslist) == 4)
assert(hdl_in.annotationslist[0].onset == 0)
assert(hdl_in.annotationslist[0].duration == -1)
assert(hdl_in.annotationslist[0].description == "Recording starts")
assert(hdl_in.annotationslist[1].onset == 9000000)
assert(hdl_in.annotationslist[1].duration == 1000000)
assert(hdl_in.annotationslist[1].description == "Test 1")
assert(hdl_in.annotationslist[2].onset == 13000000)
assert(hdl_in.annotationslist[2].duration == -1)
assert(hdl_in.annotationslist[2].description == "Recording ends")
assert(hdl_in.annotationslist[3].onset == 8200000)
assert(hdl_in.annotationslist[3].duration == 1653000)
assert(hdl_in.annotationslist[3].description == "Test 2")

assert(hdl_in.fseek(1, 400, hdl_in.EDFSEEK_SET) != 400)
assert(hdl_in.fseek(0, 412, hdl_in.EDFSEEK_SET) != 412)
assert(hdl_in.fseek(0, 20, hdl_in.EDFSEEK_SET) == 20)
assert(hdl_in.readSamples(0, dbuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(dblcmp(dbuf[i], -5000) == 0)
    continue

  if i == 19:
    assert(dblcmp(dbuf[i], 10000) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -5100 + (i * 800), 0.75) == 0)

assert(hdl_in.fseek(1, 23, hdl_in.EDFSEEK_SET) == 23)
assert(hdl_in.readSamples(1, dbuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(dblcmp(dbuf[i], -30000) == 0)
    continue

  assert(dblcmp(dbuf[i], -30100 + (i * 909)) == 0)

hdl_in.rewind(0)

assert(hdl_in.readSamples(0, dbuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(dblcmp(dbuf[i], -5000) == 0)
    continue

  if i == 19:
    assert(dblcmp(dbuf[i], 10000) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -5100 + (i * 800), 0.75) == 0)

hdl_in.rewind(1)

assert(hdl_in.readSamples(1, dbuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(dblcmp(dbuf[i], -30000) == 0)
    continue

  assert(dblcmp(dbuf[i], -30100 + (i * 909)) == 0)

assert(hdl_in.fseek(0, 40, hdl_in.EDFSEEK_SET) == 40)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -10000)
    continue

assert(ibuf[i] == -10100 + (i * 1053))

assert(hdl_in.fseek(1, 46, hdl_in.EDFSEEK_SET) == 46)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 10000)
    continue

  if (i == 20) or (i == 21):
    assert(ibuf[i] == 30000)
    continue

  if i == 22:
    assert(ibuf[i] == 10000)
    continue

  assert(ibuf[i] == 9900 + (i * 1053))

assert(hdl_in.fseek(0, 80, hdl_in.EDFSEEK_SET) == 80)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -10000)
    continue

  assert(ibuf[i] == -10100 + (i * 1053))

assert(hdl_in.fseek(1, 92, hdl_in.EDFSEEK_SET) == 92)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 10000)
    continue

  if i >= 20:
    assert(ibuf[i] == 30000)
    continue

  assert(ibuf[i] == 9900 + (i * 1053))

assert(hdl_in.fseek(0, 60, hdl_in.EDFSEEK_SET) == 60)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -10000)
    continue

  assert(ibuf[i] == -10100 + (i * 1053))

assert(hdl_in.fseek(1, 69, hdl_in.EDFSEEK_SET) == 69)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 10000)
    continue

  if (i == 20) or (i == 21):
    assert(ibuf[i] == 30000)
    continue

  if i == 22:
    assert(ibuf[i] == 10000)
    continue

  assert(ibuf[i] == 9900 + (i * 1053))

assert(hdl_in.fseek(0, 100, hdl_in.EDFSEEK_SET) == 100)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -10000)
    continue

  assert(ibuf[i] == -10100 + (i * 1053))

assert(hdl_in.fseek(1, 115, hdl_in.EDFSEEK_SET) == 115)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 10000)
    continue

  if i >= 20:
    assert(ibuf[i] == 30000)
    continue

  assert(ibuf[i] == 9900 + (i * 1053))

assert(hdl_in.readSamples(0, ibuf, 80) == 80)

for i in range(0, 80):
  if i == 0:
    assert(ibuf[i] == -10000)
    continue

  assert(ibuf[i] == -10100 + (i * 253))

assert(hdl_in.readSamples(1, ibuf, 92) == 92)

for i in range(0, 92):
  if i == 0:
    assert(ibuf[i] == 10000)
    continue

  if i >= 80:
    assert(ibuf[i] == 30000)
    continue

  assert(ibuf[i] == 9900 + (i * 253))

assert(hdl_in.fseek(0, 185, hdl_in.EDFSEEK_SET) == 185)

assert(hdl_in.readSamples(0, ibuf, 15) == 15)

for i in range(0, 15):
  assert(ibuf[i] == -10100 + ((i + 65) * 253))

assert(hdl_in.fseek(0, 115, hdl_in.EDFSEEK_SET) == 115)

assert(hdl_in.readSamples(0, ibuf, 80) == 80)

for i in range(0, 5):
  assert(ibuf[i] == 5695 + (i * 1053))
assert(ibuf[5] == -10000)
for i in range(6, 80):
  assert(ibuf[i] == -10100 + ((i - 5) * 253))

assert(hdl_in.close() == 0)

#############################################

assert(modify_and_try("test.edf", 1, bytes("1", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 1, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 16, bytes(" ", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 16, bytes("0", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0xaa, bytes(":", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0xaa, bytes(".", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0xab, bytes("9", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0xab, bytes("1", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0xac, bytes("q", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0xac, bytes("2", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0xc4, bytes("D", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0xc4, bytes("C", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x12e, bytes(" ", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x12e, bytes("s", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x1ac, bytes(chr(181), encoding="latin_1")) == 3)

###################################

assert(modify_and_try("test.edf", 0x1ac, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x308, bytes(" ", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x308, bytes("-", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x30d, bytes(",", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x30d, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x3a5, bytes(".", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x3a5, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x3bc, bytes(chr(207), encoding="latin_1"))  == 3)

###################################

assert(modify_and_try("test.edf", 0x3bc, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x40b, bytes(chr(247), encoding="latin_1")) == 3)

###################################

assert(modify_and_try("test.edf", 0x40b, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x560, bytes(chr(127), encoding="latin_1")) == 3)

###################################

assert(modify_and_try("test.edf", 0x560, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x5ff, bytes(chr(13), encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x5ff, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x54a, bytes(".", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x54a, bytes(" ", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0xad, bytes("-", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0xad, bytes(".", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x803, bytes("0.12", encoding="ascii")) == 3)

assert(modify_and_try("test.edf", 0x803, bytes("0.131", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x803, bytes("0.130", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x802, bytes("-", encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x802, bytes("+", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x750, bytes(chr(0), encoding="ascii")) == 3)

###################################

assert(modify_and_try("test.edf", 0x750, bytes(chr(0x14), encoding="latin_1")) == 7)

assert(modify_and_try("test.edf", 0x751, bytes(chr(0), encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.edf", 0x358, bytes("-32769", encoding="ascii")) == 3)

assert(modify_and_try("test.edf", 0x358, bytes("-10000", encoding="ascii")) == 7)

assert(modify_and_try("test.edf", 0x380, bytes("32768", encoding="ascii")) == 3)

assert(modify_and_try("test.edf", 0x380, bytes("10000", encoding="ascii")) == 7)

###################################

fp = open("test.edf", "rb")

fp.seek(0x600, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  if i >= 19:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  assert(dblcmp_lim(unpack_from("<h", rbuf, i * 2)[0], ((-5100 + (i * 800)) / 0.75) - 3333.333333, 1.0001) == 0)

###################################

fp = open("test.edf", "rb")

fp.seek(0x628, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if i >= 19:
    assert(unpack_from("<h", rbuf, i * 2)[0] == (-30100 + (i * 909)) + 40000)
    continue

###################################

fp = open("test.edf", "rb")

fp.seek(0x7ac, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  if i >= 19:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  assert(dblcmp_lim(unpack_from("<h", rbuf, i * 2)[0], ((-5100 + (i * 800)) / 0.75) - 3333.333333, 1.0001) == 0)

###################################

fp = open("test.edf", "rb")

fp.seek(0x7d4, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if i >= 19:
    assert(unpack_from("<h", rbuf, i * 2)[0] == (-30100 + (i * 909)) + 40000)
    continue

###################################

fp = open("test.edf", "rb")

fp.seek(0x958, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == -10100 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0x980, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if (i == 0) or (i == 22):
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if (i == 20) or (i == 21):
    assert(unpack_from("<h", rbuf, i * 2)[0] == 30000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == 9900 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xb04, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == -10100 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xb2c, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if (i == 0) or (i == 22):
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if (i == 20) or (i == 21):
    assert(unpack_from("<h", rbuf, i * 2)[0] == 30000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == 9900 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xcb0, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == -10100 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xcd8, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if i >= 20:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 30000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == 9900 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xe5c, io.SEEK_SET)

rbuf = fp.read(40)

fp.close()

for i in range(0, 20):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == -10000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == -10100 + (i * 1053))

###################################

fp = open("test.edf", "rb")

fp.seek(0xe84, io.SEEK_SET)

rbuf = fp.read(46)

fp.close()

for i in range(0, 23):
  if i == 0:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 10000)
    continue

  if i >= 20:
    assert(unpack_from("<h", rbuf, i * 2)[0] == 30000)
    continue

  assert(unpack_from("<h", rbuf, i * 2)[0] == 9900 + (i * 1053))

################################### BDF reading ###############################

hdl_in = EDFreader("test.bdf")

assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_BDFPLUS)
assert(hdl_in.getNumSignals() == 2)
assert(dblcmp_lim(hdl_in.getSampleFrequency(0), 170.9401709, 1e-5) == 0)
assert(dblcmp_lim(hdl_in.getSampleFrequency(1), 196.5811996, 1e-5) == 0)
assert(hdl_in.getTotalSamples(0) == 200)
assert(hdl_in.getTotalSamples(1) == 230)
assert((hdl_in.getNumDataRecords() * hdl_in.getLongDataRecordDuration()) == 11700000)
assert(hdl_in.getStartDateDay() == 5)
assert(hdl_in.getStartDateMonth() == 12)
assert(hdl_in.getStartDateYear() == 2017)
assert(hdl_in.getStartTimeSecond() == 8)
assert(hdl_in.getStartTimeMinute() == 23)
assert(hdl_in.getStartTimeHour() == 12)
assert(hdl_in.getStartTimeSubSecond() == 0)
assert(hdl_in.getPatientName() == "John Doe")
assert(hdl_in.getPatientCode() == "01234")
assert(hdl_in.getPatientGender() == "Male")
assert(hdl_in.getPatientBirthDate() == "04 jul 2010")
assert(hdl_in.getPatientAdditional()[0 : 3] == "nop")
assert(hdl_in.getAdministrationCode() == "789")
assert(hdl_in.getTechnician() == "Richard Roe")
assert(hdl_in.getEquipment() == "device")
assert(hdl_in.getLongDataRecordDuration() == 1170000)
assert(hdl_in.getNumDataRecords() == 10)
assert(len(hdl_in.annotationslist) == 3)
assert(hdl_in.getSignalLabel(0) == "trace1          ")
assert(hdl_in.getSignalLabel(1) == "trace2          ")
assert(hdl_in.getPhysicalMaximum(0) == 10000)
assert(hdl_in.getPhysicalMaximum(1) == -10000)
assert(hdl_in.getPhysicalMinimum(0) == -5000)
assert(hdl_in.getPhysicalMinimum(1) == -30000)
assert(hdl_in.getDigitalMaximum(0) == 1000000)
assert(hdl_in.getDigitalMaximum(1) == 3000000)
assert(hdl_in.getDigitalMinimum(0) == -1000000)
assert(hdl_in.getDigitalMinimum(1) == 1000000)
assert(hdl_in.getSampelsPerDataRecord(0) == 20)
assert(hdl_in.getSampelsPerDataRecord(1) == 23)
assert(hdl_in.getPhysicalDimension(0) == "uVxxxxxx")
assert(hdl_in.getPhysicalDimension(1) == " 0xxxxxx")
assert(hdl_in.getPreFilter(0)[0 : 9] == "qwerty   ")
assert(hdl_in.getPreFilter(1)[0 : 9] == "zxcvbn   ")
assert(hdl_in.getTransducer(0)[0 : 9] == "asdfgh   ")
assert(hdl_in.getTransducer(1)[0 : 9] == "poklhyg  ")
assert(len(hdl_in.annotationslist) == 3)
assert(hdl_in.annotationslist[0].onset == 0)
assert(hdl_in.annotationslist[0].duration == -1)
assert(hdl_in.annotationslist[0].description == "Recording starts")
assert(hdl_in.annotationslist[1].onset == 6000000)
assert(hdl_in.annotationslist[1].duration == 2000000)
assert(hdl_in.annotationslist[1].description == "Test 2")
assert(hdl_in.annotationslist[2].onset == 11700000)
assert(hdl_in.annotationslist[2].duration == -1)
assert(hdl_in.annotationslist[2].description == "Recording ends")

assert(hdl_in.fseek(1, 400, hdl_in.EDFSEEK_SET) != 400)
assert(hdl_in.fseek(0, 412, hdl_in.EDFSEEK_SET) != 412)

assert(hdl_in.fseek(0, 20, hdl_in.EDFSEEK_SET) == 20)
assert(hdl_in.readSamples(0, dbuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(dblcmp_lim(dbuf[i], -5000, 0.00001) == 0)
    continue

  if i == 19:
    assert(dblcmp_lim(dbuf[i], 10000, 0.00001) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -5100 + (i * 800), 0.75) == 0)

assert(hdl_in.fseek(1, 23, hdl_in.EDFSEEK_SET) == 23)
assert(hdl_in.readSamples(1, dbuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(dblcmp_lim(dbuf[i], -30000, 0.00001) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -30100 + (i * 909), 0.00001) == 0)

hdl_in.rewind(0)

assert(hdl_in.readSamples(0, dbuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(dblcmp_lim(dbuf[i], -5000, 0.00001) == 0)
    continue

  if i == 19:
    assert(dblcmp_lim(dbuf[i], 10000, 0.00001) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -5100 + (i * 800), 0.75) == 0)

hdl_in.rewind(1)

assert(hdl_in.readSamples(1, dbuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(dblcmp_lim(dbuf[i], -30000, 0.00001) == 0)
    continue

  assert(dblcmp_lim(dbuf[i], -30100 + (i * 909), 0.00001) == 0)

assert(hdl_in.fseek(0, 40, hdl_in.EDFSEEK_SET) == 40)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 105300))

assert(hdl_in.fseek(1, 46, hdl_in.EDFSEEK_SET) == 46)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 20:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 105300))

assert(hdl_in.fseek(0, 80, hdl_in.EDFSEEK_SET) == 80)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 105300))

assert(hdl_in.fseek(1, 92, hdl_in.EDFSEEK_SET) == 92)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 20:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 105300))

assert(hdl_in.fseek(0, 60, hdl_in.EDFSEEK_SET) == 60)

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 105300))

assert(hdl_in.fseek(1, 69, hdl_in.EDFSEEK_SET) == 69)

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 20:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 105300))

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 105300))

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 20:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 105300))

assert(hdl_in.readSamples(0, ibuf, 20) == 20)

for i in range(0, 20):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 105300))

assert(hdl_in.readSamples(1, ibuf, 23) == 23)

for i in range(0, 23):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 20:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 105300))

assert(hdl_in.readSamples(0, ibuf, 80) == 80)

for i in range(0, 80):
  if i == 0:
    assert(ibuf[i] == -1000000)
    continue

  assert(ibuf[i] == -1010000 + (i * 25300))

assert(hdl_in.readSamples(1, ibuf, 92) == 92)

for i in range(0, 92):
  if i == 0:
    assert(ibuf[i] == 1000000)
    continue

  if i >= 80:
    assert(ibuf[i] == 3000000)
    continue

  assert(ibuf[i] == 990000 + (i * 25300))

assert(hdl_in.fseek(0, 185, hdl_in.EDFSEEK_SET) == 185)

assert(hdl_in.readSamples(0, ibuf, 15) == 15)

for i in range(0, 15):
  assert(ibuf[i] == -1010000 + ((i + 65) * 25300))

assert(hdl_in.close() == 0)

#############################################

assert(modify_and_try("test.bdf", 1, bytes("1", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 1, bytes("B", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0, bytes("0", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0, bytes("\xff", encoding="latin_1")) == 7)

###################################

fp = open("test.bdf", "rb")

fp.seek(0x600, io.SEEK_SET)

rbuf = fp.read(60)

fp.close()

for i in range(0, 20):
  if i == 0:
    itmp = int.from_bytes(rbuf[(i * 3) + 0 : (i * 3) + 1], byteorder="little", signed=False)
    itmp |= (int.from_bytes(rbuf[(i * 3) + 1 : (i * 3) + 3], byteorder="little", signed=True) << 8)
    assert(itmp == -1000000)
    continue

  if i >= 19:
    itmp = int.from_bytes(rbuf[(i * 3) + 0 : (i * 3) + 1], byteorder="little", signed=False)
    itmp |= (int.from_bytes(rbuf[(i * 3) + 1 : (i * 3) + 3], byteorder="little", signed=True) << 8)
    assert(itmp == 1000000)
    continue

  itmp = int.from_bytes(rbuf[(i * 3) + 0 : (i * 3) + 1], byteorder="little", signed=False)
  itmp |= (int.from_bytes(rbuf[(i * 3) + 1 : (i * 3) + 3], byteorder="little", signed=True) << 8)
  assert(dblcmp_lim(itmp, ((-5100 + (i * 800)) / 0.0075) - 333333.333333, 1.0001) == 0)

###################################

fp = open("test.bdf", "rb")

fp.seek(0x63c, io.SEEK_SET)

rbuf = fp.read(69)

fp.close()

for i in range(0, 23):
  if i == 0:
    itmp = int.from_bytes(rbuf[(i * 3) + 0 : (i * 3) + 1], byteorder="little", signed=False)
    itmp |= (int.from_bytes(rbuf[(i * 3) + 1 : (i * 3) + 3], byteorder="little", signed=True) << 8)
    assert(itmp == 1000000)
    continue

  itmp = int.from_bytes(rbuf[(i * 3) + 0 : (i * 3) + 1], byteorder="little", signed=False)
  itmp |= (int.from_bytes(rbuf[(i * 3) + 1 : (i * 3) + 3], byteorder="little", signed=True) << 8)
  assert(dblcmp_lim(itmp, ((-30100 + (i * 909)) / 0.01) + 4000000.0, 1.0001) == 0)

###################################

assert(modify_and_try("test.bdf", 0x37f, bytes("7", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x37f, bytes("8", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0x39e, bytes("6", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x39e, bytes("7", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0x318, bytes("1 ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x318, bytes("-1", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0x358, bytes("2000000 ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x358, bytes("1000000 ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x358, bytes("-1000000", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0xec, bytes("+10", encoding="ascii")) == 7)

assert(modify_and_try("test.bdf", 0xec, bytes("-10", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0xec, bytes("-1 ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0xec, bytes("0  ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0xec, bytes(" 10", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0xec, bytes("10 ", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0x358, bytes("-8388609", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x358, bytes("-1000000", encoding="ascii")) == 7)

###################################

assert(modify_and_try("test.bdf", 0x380, bytes("8388608 ", encoding="ascii")) == 3)

assert(modify_and_try("test.bdf", 0x380, bytes("1000000 ", encoding="ascii")) == 7)

################################### EDF writing ###############################

hdl_out = EDFwriter("test2.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 1)

assert(hdl_out.setSampleFrequency(0, 100) == 0)
assert(hdl_out.setPhysicalMaximum(0, 10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -1000) == 0)
assert(hdl_out.setDigitalMaximum(0, 32767) == 0)
assert(hdl_out.setDigitalMinimum(0, -32768) == 0)
assert(hdl_out.setAdditionalPatientInfo("Test") == 0)
assert(hdl_out.setAdditionalRecordingInfo("tEST") == 0)

for i in range(0, 100):
  dbuf[i] = 0

assert(hdl_out.writeSamples(dbuf) == 0)

assert(hdl_out.close() == 0)

################################### EDF reading ###############################

hdl_in = EDFreader("test2.edf")

assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_EDFPLUS)

assert(hdl_in.getNumSignals() == 1)

assert(hdl_in.getPatientAdditional()[0 : 4] == "Test")

assert(hdl_in.getRecordingAdditional()[0 : 4] == "tEST")

assert(hdl_in.close() == 0)

################################### EDF writing ###############################

hdl_out = EDFwriter("test3.edf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 1)

assert(hdl_out.setDataRecordDuration(777770) == 0)
assert(hdl_out.setStartDateTime(2008, 12, 31, 23, 59, 58, 1234) == 0)
assert(hdl_out.setNumberOfAnnotationSignals(3) == 0)
for i in range(0, 60):
  l_tmp = 10000 * (i + 1)
  assert(hdl_out.writeAnnotation(l_tmp, -1, str("test %d sec" %(l_tmp / 10000))) == 0)
  l_tmp += 3333
  assert(hdl_out.writeAnnotation(l_tmp, -1, str("test %d.%04d sec" %(l_tmp / 10000, l_tmp % 10000))) == 0)

assert(hdl_out.setSampleFrequency(0, 100) == 0)
assert(hdl_out.setPhysicalMaximum(0, 10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -1000) == 0)
assert(hdl_out.setDigitalMaximum(0, 32767) == 0)
assert(hdl_out.setDigitalMinimum(0, -32768) == 0)
assert(hdl_out.setPatientName("\xc3lpha") == 0)
assert(hdl_out.setPatientCode("Br\xe0v\xf3") == 0)
assert(hdl_out.setPatientGender(1) == 0)
assert(hdl_out.setPatientBirthDate(2005, 7, 4) == 0)
assert(hdl_out.setAdditionalPatientInfo("Charlie") == 0)
assert(hdl_out.setAdministrationCode("D\xeblta") == 0)
assert(hdl_out.setTechnician("\xcbcho") == 0)
assert(hdl_out.setEquipment("Foxtr\xf6t") == 0)
assert(hdl_out.setAdditionalRecordingInfo("Golf") == 0)

for i in range(0, 100):
  dbuf[i] = 0

for i in range(0, 40):
  assert(hdl_out.writeSamples(dbuf) == 0)

assert(hdl_out.close() == 0)

################################### EDF reading ###############################

hdl_in = EDFreader("test3.edf")

assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_EDFPLUS)

assert(hdl_in.getNumSignals() == 1)

assert(hdl_in.getStartTimeSubSecond() == 1234000)

assert(len(hdl_in.annotationslist) == 120)

for i in range(0, 60):
  assert(hdl_in.annotationslist[i * 2].onset == (10000000 * (i + 1)))
  assert(hdl_in.annotationslist[i * 2].duration == -1)
  assert(hdl_in.annotationslist[i * 2 + 1].onset == ((10000000 * (i + 1)) + 3333000))
  assert(hdl_in.annotationslist[i * 2 + 1].duration == -1)

assert(hdl_in.getPatientName() == "Alpha")
assert(hdl_in.getPatientCode() == "Bravo")
assert(hdl_in.getPatientGender() == "Male")
assert(hdl_in.getPatientBirthDate() == "04 jul 2005")
assert(hdl_in.getPatientAdditional()[0 : 7] == "Charlie")
assert(hdl_in.getAdministrationCode() == "Delta")
assert(hdl_in.getTechnician() == "Echo")
assert(hdl_in.getEquipment() == "Foxtrot"), ("->%s<-" %(hdl_in.getEquipment()))
assert(hdl_in.getRecordingAdditional()[0 : 4] == "Golf")

dt = hdl_in.getStartDateTime()
assert(dt.day == 31)
assert(dt.month == 12)
assert(dt.year == 2008)
assert(dt.second == 58)
assert(dt.minute == 59)
assert(dt.hour == 23)
assert(dt.microsecond == 123400)

assert(hdl_in.close() == 0)

fp = open("test3.edf", "rb")

rbuf = fp.read(256)

fp.close()

assert(rbuf[8 : 88].decode("ascii") == "Bravo M 04-JUL-2005 Alpha Charlie                                               ")

assert(rbuf[88 : 168].decode("ascii") == "Startdate 31-DEC-2008 Delta Echo Foxtrot Golf                                   ")

################################### BDF writing ###############################

hdl_out = EDFwriter("test3.bdf", EDFwriter.EDFLIB_FILETYPE_EDFPLUS, 1)

assert(hdl_out.setDataRecordDuration(110000) == 0)
assert(hdl_out.setStartDateTime(2008, 12, 31, 23, 59, 58, 1234) == 0)
assert(hdl_out.setNumberOfAnnotationSignals(3) == 0)
assert(hdl_out.writeAnnotation(10000, -1, b"\xeb\x8c\x80\xed\x95\x9c\xeb\xaf\xbc\xea\xb5\xad".decode("utf-8")) == 0)
assert(hdl_out.writeAnnotation(20000, -1, b"\xeb\x8c\x80\xed\x95\x9c\xeb\xaf\xbc\xea\xb5\xad\x00".decode("utf-8")) == 0)
assert(hdl_out.writeAnnotation(30000, -1, b"\xeb\x8c\x80\xed\x95\x9c\xeb\xaf\xbc\xea\xb5\xad\x00\x00\x00\x00\x00\x00\x00".decode("utf-8")) == 0)
for i in range(0, 50):
  l_tmp = 10000 * (i + 1)
  assert(hdl_out.writeAnnotation(l_tmp, -1, str("test %d sec" %(l_tmp / 10000))) == 0)
  l_tmp += 3333
  assert(hdl_out.writeAnnotation(l_tmp, -1, str("test %d.%04d sec" %(l_tmp / 10000, l_tmp % 10000))) == 0)

assert(hdl_out.setSampleFrequency(0, 100) == 0)
assert(hdl_out.setPhysicalMaximum(0, 10000) == 0)
assert(hdl_out.setPhysicalMinimum(0, -1000) == 0)
assert(hdl_out.setDigitalMaximum(0, 32767) == 0)
assert(hdl_out.setDigitalMinimum(0, -32768) == 0)

for i in range(0, 100):
  dbuf[i] = 0

for i in range(0, 10):
  assert(hdl_out.writeSamples(dbuf) == 0)

assert(hdl_out.close() == 0)

################################### BDF reading ###############################

hdl_in = EDFreader("test3.bdf")

assert(hdl_in.getFileType() == hdl_in.EDFLIB_FILETYPE_EDFPLUS)

assert(hdl_in.getNumSignals() == 1)

assert(hdl_in.getStartTimeSubSecond() == 1234000)

assert(len(hdl_in.annotationslist) == 30)

assert(hdl_in.close() == 0)


