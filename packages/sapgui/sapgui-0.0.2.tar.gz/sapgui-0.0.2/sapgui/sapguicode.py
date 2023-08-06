from sapgui import sapgui


def zmpua25(session, *args):
    """
    Function to run zmpua25 code.
    :param session: parameter obtained from sapgui.
    :param args: variant:str, material_id: DataFrame
    :return: none.
    """
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/tbar[0]/okcd").text = "ZMPUA25"
    session.findById("wnd[0]").sendVKey(0)
    session.findById("wnd[0]/tbar[1]/btn[17]").press()
    session.findById("wnd[1]/usr/txtV-LOW").text = args[0]
    session.findById("wnd[1]/usr/txtENAME-LOW").text = ""
    session.findById("wnd[1]/usr/txtV-LOW").caretPosition = 6
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    args[1].to_clipboard(index=False, header=None)
    session.findById(r"wnd[0]/usr/btn%_R_MATNR_%_APP_%-VALU_PUSH").press()
    session.findById("wnd[1]/tbar[0]/btn[16]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]").sendVKey(8)
    session.findById("wnd[0]/tbar[1]/btn[45]").press()
    session.findById(r"wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    sapgui.sap_download_tmp_file_del()
    session.findById("wnd[1]/usr/ctxtDY_PATH").text = sapgui.SAP_TMP_PATH
    session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = sapgui.SAP_TMP_FILE
    session.findById("wnd[1]/usr/ctxtDY_FILE_ENCODING").text = "0000"
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]").sendVKey(3)
    session.findById("wnd[0]").sendVKey(3)
