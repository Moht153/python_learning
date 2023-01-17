/*
 * @Author: Moht153 1142930377@qq.com
 * @Date: 2023-01-09 13:56:58
 * @LastEditors: Moht153 1142930377@qq.com
 * @LastEditTime: 2023-01-09 16:37:41
 * @FilePath: /web/project_manager/product_manager.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */

// 从本地存储中提取token 和 username(用于加密识别)
token = window.localStorage.getItem('manager_token');
username = window.localStorage.getItem('manager_user');

// 获取当前路径
var url = document.location.toString();


////////////////////// 这一部分用于编写路径url///////////////////
var query_split = url.split('?');
var query_set = '';
if(query_split.length > 1){
    query_set = query_split[1];
}
var arrUrl = url.split("//");
//当前访问的用户
// 'http://192.168.0.114:5000/<username>/sheeps'
var blog_username = arrUrl[1].split('/')[1];

if(query_set){
    var get_url = "http://192.168.0.114:8000/v1/sheeps/"+ blog_username + "/all?" + query_set;
}else{
    var get_url = "http://192.168.0.114:8000/v1/sheeps/"+ blog_username + "/all";

}
/////////////////路径内容到此结束///////////////////




$('button#cashier').click(function(){
    window.location =  '/' + blog_username + '/cashier';
})

countStart = 1;
countEnd  = 30;
counting = 0;
var isTrue = true;
///////////////////核心模块////////////////////

$(function(){

    function ajaxGet(){
        $.ajax({
            // 请求方式
            type:"get",
            // url
            url: 'http://192.168.0.114:8000/v1/sheeps/Moht153/all',
            // url: get_url,
            // number 用来向后端告之提取数量
            data:{
                start: countStart,
                end: countEnd,
            },

            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success:function (result) {

                if (200 == result.code){

                        var sheeps_list = result.data.sheeps
                        console.log(sheeps_list)
                        for(var i=0;i< sheeps_list.length; i++){
                            var _HTML = '';
                            _HTML = '<div class="sheep_id">' + sheeps_list[i].id + '</div>'
                            _HTML += '<div class="sheep_weight">' + sheeps_list[i].weight + '</div>'
                            _HTML += '<div class="dealTo"><a href="/' +
                            blog_username + '/order?cust_name=' + sheeps_list[i].deal_to + '">'
                            _HTML += sheeps_list[i].deal_to + '</a></div>'
                            _HTML += '<div class="price">' + sheeps_list[i].single_price + '</div>'
                            _HTML += '<div class="total_price">' + sheeps_list[i].total_price + '</div>'
                            _HTML += '<div class="deal_time">' + sheeps_list[i].deal_time + '</div><br>'
                            $('#tbody').append(_HTML)



                        }
                        countStart = parseInt(result.data.end);
                        countEnd = countStart + 30;
                        console.log('start end number is:', countStart,countEnd);



                } else if(205 == result.code){
                    if(counting==0){
                        alert(result.error);
                        counting ++;
                    }

                }else{
                    alert(result.error)
                }
            }
        });

    }

    // 预先加载部分数据（预设前30条）
    ajaxGet()

    /////以下内容是滚动条触底加载模块
    function listenScroll(){
        window.onscroll=function(){
            var scrollTop = document.documentElement.scrollTop;
            var clientHeight = document.documentElement.clientHeight;
            var bodyHeight = document.body.clientHeight;
            // console.log(scrollTop, clientHeight, bodyHeight);

            if(parseInt(bodyHeight-scrollTop)<=clientHeight+5){
                if(isTrue==true){
                    console.log("触底了！");
                    isTrue=false;
                    setTimeout(function(){
                        isTrue=true;
                    },200)
                    ajaxGet();
                }
            }
        }
    }

    listenScroll()

});


// 登出模块
$('#log_out').on('click', function(){

    if(confirm("确定登出吗？")){
        window.localStorage.removeItem('manager_token');
        window.localStorage.removeItem('manager_user');
        window.location.href= '/';
    }
}
)