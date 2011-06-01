
  $(document).ready(function() {
	
	var dummyVal = "Votre email ici";
	
	$('#mailInput').focus(function() {
	  if(this.value == this.defaultValue){
	       this.value="";
	    }
	 
	});
	
	$('#mailInput').blur(function() {
	  if(this.value == ""){
	        this.value=dummyVal;
	    }
	 
	});
	
	
	
    $("#subForm input:submit").click(function() { 

		
      // First, disable the form from submitting
      $('form#subForm').submit(function() { return false; });
	
	
      // Grab form action
      var formAction = $("form#subForm").attr("action");

      // Hacking together id for email field
      // Replace the xxxxx below:
      // If your form action were http://mysiteaddress.createsend.com/t/r/s/abcde/, then you'd enter "abcde" below
      var id = "ykjhc";
      var emailId = "mailInput";

      // Validate email address with regex
      if (!checkEmail(emailId)) {
			$("#error").text("PLEASE INPUT A VALID EMAIL");
			$("#error").fadeIn("normal");  // Shows "Thanks for subscribing" div
			
			
			
			setTimeout(function() { $('#error').fadeOut("normal"); }, 3000);
			
			
			//setTimeout(function() { $('#error').fadeOut("slow"); }, 3000);

						
        return false;
      }

      // Serialize form values to be submitted with POST
      var str = $("form#subForm").serialize();

      // Add form action to end of serialized data
      // CDATA is used to avoid validation errors
      //<![CDATA[
      var serialized = str + "&action=" + formAction;
      // ]]>

      // Submit the form via ajax
      $.ajax({
        url: "http://www.enjoy-digital.fr/proxy.php",
        type: "POST",
        data: serialized,
        success: function(data){
          // Server-side validation
          if (data.search(/invalid/i) != -1) {
 			$('#error').hide();
          }
          else
          {
            $("form").hide(); // If successfully submitted hides the form
            $("#confirmation").fadeIn("slow");  // Shows "Thanks for subscribing" div
            $("#confirmation").tabIndex = -1;
            $("#confirmation").focus(); // For screen reader accessibility
          }
        }
      });
    });
    
     function checkEmail(email) { 
    var pattern = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var emailVal = $("#" + email).val();
    return pattern.test(emailVal);
  }
  });