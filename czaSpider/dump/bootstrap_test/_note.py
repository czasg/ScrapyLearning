__goal__ = "js"
"""
通过内置的data-API可以使用所有的js插件
【模态框】
能够动态谈下来的那种框框，使用的class="modal fade" role="dialog" data-dismiss="modal" aria-label="Close"
首先是一个大类<div class="modal-dialog" role="document">用来包括所有的内容
然后用一个<div class="modal-content">来包括所有的内容
里面的细节就是class="modal-header" / "modal-body" / "modal-footer"

这个务必添加role和aria-labelledby属性，且需要在标题中的按钮中添加aria-hidden="true"属性
这里的fade是用来控制淡入淡出的，很好看啊
class="modal fade" role="dialog"
    class="modal-dialog" role="document"
        class="modal-content"
            class="modal-header"
            class="modal-nody"
            class="modal-footer"
如果要添加栅格栏，或者表单，我们可以在body里面进行定义












"""