// 废弃翻页逻辑
$(function() {
    var nav_pager_footer = new Vue({
        el: '#nav-pager-footer',
        methods: {
            nextPage: function () {
                page = {{ page_index }}
                page = page + 1;
                gotoPage(page);
            },
            prePage: function () {
                page = {{ page_index }}
                page = page - 1;
                gotoPage(page);
            }
        }
    })
})

//废弃逻辑
<script>
    function Drop_initManageUser(data) {
        $('#manageUsers').show();
        var manageUsers = new Vue({
            el: '#manageUsers',
            data: {
                users: data.users,
                page: data.page
            },
            methods: {
                test: function() {
                    var that = this;
                    var
                        page_index = $('#footer_page_index'),
                        nextPage = parseInt(page_index.text().trim()) + 1,
                        res = '';
                    page_index.text(nextPage);
                    $.get('/api/get/users', {
                        page: nextPage
                    }, function (results, status) {
                        if (status==='success'){
                            $('#loading').hide();
                            //res = results;
                            console.log(results)
                            that.users = results.users
                            that.page = results.page
                            that.$nextTick()
                        }
                    })
                }
            }
        });
    }
</script>