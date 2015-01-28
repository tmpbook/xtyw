// JavaScript Document
/*Javascript代码片段，这里使用jQuery*/


    function check_values() {
        if ($("#username").val().length !== 0 && $("#password").val().length !== 0) {
            $("#loginbtn").animate({ left: '0' , duration: 'slow'});
            $("#lockbtn").animate({ left: '500px' , duration: 'slow'});
        }else{
          $("#loginbtn").animate({ left: '500px' , duration: 'slow'});
          $("#lockbtn").animate({ left: '0px' , duration: 'slow'});
        }
    }

				
	$("#loginbtn").click(function(){
		$('#loading').removeClass('hidden');
		//登录相关后台处理，例如: Ajax请求
	});

    
 $(function(){
     $("#id_username").blur(function(){//用户名文本框失去焦点触发验证事件
        if(!$(this).val || !$(this).val.match(/([w]){2,15}$/))//只处验证不能为空并且只能为英文或者数字或者下划线组成的２－１５个字符
        {
            $("#nameTip").html("用户名不能为空且只能为英文或者数字");
        }
        else
        {
            $("#nameTip").html("输入正确");
        }

     });

      $("#id_password1").blur(function(){//用户名文本框失去焦点触发验证事件
        if(!$(this).val || !$(this).val.match(/([w]){2,15}$/))//只处验证和上面一样
        {
            $("#pas1Tip").html("密码不能为空且只能为英文或者数字");
        }
        else
        {
            $("#pas1Tip").html("输入正确");
        }

     });
     $("#id_password2").blur(function(){//用户名文本框失去焦点触发验证事件
        if(!$(this).val || $(this).val() != $("#id_password1").val() )//只处验证和上面一样
        {
            $("#pas2Tip").html("密码为空或者和上面的密码不致");
        }
        else
        {
            $("#pas2Tip").html("输入正确");
        }

     });

})