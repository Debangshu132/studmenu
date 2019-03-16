window.cart=[];

window.swiper = new Swiper('.swiper-container', {
  slidesPerView:5,
  simulateTouch:true,
  initialSlide:0,
  lazy: {loadPrevNext: true,loadPrevNextAmount: 2,},
  spaceBetween: 30,

  breakpoints: {
      1300: {
          slidesPerView: 11,
          spaceBetween: 40,
        },
      900: {
          slidesPerView: 9,
          spaceBetween: 40,
        },
      710: {
        slidesPerView: 8,
        spaceBetween: 40,
      },
      560: {
        slidesPerView: 7,
        spaceBetween: 15,
      },
      450: {
        slidesPerView: 6,
        spaceBetween: 10,
      },
      370: {
        slidesPerView: 5,
        spaceBetween: 10,
      }
    }

});

food=['Attributes','Bread Drive','Bytes','Floppy','Hardware','Programmer','Software'];
drink=['beer','water','whiskey','water'];
generalIcons={
"veg":"https://s3.ap-south-1.amazonaws.com/studmenu/General+Icons/Veg.png",
"nonveg":"https://s3.ap-south-1.amazonaws.com/studmenu/General+Icons/Non+Veg.png"

}

picCategoryArrayFood=[
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Attributes.png",  
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Bread+Drive.png",
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Bytes.png",  
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Floppy.png",
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Hardware.png",  
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Programmer.png",
"https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Uncolored/Software.png"
]
picCategoryArrayFoodColored=[
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Attributes.png",  
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Bread+Drive.png",
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Bytes.png",  
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Floppy.png",
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Hardware.png",  
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Programmer.png",
  "https://s3.ap-south-1.amazonaws.com/studmenu/Restaurants/CAD+Tech+Bar/Food/Category+1+icons/Colored/Software.png"
  ]

picCategoryArrayDrink=[
  "https://img.icons8.com/color/48/000000/beer-glass.png",
  "https://img.icons8.com/cotton/64/000000/water-glass.png",
  "https://img.icons8.com/dusk/64/000000/wine-glass.png",
  "https://img.icons8.com/cotton/64/000000/water-glass.png"
]
window.menuPicArray=[
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')",
  "url('https://s3.ap-south-1.amazonaws.com/studmenu/Test/Pics/DUO+OF+FLOREST+TIKKA+(1)-min.jpg')"
 
 

  ] 
  function deletecartquantityzeroitems(){
    for(var i=window.cart.length-1;i>-1;i--){
      if(window.cart[i]["quantity"]===0){
        window.cart.splice(i,1);
        console.log(i);
      }
    }
  }

