window.onload = function() {
   
   //window.cartitemjson=JSON.parse(window.data);
   populateBody();
}

function populateBody(){
   //document.getElementById("cartbody").innerHTML+= window.data;
   //var datajson=JSON.parse(window.data);
   //document.getElementById("cartbody").innerHTML+= window.data;
   //document.getElementById("cartbody").innerHTML+= window.data;
   //document.getElementById("cartbody").innerHTML+="1324";
   //var bucketlist=datajson["cart"];

   var datajson=JSON.parse(window.data);
   window.identity=datajson["identity"];
   window.restaurant=datajson["restaurant"];
   window.tableno=datajson["tableno"];
   datajson=datajson["tableinfo"];
   
   datajson=datajson["cart"];
   var bucketlist=Object.keys(datajson);
   
   for(var bucketitem=0;bucketitem < bucketlist.length;bucketitem++)
   {   
     var individualid=bucketlist[bucketitem];
     var singlepersonorderlistjson=datajson[individualid];
     singlepersonorderlistjson=singlepersonorderlistjson["mycart"];
     var firstnamejson=datajson[individualid]["firstname"];
     var firstname=document.createElement('div');
     firstname.className="firstname";
     firstname.innerHTML=JSON.stringify(firstnamejson);
     var bucket=document.createElement('div');
     bucket.className="bucket";
     for(var orderindex=0;orderindex<singlepersonorderlistjson.length;orderindex++)
     {
      //document.getElementById("cartbody").innerHTML+=JSON.stringify(singlepersonorderlistjson[orderindex])+"<br/>";
      var atomicorderjson=singlepersonorderlistjson[orderindex];
      
      window.statusjson=atomicorderjson["status"];;
      var itemjson=atomicorderjson["item"];
      var customizationjson=atomicorderjson["customization"];
      var pricejson=atomicorderjson["price"];
      var quantityjson=atomicorderjson["quantity"];

      var atomicorder=document.createElement('div');
      var status=document.createElement('div');
      var item=document.createElement('div');
      var customization=document.createElement('div');
      var price=document.createElement('div');
      var quantity=document.createElement('div');

      atomicorder.className="atomicorder";
      status.className="status";
      firstname.className="firstname";
      item.className="item";
      customization.className="customization";
      price.classname="price";
      quantity.className="quantity";

      status.innerHTML=statusjson;
      firstname.innerHTML=firstnamejson;
      item.innerHTML=itemjson;
      customization.innerHTML=JSON.stringify(customizationjson);
      price.innerHTML=pricejson;
      quantity.innerHTML=quantityjson;
      atomicorder.appendChild(status);
      atomicorder.appendChild(item);atomicorder.appendChild(price);atomicorder.appendChild(quantity);atomicorder.appendChild(customization);
      bucket.appendChild(atomicorder); 
     
   }
   bucket.onclick=alert(individualid);
   if(window.identity==="waiter"){
      bucket.onclick=function(id){
      alert(id);   
      //executeWaitersCode(id);
   }}(individualid);
   document.getElementById("cartbody").appendChild(firstname);
   document.getElementById("cartbody").appendChild(bucket);
   }
}
function executeWaitersCode(id){
    var acceptOrder=document.createElement('div');
    var acceptOrderContent=document.createElement('div');

    acceptOrder.className="acceptOrder";
    acceptOrder.id="acceptOrder";
    acceptOrderContent.className="acceptOrderContent";


    var accept=document.createElement('div');
    
    accept.onclick=function(argid){
       postAcceptOrder(argid);
    }(id)
     
   

    acceptOrderContent.innerHTML="Are you sure you want to accept the order?";
    acceptOrderContent.appendChild(accept);
    acceptOrder.appendChild(acceptOrderContent);
    document.getElementById("cartbody").appendChild(acceptOrder);

} 
function postAcceptOrder(id){
    var http = new XMLHttpRequest();
    var url = 'https://studmenu.herokuapp.com/acceptdeny/'+JSON.stringify({"tableno":window.tableno,"restaurant":restaurant,"id":id});
    http.open("POST", url, false); 
    http.setRequestHeader("Content-Type", "application/json");
    http.send(window.cart);
    document.getElementById('acceptOrder').remove();
}
