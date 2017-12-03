(function(){

    msgTemplate = _.template(`
    <li class="time-line-list-item">
    <div class="time-line-structure time-line-clock">
      <p class="time-line-clock-text"><%= ts %><span>am</span></p>
    </div>
    <div class="time-line-structure time-line-icon message">
      <span><i class="fa fa-envelope"></i></span>
    </div>
    <div class="time-line-structure time-line-text">
      <p class="log-type"><%= title %></p>
      <p class="contact-name"><%= msg %></p>
    </div>
  </li>
    `);


    getMsgs = function(phone) {
        return apiCall("GET", "/sms/"+phone ).done(function(data) {
          console.log(data);
          if(data['status'] == '1'){
            $('#msgs-container').empty();
            var newLis = _.map(data['data']['msgs'], msgTemplate);
            _.each(newLis, function(x){ $('#msgs-container').append(x);  } );
          }else{
            // show error
          }
        });
      };





      $(function() {
        var phone = window.location.hash.substring(1);
        if(phone.length>0){
            $('h1').text(phone);
            getMsgs(phone);
        }
      });
}).call(this);