document.getElementById("carticon").onclick=function(menuPicArray){
 deletecartquantityzeroitems(); 
 var cart=document.createElement('div');
 cart.className="cart";
 cart.id="cart";
 //cart.innerHTML=JSON.stringify(window.cart);
 var cartheader=document.createElement('div');
 var cartorderbutton=document.createElement('div');
 var cartheaderback=document.createElement('IMG'); 
 var cartheadername=document.createElement('div');
 cartheader.className="cartheader";
 cartheaderback.className="cartheaderback";
 cartheadername.className="cartheadername";
 cartorderbutton.className="cartorderbutton";
 cartheaderback.setAttribute("src","https://img.icons8.com/windows/32/000000/left.png");
 cartheadername.innerHTML="cart"
 cartheader.appendChild(cartheaderback);
 cartheader.appendChild(cartheadername);
 cartheaderback.onclick=function(){
  document.getElementById("cart").remove();
 }
 //cartheader.innerHTML="cart";
 //document.getElementById("customizationtab").remove();
 cart.appendChild(cartheader);
 for(var i=0;i<window.cart.length;i++){
  var cartitem=document.createElement('div');
  var cartitemname=document.createElement('div');
  var cartcustomizationname=document.createElement('div');
  var cartitempricename=document.createElement('div');
  var cartitemquantityname=document.createElement('div');
  var minusbutton=document.createElement('img');
  var plusbutton=document.createElement('img');
  var changecartitem=document.createElement('div');
  var cartitempic=document.createElement('IMG');

  
  cartitemname.className="cartitemname";
  cartcustomizationname.className="cartcustomizationname";
  cartitempricename.className="cartitempricename";
  cartitemquantityname.className="cartitemquantityname";
  cartitem.className="cartitem";
  changecartitem.className="changecartitem";
  minusbutton.className="cartminusbutton";
  plusbutton.className="cartplusbutton";
  cartitempic.className="cartitempic";

  plusbutton.src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJ22akRsJMV7hsI-OPSvJj7BHWM-qaLCO6Ea0U3gY0esVB2al8Gg";
  minusbutton.src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAGFBMVEX///8AAADz8/NfX1+UlJT4+Pitra1XV1cQNkZNAAAAeElEQVR4nO3Y2QkAIRBEQXU98s/YGBYGZpCqDN5nd2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAApFujlhVeuM9XydnhhbPXMhUqVJhOoUKF+RQqVJhPoUKF+eIL39/47/80AAAAAAAAAAAAAAAAAAAAAAAAAAAAAPx2ARGUD9oUhrtMAAAAAElFTkSuQmCC";
  cartitempic.src='../static/'+[Math.floor(1+Math.random() * 10)]+'.jpg' ;




  var cartitemnamestring=JSON.stringify(window.cart[i]["item"]).substring(1,JSON.stringify(window.cart[i]["item"]).length-1);
  var cartcustomizationnamestring=JSON.stringify(window.cart[i]["customization"]).replace('{"','');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('":["',' : ');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('"],"',' ; ');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('":["',' : ');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('"],"',' ; ');
  cartcustomizationnamestring=cartcustomizationnamestring.replace(']}','');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('[','');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('":[','');
  cartcustomizationnamestring=cartcustomizationnamestring.replace('":],"',' ; ');
  cartcustomizationnamestring=cartcustomizationnamestring.replace(',',' ,Rs');
  cartitemname.innerHTML=cartitemnamestring;
  cartcustomizationname.innerHTML=cartcustomizationnamestring;
  cartitempricename.innerHTML="Price:Rs"+JSON.stringify(window.cart[i]["price"]);
  cartitemquantityname.innerHTML=JSON.stringify(window.cart[i]["quantity"]);
  cartorderbutton.innerHTML="ORDER2";
  cartorderbutton.onclick=function(){
    
    //http.setRequestHeader("Content-Type", "application/json");
    //MessengerExtensions.requestCloseBrowser();
    
    var messageToShare = {"attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements": [{
          "title":"I took Peter's 'Which Hat Are You?' Quiz",
          "image_url": "https://img.icons8.com/color/48/000000/beer-glass.png",
          "subtitle": "My result: Fez",
          "default_action":{
            "type":"web_url",
            "url": "https://www.google.com"
          },
          "buttons":[{
            "type":"web_url",
            "url":"https://www.google.com",
            "title":"Take the Quiz"
          }]
        }]
      }
    }};
    var http = new XMLHttpRequest();
    var url = 'http://studmenu.herokuapp.com/cart/'+JSON.stringify(window.cart);
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json");
    http.send();
    //window.open('http://studmenu.herokuapp.com/cart');
    MessengerExtensions.requestCloseBrowser((function success() {
       //webview closed
      var http = new XMLHttpRequest();
      var url = 'http://studmenu.herokuapp.com/cart/'+JSON.stringify(window.cart);
      http.open("POST", url, true);
      http.setRequestHeader("Content-Type", "application/json");
      http.send();
    }, function error(err) {
      // an error occurred
    }));
  
   /* MessengerExtensions.beginShareFlow(function success(response) {
      if(response.is_sent === true){ 
        // User shared. We're done here!
        
      	MessengerExtensions.requestCloseBrowser((function success() {
          // webview closed
        }, function error(err) {
          // an error occurred
        }));
      }
      else{
      	// User canceled their share! 
      
      }
    }, 
    function error(errorCode, errorMessage) {      
  	// An error occurred trying to share!
    },
    messageToShare,
    "current_thread");  */ 
    //var params = {'cartdata':window.cart};  
    //console.log("ordered");
    //http.open("POST", url, true); 
    //window.location.replace("https://www.messenger.com/closeWindow/?image_url='https://img.icons8.com/color/48/000000/beer-glass.png'&display_text="+JSON.stringify(window.cart));
   
    //http.setRequestHeader("Content-Type", "application/json");
    
    //http.send(params);

  }
  plusbutton.onclick=function(arg,arg2,arg3){
    return function(){
     var priceperitem=  parseInt(window.cart[arg]["price"])/ window.cart[arg]["quantity"];
    window.cart[arg]["quantity"]=window.cart[arg]["quantity"]+1; 
    window.cart[arg]["price"]=window.cart[arg]["price"]+priceperitem;   
    arg2.innerHTML=JSON.stringify(window.cart[arg]["quantity"]);
    arg3.innerHTML="Price:Rs"+JSON.stringify(window.cart[arg]["price"]);
  }

  }(i,cartitemquantityname,cartitempricename);
  minusbutton.onclick=function(arg,arg2,arg3,arg4){
    return function(){
    console.log(window.cart);
    //console.log(arg);
    if(window.cart[arg]["quantity"]>0){
      var priceperitem=  parseInt(window.cart[arg]["price"])/ window.cart[arg]["quantity"];   
    window.cart[arg]["quantity"]=window.cart[arg]["quantity"]-1;
    window.cart[arg]["price"]=window.cart[arg]["price"]-priceperitem;   
    arg2.innerHTML=JSON.stringify(window.cart[arg]["quantity"]);
    arg3.innerHTML="Price:Rs"+JSON.stringify(window.cart[arg]["price"]);
  } 
    if(window.cart[arg]["quantity"]===0){
     
      arg4.remove();
      //window.cart.splice(arg,1);
      // 
    
    }}
}(i,cartitemquantityname,cartitempricename,cartitem);



  changecartitem.appendChild(plusbutton);
  changecartitem.appendChild(cartitemquantityname);
  changecartitem.appendChild(minusbutton);
  cartitem.appendChild(cartitemname);
  cartitem.appendChild(cartcustomizationname);
  cartitem.appendChild(cartitempricename);
  cartitem.appendChild(changecartitem);
  cartitem.appendChild(cartitempic);
  cart.appendChild(cartitem);
 
 }


 cart.appendChild( cartorderbutton);
 document.getElementById("menuitbody").appendChild(cart);
}



