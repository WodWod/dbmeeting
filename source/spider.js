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
    if(data.address){
        arr.push(data)
    }
}
console.log(JSON.stringify(arr));