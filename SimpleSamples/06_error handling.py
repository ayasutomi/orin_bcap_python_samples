# -*- coding:utf-8 -*-

# Sample program
# Robot error handling

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
from pybcapclient.orinexception import ORiNException

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

try:

    # Connection processing of tcp communication
    m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
    print("Open Connection")

    # start b_cap Service
    m_bcapclient.service_start("")
    print("Send SERVICE_START packet")

    # set Parameter
    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = ("localhost")
    Option = ("")

    # Connect to RC8 (RC8(VRC)provider)
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # get Robot Object Handl
    HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
    print("AddRobot")

    '''
    ### TakeArm
    Command = "TakeArm"
    Param = [0,0]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    print("TakeArm")

    # Motor On
    Command = "Motor"
    Param = [1, 0]
    m_bcapclient.robot_execute(HRobot, Command, Param)
    print("Motor On")
    '''

    # Move Initialize Position
    Comp = 1
    Pos_value = [0.0, 0.0, 1000.0, 0.0, 90.0, 0.0]
    Pose = [Pos_value, "J", "@E"]
    m_bcapclient.robot_move(HRobot, Comp, Pose, "")
    print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")

except ORiNException as e:
    print("ORiN Error")
    errorcode_int = int(str(e))
    if errorcode_int < 0:
        errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
    else:
        errorcode_hex = hex(errorcode_int)
    print("Error Code : 0x" + str(errorcode_hex))
    error_description = m_bcapclient.controller_execute(
        hCtrl, "GetErrorDescription", errorcode_int)
    print("Error Description : " + error_description)

except Exception as e:
    print("ERROR")
    print(e)

finally:

    # Release Handle and Disconnect
    if HRobot != 0:
        m_bcapclient.robot_release(HRobot)
        print("Release Robot")
    if hCtrl != 0:
        m_bcapclient.controller_disconnect(hCtrl)
        print("Release Controller")

    # b-cap service stop
    m_bcapclient.service_stop()
    print("b-cap service Stop")

    del m_bcapclient
    print("Finish")
