from win32com import client as wc
"""
附件转化未完成
"""
w = wc.Dispatch("Word.Application")
doc = w.Documents.Open()
doc.SaveAs()