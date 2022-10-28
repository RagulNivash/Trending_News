const container = document.querySelector(".container"),
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password"),
      signUp = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link"),
      form = document.querySelector("form"),
      eInput = form.querySelector(".input"),
      text = form.querySelector(".text"),
      emailfield = document.querySelectorAll(".email-input"),
      emailinput = document.querySelectorAll(".email"),
      passfield = document.querySelectorAll(".createpassword"),
      cnfPassfield = document.querySelectorAll(".confirmpassword"),
      loginbutton = document.querySelector(".loginbutton"),
      signupbutton = document.querySelector(".submit"),
      cnfpassinput = document.querySelector(".confirmpass");


      


    //   js code to show/hide password and change icon
    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener("click", ()=>{
            pwFields.forEach(pwField =>{
                if(pwField.type ==="password"){
                    pwField.type = "text";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                    })
                }else{
                    pwField.type = "password";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye", "uil-eye-slash");
                    })
                }
            }) 
        })
    })

    // js code to appear signup and login form
    signUp.addEventListener("click", ( )=>{
        container.classList.add("active");
    });
    login.addEventListener("click", ( )=>{
        container.classList.remove("active");
    });

    
 

    // // Calling Funtion on Form Sumbit
    // form.addEventListener("submit", (e) => {
    //     e.preventDefault(); //preventing form submitting
    //     verfyemail();
    // }


    $(document).ready(function(){
		// set initially button state hidden
		$("#submit").hide();
		// use keyup event on email field
		$("#email").keyup(function(){
			if(validateEmail()){
				// if the email is validated
				// set input email border green
                $("#emailmsg").html("<p>Validated</p>");
				$("#email").css("border","2px solid green");
				// and set label 
				
			}else{
				// if the email is not validated
				// set border red
				$("#email").css("border","2px solid red");
				$("#emailmsg").html("<p class='error-text'>Please enter a valid email</p>");
                
			}
			buttonState();
		});
		// use keyup event on password
		$("#pass").keyup(function(){
			// check
			if(validatePassword()){
				// set input password border green
				$("#pass").css("border","2px solid green");
				 //set passMsg 
				$("#passmsg").html("<p> </p>");
			}else{
					// set input password border red
				$("#pass").css("border","2px solid red");
				    //set passMsg 
				$("#passmsg").html("<p class='error-text'>Password should have atleast 8 charatcer.</p>");

			}
			buttonState();
		});
	});


    $("#cnfpass").keyup(function(){
        // check
        if(validatePassword()){
            // set input password border green
            $("#cnfpass").css("border","2px solid green");
             //set passMsg 
            $("#cnfpassmsg").html("<p> </p>");
        }else{
                // set input password border red
            $("#cnfpass").css("border","2px solid red");
                //set passMsg 
            $("#cnfpassmsg").html("<p class='error-text'>Password should have atleast 8 charatcer.</p>");

        }
        buttonState();
    });

    





	function buttonState(){
		if(validateEmail() && validatePassword() && validateConfirmPass){
			// if the both email and password are validate
			// then button should show visible
			$("#submit").show();
		}else{
			// if both email and pasword are not validated
			// button state should hidden
			$("#submit").hide();
		}
	}
	function validateEmail(){
		// get value of input email
		var email=$("#email").val();
		// use reular expression
		 var reg = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
		 if(reg.test(email)){
		 	return true;
		 }else{
		 	return false;
		 }

	}
	function validatePassword(){
		//get input password value
		var pass=$("#pass").val();
		// check it s length
		if(pass.length > 8 ){
			return true;
		}else{
			return false;
		}

	}

    function validateConfirmPass(){
        var cnfpass=$("#cnfpass").val();
        var pass=$("#pass").val();
        if(cnfpass == pass){
            return true;}
        else{
            return false

        
        }

    }


    loginbutton.addEventListener("click", ( )=>{
        var data = {};
        data.email = $('#enteremail').val();
        data.password2 = $('#password2').val();

        $.post('/jquery/submitData',   // url
       { myData: data }, // data to be submit
       function(data, status, jqXHR) {// success callback
                // $('p').append('status: ' + status + ', data: ' + data);
            if(data.msg == authorize && status== success){
                window.location.href = 'dashboard.html';
                }
                else{
                    $("#enteremail").html("<p>User not authorized.</p>");
             
                }
        })

        console.log("calling api")
        console.log(JSON.stringify(data))
        
    });

    signupbutton.addEventListener("click", ( )=>{
        var data1 = {};
        data1.username = $('#username').val();
        data1.emailsignup = $("#email").val();
        data1.password = $('#pass').val();
        data1.cnfpassword =$('#cnfpass').val();

    //     $.post('/jquery/submitData',   // url
    //    { myData1: data1 }, // data to be submit
    //    function(data1, status, jqXHR) {// success callback
    //             // $('p').append('status: ' + status + ', data: ' + data);
    //         if(data1.msg == authorize && status== success && data1.password==data1.cnfpassword){
    //             window.location.href = 'registeration.html';
    //             }
    //             else{
    //                 $("#enteremail").html("<p>Registeration failed.</p>");
             
    //             }
        console.log(JSON.stringify(data1))
        });




   




        // $.get("https://dog.ceo/api/breeds/list/all", function (data, status) {
        // if(data.msg == authorize && status== success){
        // window.location.href = 'dashboard.html';
        // }
        // else{
        //     $("#enteremail").html("<p>User not authorized.</p>");
 
        // }

        // });

    
    

 

  
  