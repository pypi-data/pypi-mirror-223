# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 06:41:06 2023

@author: Hedi
"""

import wx
import wx.grid as grid



class MyFrame(wx.Frame):
    def __init__(self,app, parent, title):
        super(MyFrame, self).__init__(parent, title =title, size = (800,600))
        self.panel = MyPanel(app, self)


class MyPanel(wx.Panel):
    def __init__(self,app, parent):
        super(MyPanel, self).__init__(parent)

        mygrid = grid.Grid(self)
        mygrid.CreateGrid( len(app.inventories), 3)
        
        mygrid.SetColLabelValue(0, "Inventory")
        mygrid.SetColLabelValue(1, "Amount")
        mygrid.SetColLabelValue(2, "Unit")
        for i, inv in enumerate(app.inventories.values()):
            mygrid.SetCellValue(i, 0, inv.name)
            mygrid.SetCellValue(i, 1, str(inv.amount))
            mygrid.SetCellValue(i, 2, inv.unit)
            mygrid.SetRowLabelValue(i, str(i))
        mygrid.AutoSizeColumns()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)




class InvApp(wx.App):
    def __init__(self, inventories):
        self.inventories = inventories
        wx.App.__init__(self)
        
    def OnInit(self):
        self.frame = MyFrame(self,parent=None, title="Life Cycle Inventories")
        self.frame.Show()
        return True

def InLoadInv(lca):
    app = wx.App()
    with wx.FileDialog(None, "Open JSON file", wildcard="XYZ files (*.json)|*.json",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            pass
        else:
            import os
            import inspect
            import json
            script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            for pathname in fileDialog.GetPaths():
                #shutil.copyfileobj(open(pathname, 'rb'), open(script_directory+"\\lci\\"+os.path.basename(pathname), 'wb'))
                inv = json.load(open(pathname))
                PRODUCT_FLOW =list(filter(lambda e: not e["input"] and e["flow"]["flowType"]=="PRODUCT_FLOW",inv["exchanges"]))
                lci={}
                if len(PRODUCT_FLOW)>0:
                    lci["name"]=inv["name"]
                    lci['id']=inv["@id"]
                    lci["amount"] = PRODUCT_FLOW[0]["amount"]
                    lci["unit"] = PRODUCT_FLOW[0]["unit"]["name"]
                    lci["exchanges"]={}
                    for e in filter(lambda e: not e["input"] and e["flow"]["flowType"]=="ELEMENTARY_FLOW",inv["exchanges"]):
                        lci["exchanges"][e["flow"]["@id"]] = {
                            "name":e["flow"]["name"],
                            "unit":e["unit"]["name"],
                            "amount":e["amount"]}
                    with open(script_directory+"\\lci\\"+os.path.basename(pathname), "w") as outfile:
                        outfile.write(json.dumps(lci))
            lca.inventories.load()
                    