document.getElementById("food").onclick=function()
{
  //document.getElementById("menuit").style.background="#1a8cff";
  clearFooter("menuite");
  populateFooter("Taj",food,"Foods",picCategoryArrayFood);
} 



document.getElementById("drink").onclick=function()
{//document.getElementById("menuit").style.background="#46cc3d";
clearFooter("menuite");

populateFooter("Taj",drink,"Drinks",picCategoryArrayDrink);
}  




window.onload = function() {
  populateFooter("Taj",food,"Foods",picCategoryArrayFood,picCategoryArrayFoodColored);
  window.menuitemjson=JSON.parse(menuitem);
  clearFooter("menuitbody");
  populateBody("restaurantName",menuitemjson["Foods"]["Bytes"],menuPicArray);
  };
 

  


function clearFooter(elementID)
{document.getElementById(elementID).innerHTML = "";


}
function populateFooter(restaurantName,foodOrDrink,foodDrink,arraypic,arraypiccolored){
  
  for(i=0;i<foodOrDrink.length;i++){
  var div = document.createElement("div");
 
  div.className="swiper-slide";
  var img = document.createElement("img");
  img.src = arraypic[i];
  img.className="menuitemspic"
  var divChild = document.createElement("div");
  divChild.className="menuitemsdescription";
  divChild.innerHTML+=foodOrDrink[i];
  var menuitemjson=JSON.parse(menuitem);
  var item=menuitemjson[foodDrink][foodOrDrink[i]];
  if(item==='undefined'){
  item="Its not available";}
  img.onclick= function(arg,arg2,arg3,index) {
      return function() {
          
          clearFooter("menuitbody");
          clearAllBorders();
          arg2.src=arg3[index];
          populateBody("restaurantName",arg,menuPicArray);
         
          
         
         
          
      }
  }(item,img,arraypiccolored,i);
  div.appendChild(img);
  div.appendChild(divChild);
  var currentDiv = document.getElementById("div1"); 
  document.getElementById("menuite").insertBefore(div,currentDiv);}
  window.swiper.updateSize(); 
  window.swiper.updateSlides();
 
}


