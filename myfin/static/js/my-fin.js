   function ChangeSumFrom() {
        var sum_from = document.getElementsByName("sum_transaction_from");
        var sum_to = document.getElementsByName("sum_transaction_to");  
        var cur_from = document.getElementsByName("currency_from"); 
        var cur_to = document.getElementsByName("currency_to");
		var course = document.getElementsByName("course");
		
		 if(cur_from[0].value!=cur_to[0].value) {       
          res = sum_to[0].value/sum_from[0].value;
		  course[0].value = parseFloat(res.toFixed(4));
        }   
		else {
			sum_to[0].value = sum_from[0].value;
			course[0].value = 1;
		}	
    }
    
    function ChangeSumTo() {
        var sum_from = document.getElementsByName("sum_transaction_from");
        var sum_to = document.getElementsByName("sum_transaction_to");  
		var cur_from = document.getElementsByName("currency_from"); 
        var cur_to = document.getElementsByName("currency_to");
		var course = document.getElementsByName("course");
		
		 if(cur_from[0].value!=cur_to[0].value) {       
          res = sum_to[0].value/sum_from[0].value;
		  course[0].value = parseFloat(res.toFixed(4));
        }         
    }
    
   function ShowHiddenFields() {
       var cur_from = document.getElementsByName("currency_from"); 
       var cur_to = document.getElementsByName("currency_to");
       var sum_from = document.getElementsByName("sum_transaction_from");
       var sum_to = document.getElementsByName("sum_transaction_to");  
	   var course = document.getElementsByName("course");

       if(cur_from[0].value==cur_to[0].value) {       
          sum_to[0].hidden = true; 
		   cur_to[0].hidden = true; 
           label = document.querySelector("label[for=id_sum_transaction_to]");
           label.hidden = true; 
		   
		   course[0].hidden = true; 
		   label = document.querySelector("label[for=id_course]");
           label.hidden = true; 
        } 
              
       else {
           sum_to[0].hidden = false; 
		   cur_to[0].hidden = false; 
           label = document.querySelector("label[for=id_sum_transaction_to]");
           label.hidden = false; 
   
		   course[0].hidden = false; 
		   label = document.querySelector("label[for=id_course]");
           label.hidden = false;
       }
   } 
    
  function SetCurrancyWallet(id,cur_from) {
         var result='11';
         var url ="http://127.0.0.1:8000/get_currance_wallet/?id_wallet="+id;
         defaults = {'method': 'GET'};
         fetch(url, defaults)
  
        .then(function(response) {
          response.text().then(function(result) {
               cur_from[0].value = result;  
               ShowHiddenFields();   
            });   
                        
         })
         
     }
     
     function ChangeWalletFrom() {
       var wal_from = document.getElementsByName("wallet_from");
       var cur_from = document.getElementsByName("currency_from");  
       wal_id = wal_from[0].value;
       SetCurrancyWallet(wal_id,cur_from) ;      
    }
    
     function ChangeWalletTo() {
       var wal_to = document.getElementsByName("wallet_to");
       var cur_to = document.getElementsByName("currency_to");  
       wal_id = wal_to[0].value;
       SetCurrancyWallet(wal_id,cur_to) ;      
    }
	
	
	function SelectImage(name_img,name_folder) {        
		image = document.getElementsByName("image");
		image[0].value = name_img; 	
        var img = new Image();
        img.addEventListener("load", function() {
            document.getElementById("img_to").src = img.src;
            setTimeout(function() {
                img.src = "/static/icon/" + name_folder + "/" + name_img + "?" + (new Date).getTime();
            }, 1000/15); 
        })
        document.getElementById("img_to").src = "/static/icon/" + name_folder + "/" + name_img + "?" + (new Date).getTime();
    }
	
	function ChangeTypeReport() {
	/***window.location='/reports/?currency='+document.getElementsByName('currency')[0].value+'&id='+this.value;***/
       var report_id = document.getElementsByName("id"); 
	   var date_start = document.getElementsByName("date_start");
	   var date_end = document.getElementsByName("date_end");
	   label_date_start = document.querySelector("label[for=id_date_start");
	   label_date_end = document.querySelector("label[for=id_date_end");
         
      if(report_id[0].value!=1 && report_id[0].value!=5) {       
           date_start[0].hidden = true; 
		   date_end[0].hidden = true;
		   label_date_start.hidden = true; 
		   label_date_end.hidden = true; 
	   }
		else {
			date_start[0].hidden = false;
			date_end[0].hidden = false;
			label_date_start.hidden = false; 
			label_date_end.hidden = false; 
        } 

    }

	
	