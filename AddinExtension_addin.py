# -*- coding: utf-8 -*-
import arcpy
import pythonaddins

class KofraExtension(object):
    """Implementation for AddinExtension_addin.extension2 (Extension)"""
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True
    def onChangeFeature(self):
        mxd = arcpy.mapping.MapDocument(r"CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            mxd.activeView = df.name
            mxd.title = df.name
            lyr = arcpy.mapping.ListLayers(mxd, "Kofra", df)[0]
            sdePath = lyr.dataSource.split(".sde")[0]
            database = sdePath + ".sde"
            fc = lyr.dataSourcefc = lyr.dataSource
            layer_names = [u'Kofra']
            workspace = database
            wgs = arcpy.SpatialReference(4326)
            edit = arcpy.da.Editor(workspace)
            layerName = layer_names[0]
            def selectObje(layer_names):
                try:
                    selectedOIDsAG = arcpy.Describe(layerName).FIDSet.split("; ")
                    if len(selectedOIDsAG) < 2:
                        for i in selectedOIDsAG:
                            sql = "OBJECTID = %i" % int(i)
                            with arcpy.da.SearchCursor(fc, ['SHAPE@', 'OBJECTID'], sql) as cursor:
                                for row in cursor:
                                    cursor2 = arcpy.da.UpdateCursor(fc, ['SHAPE@', 'OBJECTID', 'ENLEM', 'BOYLAM'], sql)
                                    for row2 in cursor2:
                                        pnt_wgs = row2[0].projectAs(wgs)
                                        row2[2:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X]
                                        row2[2:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X]
                                        cursor2.updateRow(row2)
                                    del cursor2
                except:
                    print "Kofra Enlem Boylam yazdirma isleminde hata!"
            for i in layer_names:
                selectObje(i)

    def onStartOperation(self):
        pass

    def onCreateFeature(self):
        pass

    def beforeStopOperation(self):
        pass

    def onStopOperation(self):
        pass

    def onEditorSelectionChanged(self):
        mxd = arcpy.mapping.MapDocument(r"CURRENT")
        for df in arcpy.mapping.ListDataFrames(mxd):
            mxd.activeView = df.name
            mxd.title = df.name
            lyr = arcpy.mapping.ListLayers(mxd, "Kofra", df)[0]
            sdePath = lyr.dataSource.split(".sde")[0]
            database = sdePath + ".sde"
            fc = lyr.dataSourcefc = lyr.dataSource
            layer_names = [u'Kofra']
            workspace = database
            wgs = arcpy.SpatialReference(4326)
            edit = arcpy.da.Editor(workspace)

            # edit.startEditing(False, True)
            # edit.startOperation()
            def selectObje(layerName):
                try:
                    selectedOIDsAG = arcpy.Describe(layerName).FIDSet.split("; ")
                    if len(selectedOIDsAG) < 2:
                        for i in selectedOIDsAG:
                            sql = "OBJECTID = %i" % int(i)
                            with arcpy.da.SearchCursor(fc, ['SHAPE@', 'OBJECTID'], sql) as cursor:
                                for row in cursor:
                                    cursor2 = arcpy.da.UpdateCursor(fc, ['SHAPE@', 'OBJECTID', 'ENLEM', 'BOYLAM'], sql)
                                    for row2 in cursor2:
                                        pnt_wgs = row2[0].projectAs(wgs)
                                        row2[2:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X]
                                        row2[2:] = [pnt_wgs.centroid.Y, pnt_wgs.centroid.X]
                                        cursor2.updateRow(row2)
                                    del cursor2
                except:
                    print "Kofra Enlem Boylam yazdirma isleminde hata!"

            for i in layer_names:
                selectObje(i)
            # edit.stopOperation()
            # edit.stopEditing(True)

    def onSaveEdits(self):
        mxd = arcpy.mapping.MapDocument(r"CURRENT")
        arcpy.env.overwriteOutput = True
        for df in arcpy.mapping.ListDataFrames(mxd):
            mxd.activeView = df.name
            mxd.title = df.name
            lyr1 = arcpy.mapping.ListLayers(mxd, "İstasyon", df)[0]
            in_layer = "Kabin-TRP"
            for layer in lyr1:
                if layer.name == "Kabin-TRP":
                    layer_names1 = [u'Kabin-TRP']
                    fc1 = layer.dataSourcefc = layer.dataSource
                    sdePath = layer.dataSource.split(".sde")[0]
                    database = sdePath + ".sde"
                    workspace = database
                    field_names1 = [f.name for f in arcpy.ListFields(fc1)]
                    arcpy.SetSeverityLevel(1)
                    edit = arcpy.da.Editor(workspace)
                    def queryObje(layer_names1):
                        try:
                            with arcpy.da.SearchCursor(layer_names1, ["OID@","STATION_NAME"]) as rows:
                                for row in rows:
                                    if row[1] is None:
                                        pythonaddins.MessageBox("{} OBJECTID' LI STATION_NAME kolonu bos!".format(row[0]), 'İstasyon Katmani', 0)
                        except:
                            arcpy.AddMessage("İstasyon STATION_NAME kolonu bos gecilemez isleminde hata!")
                    for i in layer_names1:
                        queryObje(i)
                else:
                    break
            query = "STATION_NAME IS NULL"
            arcpy.SelectLayerByAttribute_management(in_layer, "NEW_SELECTION", query)