function populateBody(restaurantName,jsonofitems,menuPicArray){
  
var itemnamearray=Object.keys(jsonofitems); 
for(i=0;i<itemnamearray.length;i++){
var div = document.createElement("div");
div.className="slidebody";

var divChild = document.createElement("div");
divChild.className="menuitemsdescriptionbody";
var tempname=JSON.stringify(itemnamearray[i]);
tempname = tempname.substring(1, tempname.length-1);
divChild.innerHTML += tempname; 
divChild.style.fontFamily = "Times New Roman, Times, serif";

var divChildPic = document.createElement("div");
var divChildPicVegNonveg=document.createElement("IMG");
var divChildPlusMinus = document.createElement("div");  
var divChildDescriptionOfFood = document.createElement("div");
divChildDescriptionOfFood.className="bodyfoodprice";

  
divChildPic.className="menuitemsbodypic";
divChildPicVegNonveg.className="divChildPicVegNonveg";
divChildPlusMinus.className="menuitemsbodyplusminus";




divChildPicVegNonveg.src=generalIcons[jsonofitems[tempname]["vegnonveg"]];


divChildPlusMinus.addEventListener('click', function(pEvent) {
  pEvent.stopPropagation();
})

var menuitemsbodyplus=document.createElement("IMG");
menuitemsbodyplus.className="menuitemsbodyplus";
menuitemsbodyplus.setAttribute("src","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJ22akRsJMV7hsI-OPSvJj7BHWM-qaLCO6Ea0U3gY0esVB2al8Gg")
var menuitemsbodyminus=document.createElement("IMG");
menuitemsbodyminus.className="menuitemsbodyminus";
menuitemsbodyminus.setAttribute("src","data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAGFBMVEX///8AAADz8/NfX1+UlJT4+Pitra1XV1cQNkZNAAAAeElEQVR4nO3Y2QkAIRBEQXU98s/YGBYGZpCqDN5nd2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAApFujlhVeuM9XydnhhbPXMhUqVJhOoUKF+RQqVJhPoUKF+eIL39/47/80AAAAAAAAAAAAAAAAAAAAAAAAAAAAAPx2ARGUD9oUhrtMAAAAAElFTkSuQmCC")



//divChildPlusMinus.innerHTML  = '<img class="menuitemsbodyplus" " src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJ22akRsJMV7hsI-OPSvJj7BHWM-qaLCO6Ea0U3gY0esVB2al8Gg"><br /><img class="menuitemsbodyminus" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAGFBMVEX///8AAADz8/NfX1+UlJT4+Pitra1XV1cQNkZNAAAAeElEQVR4nO3Y2QkAIRBEQXU98s/YGBYGZpCqDN5nd2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAApFujlhVeuM9XydnhhbPXMhUqVJhOoUKF+RQqVJhPoUKF+eIL39/47/80AAAAAAAAAAAAAAAAAAAAAAAAAAAAAPx2ARGUD9oUhrtMAAAAAElFTkSuQmCC">';

menuitemsbodyplus.onclick=function(arg,arg2){
  return function() {
    createCustomizationTab(arg,arg2,100);
  }}(tempname,jsonofitems[tempname]);
menuitemsbodyminus.onclick=function(arg,arg2){
    return function() {
      checkandminus(arg,arg2);
    }}(tempname,jsonofitems[tempname]);  





  divChildPlusMinus.appendChild(menuitemsbodyplus);
  divChildPlusMinus.appendChild(menuitemsbodyminus);

  
var temp=JSON.stringify(jsonofitems[itemnamearray[i]]);
div.onclick=  function(arg) {
  return function() {
      
      if( arg.style.height==='90px'){

        resetAllHeights();
        arg.style.height='240px';}
        else{
        arg.style.height='90px';
      } 
  }
}(div);

divChildDescriptionOfFood.innerHTML= jsonofitems[itemnamearray[i]];
divChildPic.style.backgroundImage=window.menuPicArray[Math.floor(1+Math.random() * 10)];  
 
//divChildPic.innerHTML = '<img class="menuitemsbodyactualpic" src="../static/1.jpg">'; 
divChildPic.appendChild(divChildPicVegNonveg);
div.appendChild(divChildPic);
div.appendChild(divChild);
div.appendChild(divChildPlusMinus);  
//div.appendChild(divChildDescriptionOfFood);    
document.getElementById("menuitbody").appendChild(div);}
}






