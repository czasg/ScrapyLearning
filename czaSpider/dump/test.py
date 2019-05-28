from win32com import client as wc

w = wc.Dispatch("Word.Application")
doc = w.Documents.Open()
doc.SaveAs()