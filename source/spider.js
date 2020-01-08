//https://www.kuaidaili.com/free/
var ele=$('tr')
var arr=[]
for(var i=0;i<ele.length;i++){
    var data={}
    var address=''
    for(var j=0;j<ele.eq(i).find('td').length;j++){
        if(ele.eq(i).find('td').eq(j).data('title')=='IP'){
           address=ele.eq(i).find('td').eq(j).text()+':'
        }
        if(ele.eq(i).find('td').eq(j).data('title')=='PORT'){
           address+=ele.eq(i).find('td').eq(j).text()
        }
        if(ele.eq(i).find('td').eq(j).data('title')=='类型'){
            
            if(ele.eq(i).find('td').eq(j).text()=='HTTP'){
                data.HTTP=address
            }else if(ele.eq(i).find('td').eq(j).text()=='HTTPS'){
                data.HTTPS=address
            }
        }
    }
    if(data.HTTP || data.HTTPS){
        arr.push(data)
    }
}
console.log(JSON.stringify(arr));

//http://www.66ip.cn/nm.html
var str=document.body.innerText;
var arr=str.split('\n');
var arr_proxy=[];

for(var i=0;i<arr.length;i++){
    var data={}
    if(arr[i]){
        data.HTTP=arr[i]
        arr_proxy.push(data)
    }
}
console.log(JSON.stringify(arr_proxy))

var str=document.body.innerText;
var arr=JSON.parse(str).data
var arr_proxy=[];
for(var i=0;i<arr.length;i++){
    var data={}
    data.HTTP=arr[i].ip+':'+arr[i].port
    arr_proxy.push(data)
}
console.log(JSON.stringify(arr_proxy))