function resetAllHeights(){
  var items=document.getElementsByClassName("slidebody");
  for (var i=0; i < items.length; i++) {
    items[i].style.height='90px' ;
  }

}





document.onreadystatechange = function () {
  var state = document.readyState
  if (state == 'interactive') {
       document.getElementById('menu').style.visibility="hidden";
  } else if (state == 'complete') {
      setTimeout(function(){
         document.getElementById('interactive');
         fadeOutEffect();
          document.getElementById('load').style.visibility="hidden";
          document.getElementById('menu').style.visibility="visible";
      },1000);
  }
}


function fadeOutEffect() {
  var fadeTarget = document.getElementById('load');
  var fadeEffect = setInterval(function () {
      if (!fadeTarget.style.opacity) {
          fadeTarget.style.opacity = 1;
      }
     
      if (fadeTarget.style.opacity > 0) {
          fadeTarget.style.opacity -= 0.1;
      } else {
          clearInterval(fadeEffect);
      }
  }, 50);
}


function  checkandminus(item,text){
   var countfitemareadypresentincart=0;
   for(var i=0;i<window.cart.length;i++){
     if(JSON.stringify(window.cart[i]["item"]) === JSON.stringify(item) ){
       countfitemareadypresentincart= countfitemareadypresentincart+1;}}
      // alert(countfitemareadypresentincart);
     if(countfitemareadypresentincart>1){
       alert("you have multiple vriations.please go to cart to remove");
     }
     if(countfitemareadypresentincart===0){
       alert("you dont have this item in cart yet");
     }  
     if(countfitemareadypresentincart===1){
         for(var j=0;j<window.cart.length;j++){
           if(JSON.stringify(window.cart[j]["item"])===JSON.stringify(item)){
            if(parseInt(window.cart[j]["quantity"])===1){
              window.cart.splice(j,1);
              console.log(window.cart);
             }
                  if(parseInt(window.cart[j]["quantity"])>1){
                    var priceofsingleitem=parseInt(window.cart[j]["price"])/parseInt(window.cart[j]["quantity"]);
                    window.cart[j]["quantity"]=window.cart[j]["quantity"]-1;
                    window.cart[j]["price"]=window.cart[j]["price"]-priceofsingleitem;
                    console.log(window.cart);
                  }
                  
           }
         }





     } 
}


