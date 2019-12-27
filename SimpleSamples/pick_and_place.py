# -*- coding:utf-8 -*-

# pick and place motion sample
# you need teaching picking point(P1), placing point(P2) and Work origin (P0)

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
from pybcapclient.orinexception import ORiNException

# set IP Address , Port number and Timeout of connected RC8
host = "127.0.0.1"
port = 5007
timeout = 2000

try:
    # Connection processing of tcp communication
    m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
    print("Open Connection")

    # start b_cap Service
    m_bcapclient.service_start("")
    print("Send SERVICE_START packet")

    # set parameter
    name = ""
    provider = "CaoProv.DENSO.VRC"
    machine = ("localhost")
    option = ("")

    # Connect to RC8 (RC8(VRC)provider)
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC8")
    # get Robot Object Handl
    hrobot = m_bcapclient.controller_getrobot(hctrl, "Arm", "")
    print("AddRobot")

    # TakeArm
    command = "TakeArm"
    param = [0, 0]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("TakeArm")

    # Motor On
    command = "Motor"
    param = [1, 0]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("Motor On")

    # set Extspeed speed,accel,decel
    command = "Extspeed"
    speed = 100
    accel = 100
    decel = 100
    param = [speed, accel, decel]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("Extspeed")

    # move to Work origin point P0
    comp = 1
    pose = "@P P0"
    m_bcapclient.robot_move(hrobot, comp, pose, "")
    print("complete Move P,@P P[0]")

    # ---- Picking motion ---- #
    command = "Approach"
    comp = 1
    pose = "P1"
    pose_len = "@P 50"
    param = [comp, pose, pose_len]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("[pick] : Approach P,P[1],@P 100")

    comp = 2
    pose = "@E P1"
    m_bcapclient.robot_move(hrobot, comp, pose, "")
    print("[pick] : complete Move L,@E P[1]")

    # hand chuck
    '''
    # cobotta hand
    command = "HandMoveH"
    param = [10, True]
    m_bcapclient.controller_execute(hctrl, command, param)
    '''
    '''
    # Electric hand Taiyo
    h_extention = m_bcapclient.controller_getextension(hctrl, "Hand0", "")
    command = "MoveH"
    param = [50, 30, 1]
    m_bcapclient.extension_execute(h_extention, command, param)
    '''
    '''
    # chuck controlled by IO
    h_io = m_bcapclient.controller_getvariable(hctrl, "IO64", "")
    m_bcapclient.variable_putvalue(h_io, True)
    '''
    print("[pick] : Chuck")

    command = "Depart"
    comp = 2
    pose_len = "@P 50"
    stropt = ""
    param = [comp, pose_len, stropt]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("[pick] : Depart L,@P 50")

    # ---- placing motion ---- #
    command = "Approach"
    comp = 1
    pose = "P2"
    pose_len = "@P 50"
    param = [comp, pose, pose_len]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("[place] : Approach P,P[1],@P 100")

    comp = 2
    pose = "@E P2"
    m_bcapclient.robot_move(hrobot, comp, pose, "")
    print("[place] : complete Move L,@E P[1]")

    # hand chuck
    '''
    # cobotta hand
    command = "HandMoveH"
    param = [10, True]
    m_bcapclient.controller_execute(hctrl, command, param)
    '''
    '''
    # Electric hand Taiyo
    h_extention = m_bcapclient.controller_getextension(hctrl, "Hand0", "")
    command = "MoveH"
    param = [50, 30, 1]
    m_bcapclient.extension_execute(h_extention, command, param)
    '''
    '''
    # chuck controlled by IO
    h_io = m_bcapclient.controller_getvariable(hctrl, "IO64", "")
    m_bcapclient.variable_putvalue(h_io, True)
    '''
    print("[place] : Chuck")

    command = "Depart"
    comp = 2
    pose_len = "@P 50"
    stropt = ""
    param = [comp, pose_len, stropt]
    m_bcapclient.robot_execute(hrobot, command, param)
    print("[place] : Depart L,@P 50")

    # move to work origin position
    comp = 1
    pose = "@P P0"
    m_bcapclient.robot_move(hrobot, comp, pose, "")
    print("complete Move P,@P P[0]")

except ORiNException as e:
    print("ORiN Error")
    errorcode_int = int(str(e))
    if errorcode_int < 0:
        errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
    else:
        errorcode_hex = hex(errorcode_int)
    print("Error Code : 0x" + str(errorcode_hex))
    error_description = m_bcapclient.controller_execute(
        hctrl, "GetErrorDescription", errorcode_int)
    print("Error Description : " + error_description)

except Exception as e:
    print("ERROR")
    print(e)

finally:
    # Disconnect
    if(hrobot != 0):
        # Motor Off
        command = "Motor"
        param = [0, 0]
        m_bcapclient.robot_execute(hrobot, command, param)
        print("Motor Off")

        # Give Arm
        command = "GiveArm"
        param = None
        m_bcapclient.robot_execute(hrobot, command, param)
        print("GiveArm")
        # release robot handle
        m_bcapclient.robot_release(hrobot)
        print("Release Robot Object")
    # End If
    if(hctrl != 0):
        m_bcapclient.controller_disconnect(hctrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
