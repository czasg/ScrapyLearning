import os

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator


current_path = os.path.dirname(os.path.abspath(__file__))

def pdf2doc(input, output):
    try:
        with open(input, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument()
            parser.set_document(doc)
            doc.set_parser(parser)
            # 设置初始化密码
            doc.initialize()
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in doc.get_pages():
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for x in layout:
                        if isinstance(x, LTTextBoxHorizontal):
                            with open(output, 'a', encoding='utf-8') as f1:
                                results = x.get_text()
                                f1.write(results+'\n')
        return True
    except Exception as e:
        print(e)
        return False


def main():
    # rc = doc2pdf(input, output)
    # rc = doc2html(input, output)
    input = '2.pdf'
    output = os.path.join(current_path, 'test.doc')
    rc = pdf2doc(input, output)
    if rc:
        print('转换成功')
    else:
        print('转换失败')

if __name__ == '__main__':
    main()