function createCustomizationTab(item,text,baseprice){
    
    if(text["customization"]===true){
          var addtocart=document.createElement('div'); 
          var totalcart=0;
          var customization={};
          var singlechoicejson=text["customizationdata"]['singlechoice'];
          var singlechoicearr=Object.keys(singlechoicejson);
          
          var multiplechoicejson=text["customizationdata"]['multiplechoice'];
          var multiplechoicearr=Object.keys(multiplechoicejson);
          var customizationtab=document.createElement('div');
          customizationtab.id="customizationtab";
          var customizationtabcontent=document.createElement('div');
          customizationtab.className='customizationtab';
          customizationtabcontent.className='customizationtabcontent';
          var singlechoice=Object.keys(singlechoicejson);
          var multiplechoice=Object.keys(multiplechoicejson);
          for(section in singlechoice){
            var singlesectionquery=JSON.stringify(singlechoice[section]);
            var singlesectionoptions=singlechoicejson[singlechoice[section]];
            singlesectionquery = JSON.stringify(singlesectionquery).substring(3, singlesectionquery.length+1); 
            customizationtabcontent.innerHTML+=singlesectionquery + '<br></br>';
            for(option in singlesectionoptions){
            option = JSON.stringify(option).substring(1, option.length+1);  
            var nameofoption=document.createElement('div');
            nameofoption.className='customizationnameofoption';

            var priceofoption=document.createElement('div');  
            priceofoption.className='customizationpriceofoption';
                  



            var checkbox = document.createElement("input"); 
            checkbox.setAttribute("type", "radio");
            checkbox.setAttribute("name", singlesectionquery);
            checkbox.setAttribute("value", [option,singlesectionoptions[option]]);
            checkbox.setAttribute("checked", true);
            //checkbox.setAttribute("onclick", "function(){customization='hey'}");
           
       




            var label= document.createElement("label"); 
            label.setAttribute("for", singlesectionquery);
            label.innerHTML=option;
            nameofoption.appendChild(checkbox); 
            nameofoption.appendChild(label);
            //nameofoption.innerHTML='<input type="radio"  name="'+singlesectionquery+'" value="Bike"> ' + option ;
            priceofoption.innerHTML= JSON.stringify(singlesectionoptions[option]) + '<br></br>';
            customizationtabcontent.appendChild(nameofoption);
            customizationtabcontent.appendChild(priceofoption);
          }}

         for(section in multiplechoice){
          var multiplesectionquery=JSON.stringify(multiplechoice[section]);
          var multiplesectionoptions=multiplechoicejson[multiplechoice[section]];
          multiplesectionquery = JSON.stringify(multiplesectionquery).substring(3, multiplesectionquery.length+1); 
          customizationtabcontent.innerHTML+=multiplesectionquery + '<br></br>';
          for(option in multiplesectionoptions){
          option = JSON.stringify(option).substring(1, option.length+1);  
          var nameofoption=document.createElement('div');
          nameofoption.className='customizationnameofoption';

          var priceofoption=document.createElement('div');  
          priceofoption.className='customizationpriceofoption';
                



          var checkbox = document.createElement("input"); 
          checkbox.setAttribute("type", "checkbox");
          checkbox.setAttribute("name", multiplesectionquery);
          checkbox.setAttribute("value", [option,multiplesectionoptions[option]]);



          var label= document.createElement("label"); 
          label.setAttribute("for", multiplesectionquery);
          label.innerHTML=option;
          nameofoption.appendChild(checkbox); 
          nameofoption.appendChild(label);
         
          //nameofoption.innerHTML='<input type="radio"  name="'+singlesectionquery+'" value="Bike"> ' + option ;
          priceofoption.innerHTML= JSON.stringify(multiplesectionoptions[option]) + '<br></br>';
          customizationtabcontent.appendChild(nameofoption);
          customizationtabcontent.appendChild(priceofoption);
        }}
          
            
                  
            var quantity = document.createElement("INPUT");
            quantity.className="quantitycustomizationinput";
            quantity.setAttribute("type", "number");
            quantity.setAttribute("name", "number of items");
            quantity.setAttribute("value", "1");
           

            addtocart.className='customizetabaddtocart';
            addtocart.id="customizetabaddtocart";
            addtocart.innerHTML='ADD TO CART';
           



            addtocart.onclick=function(){
               


              for(var i=0;i < singlechoicearr.length;i++){
            customization[singlechoicearr[i]]=updatecustomization(singlechoicearr[i]);}
            for(var i=0;i < multiplechoicearr.length;i++){
              customization[multiplechoicearr[i]]=updatecustomization(multiplechoicearr[i]);}
              var quantityofitems=quantity.value;
            updatecart(item,customization,quantityofitems);
          }
          customizationtabcontent.appendChild(quantity);
            
            customizationtab.appendChild(customizationtabcontent);
            customizationtab.appendChild(addtocart);
            document.getElementById("menu").appendChild(customizationtab);}
        else{
          //alert("updating");
          updatecart(item,"none",1);
          
          
        }   
           

    
}
function updatecart(item,customization,quantity){
  var priceofindividualitem=calculatepriceofindividualitem(customization)*parseInt(quantity);
  var newitem={"item":item,"customization":customization,"quantity":parseInt(quantity),"price":priceofindividualitem};
  if(window.cart.length>0){
  var ispresentalready=checkforsameitemandcustomizationincart(newitem);

  if(ispresentalready===false){
    window.cart.push(newitem);}}
  else{
  window.cart.push(newitem);}
  try{
  document.getElementById("customizationtab").remove();}
  catch{
    //alert("updated!");
  }
  console.log(JSON.stringify(window.cart));
}
function checkforsameitemandcustomizationincart(newitem){
   for(var i=0;i<window.cart.length;i++){
        //alert(JSON.stringify(window.cart[i]));
        if(newitem["item"]===window.cart[i]["item"] && JSON.stringify(newitem["customization"])===JSON.stringify(window.cart[i]["customization"])){
          window.cart[i]["quantity"]=window.cart[i]["quantity"]+newitem["quantity"];
          window.cart[i]["price"]=window.cart[i]["price"]+newitem["price"];
          return true;
        }}
      return false;
}
function calculatepriceofindividualitem(customization){
   var price=0;
   var sections=Object.keys(customization);
   for(var i=0;i<sections.length;i++){
    var arrayofitemsselected=customization[sections[i]];
    //price=price+arrayofitemsselected ;
   for(var j=0;j<arrayofitemsselected.length;j++){
      var itempricearray=arrayofitemsselected[j].split(',');
      price=price+parseInt(itempricearray[1]);
   }}
   return price; 
}
function updatecustomization(checkboxName) {
  var checkboxes = document.querySelectorAll('input[name="' + checkboxName + '"]:checked'), values = [];
  Array.prototype.forEach.call(checkboxes, function(el) {
      values.push(el.value);});
 return values;
}













