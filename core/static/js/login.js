
(function(){
    login = function(e) {
        e.preventDefault();
        return apiCall("POST", "/sms/login", $("#login-form").serializeObject()).done(function(data) {
          if(data['status'] == '1'){
            window.location.href = "/#"+data['data']['phone'];
          }else{
            // show error
          }
        });
      };

      $(function() {
        $("#login-form").on("submit", login);
      });
}).call(this);