function clearAllBorders(){
  var a=document.getElementsByClassName("menuitemspic");
  for (var i=0; i < a.length; i++) {
    a[i].src=picCategoryArrayFood[i] ;
    
  }
}






function searchitem(){
var text= document.getElementById("textsearch");  
//var men=document.getElementById('menu');
var textvalue=text.value;
var jsonofitems={};
clearFooter("menuitbody");
//men.innerHTML="";
//var data=JSON.stringify(menuitemjson);
var fooddrink;
for (fooddrink in menuitemjson) { 
  
  var category;
  for(category in menuitemjson[fooddrink]){
    var fooditem;
    for(fooditem in menuitemjson[fooddrink][category]){
      var stringfooditem=JSON.stringify(fooditem);
      if( stringfooditem.includes(textvalue.toLowerCase())){

         var price=menuitemjson[fooddrink][category][fooditem];
         jsonofitems[stringfooditem]=price;
        
         
      }
    }
  }
}
var stringresult=JSON.stringify(jsonofitems);
var finalData = stringresult.replace(/\\/g, "");
var finallymadedata=finalData.replace('""','"');
var thisoneisfinal = finallymadedata.replace(/""/g, '"');
var nopethisone=JSON.parse(thisoneisfinal);
var a=JSON.stringify(nopethisone);
//men.innerHTML+=a;

populateBody("restaurantName",nopethisone,menuPicArray);  
document.getElementById("textsearch").value = "";
document.getElementById("textsearch").blur();

}
