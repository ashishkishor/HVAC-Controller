AWS.config.update({
  region: "eu-west-1",
  // accessKeyId default can be used while using the downloadable version of DynamoDB. 
  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
  accessKeyId: "AKIAQTN33AHNTAOVSIEZ",
  // secretAccessKey default can be used while using the downloadable version of DynamoDB. 
  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
  secretAccessKey: "8NhJ+/lba8xq87tnaumycqR7mcH9Hgx9BfkjOJ4C"
});

var rtemp = new Array(0);
var actemp = new Array(0);
var fantemp = new Array(0);
var heatertemp = new Array(0);

var docClient = new AWS.DynamoDB.DocumentClient();

function cloudDBAuth()
{
      var username = document.getElementById('username').value;
      var password= document.getElementById('password').value;
      //Form Validation starts
      if(username==="" || password===""){
        if(username===""){
          alert("Please Enter Username");
          document.getElementById('username').focus();
        }
        else if(password===""){
          alert("Please Enter Password");
          document.getElementById('password').focus();
        }
        return;
      }
       //Form Validation ends
       var params = {
        TableName :"user_reg",
        Key:{
            "username": username
        }
    };
   
 docClient.get(params, function(err, data) {
        if (err) {
            alert('No Such User,' + err);
        } else {
              
             var pass = data['Item']['password'];
             if(pass == password)
             {
             sessionStorage.setItem('username', username);
             window.location.href = "dashboard.html";
             }
            else{
                 alert("Please enter correct Password");
                   } 
        }
    });
}

function cloudDBInsert()
{
      var username = document.getElementById('username').value;
      var password= document.getElementById('password').value;
      var device_id = document.getElementById('dev_id').value;
      //Form Validation starts
      if(username==="" || password==="" || device_id===""){
        if(username===""){
          alert("Please Enter Username");
          document.getElementById('username').focus();
        }
        else if(password===""){
          alert("Please Enter Password");
          document.getElementById('password').focus();
        }
        else if(device_id===""){
          alert("Please Enter Device ID");
          document.getElementById('dev_id').focus();
        }
        return;
      }
      //Form Validation ends
       var params = {
        TableName :"user_reg",
        Item:{
            "username": username,
            "password": password ,
            "device_id": device_id
        }
    };
   
 docClient.put(params, function(err, data) {
        if (err) {
            alert('User Creation Error, ' + err);
        } else {
             window.location.href = "success_page.html"
        }
    });
}


function renderDashboard()
{

if(sessionStorage.getItem('username') == null)
{
  if (window.confirm('Not Allowed, Please Login')) 
    {
      window.location.href='login.html';
    };
}

var username = sessionStorage.getItem('username');

var user_dev = document.getElementById('user_dev');
var params = {
        TableName :"user_reg",
        Key:{
            "username": username,
        }
    };

 docClient.get(params, function(err, data) {
        if (err) {
                      alert("error : "+err);
        } else {
             var ud = "<b>Username: </b>"+data['Item']['username'] +"\t"+"<b>Device ID:</b>" +data['Item']['device_id'];
             sessionStorage.setItem('device_id',data['Item']['device_id']);
             user_dev.innerHTML = ud;
        }
    });

var params = {
        TableName :"hvac_device",
        Key:{
            "device_id": ""+sessionStorage.getItem('device_id') ,
        }
    };

 docClient.get(params, function(err, data) {
        if (err) {
                      alert("error : "+err);
        } else {
                          const datetime = new Date(Date.now());
                          console.log(data);
                          document.getElementById('log_data').innerHTML = document.getElementById('log_data').value + "<span style = 'background: yellow; color:black;'>"+datetime.toDateString()+"</span><b>&nbsp;Device ID : </b>" + data['Item']['device_id']+ "<br><b>AC : </b>{ <b>FanSpeed=</b>"+  data['Item']['AC_fanspeed'] +", <b>Status=</b>" + data['Item']['AC_status'] + ", <b>Temp=</b>"+ data['Item']['AC_temp'] + " } <b>Fan :{ Fan Status=</b>"+ data['Item']['Fan_status']+", <b>FanSpeed=</b>"+ data['Item']['Fan_fanspeed'] +" } <b>Heater : </b>{ <b>Status=</b> " +  data['Item']['Heater_status'] +", <b>Temp=</b>" + data['Item']['Heater_temp']+" }<br><br>";

                           document.getElementById('temp_data').innerHTML = "<h7 style='color:white;' > Last Reported Room Temperature : " +data['Item']['room_temp'] +"&degC</h7>";
                          document.getElementById('ac_data').innerHTML = "<h7 style='color:white;' > Last Reported AC Temperature : " +data['Item']['AC_temp'] +"&degC</h7>";
                           document.getElementById('fan_data').innerHTML = "<h7 style='color:white;' > Last Reported Fan Speed: " +data['Item']['Fan_fanspeed'] +"</h7>";
                            document.getElementById('heater_data').innerHTML = "<h7 style='color:white;' > Last Reported Heater Temperature : " +data['Item']['Heater_temp'] +"&degC</h7>";
                            var avg_temp = (parseInt(data['Item']['AC_temp'])+ parseInt(data['Item']['Fan_fanspeed'] ) + parseInt(data['Item']['Heater_temp'] ))/2;
                             document.getElementById('stat_data').innerHTML = "<h7 style='color:white;' > Average Current Regulated Temperature : <b>" +avg_temp+"&degC</b></h7><br>";
                             document.getElementById('stat_data').innerHTML =  document.getElementById('stat_data').innerHTML+  "<h7 style='color:white;' > All Reports Reported Last at : <b> " +datetime.toUTCString()+"</b></h7>";
                             document.getElementById('monitor').innerHTML =  document.getElementById('monitor').innerHTML + "<h7 style='color:white;' > AC is currently <b> " +data['Item']['AC_status']+"</b></h7><br>";
                              document.getElementById('monitor').innerHTML =  document.getElementById('monitor').innerHTML + "<h7 style='color:white;' >Fan is currently <b>" +data['Item']['Fan_status']+"</b></span></h7><br>";
                               document.getElementById('monitor').innerHTML =   document.getElementById('monitor').innerHTML  + "<h7 style='color:white;' > Heater is currently <b>" +data['Item']['Heater_status']+"</b></span></h7><br>";

        }
    });
var layout = { width: 600, height: 500, margin: { t: 0, b: 0 },  };
Plotly.newPlot(document.getElementById('temp_canvas'), [{
	x: [0,5,10,15,20,25,30,35,40,45,50],
	y: rtemp}], {
	margin: { t: 0 } , xaxis : {title : {text :"Time"} }, yaxis :  {title : {text :"Temp/Fan Speed"} } });

Plotly.newPlot(document.getElementById('ac_canvas'), [{
	x: [0,5,10,15,20,25,30,35,40,45,50],
	y: actemp }], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} } } );

Plotly.newPlot(document.getElementById('fan_canvas'), [{
	x:  [0,5,10,15,20,25,30,35,40,45,50],
	y: fantemp}], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} }});

Plotly.newPlot(document.getElementById('heater_canvas'), [{
	x:  [0,5,10,15,20,25,30,35,40,45,50],
	y:  heatertemp}], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} } });

}

function resetPlot()
{
rtemp.length = 0;
actemp.length = 0;
fantemp.length = 0;
heatertemp.length = 0;
}

function renderLogs()
{
if(sessionStorage.getItem('username') == null)
{

  if (window.confirm('Not Allowed, Please Login')) 
  {
    window.location.href='login.html';
  };
}

document.getElementById('temp_canvas').innerHTML = "";
document.getElementById('ac_canvas').innerHTML = "";
document.getElementById('fan_canvas').innerHTML = "";
document.getElementById('heater_canvas').innerHTML = "";
document.getElementById('monitor').innerHTML = "";
document.getElementById('stat_data').innerHTML ="";
var params = {
        TableName :"hvac_device",
        Key:{
            "device_id": sessionStorage.getItem('device_id') ,
        }
    };

 docClient.get(params, function(err, data) {
        if (err) {
                      alert("error : "+err);
        } else {
                          const datetime = new Date(Date.now());
                          document.getElementById('log_data').innerHTML = document.getElementById('log_data').innerHTML+ "<p><span style = 'background: yellow; color:black;'><b>"+datetime.toUTCString()+"</b></span><b>&nbsp;Device ID :</b>" + data['Item']['device_id']+ "<br><b>AC : </b>{ <b>FanSpeed=</b>"+  data['Item']['AC_fanspeed'] +", <b>Status=</b>" + data['Item']['AC_status'] + ", <b>Temp=</b>"+ data['Item']['AC_temp'] + " } <b>Fan :{ Fan Status=</b>"+ data['Item']['Fan_status']+", <b>FanSpeed=</b>"+ data['Item']['Fan_fanspeed'] +" } <b>Heater : </b>{ <b>Status=</b> " +  data['Item']['Heater_status'] +", <b>Temp=</b>" + data['Item']['Heater_temp']+" }</p>";

                           document.getElementById('temp_data').innerHTML = "<h7 style='color:white;' > Last Reported Room Temperature : " +data['Item']['room_temp'] +"&degC</h7>";
                          document.getElementById('ac_data').innerHTML = "<h7 style='color:white;' > Last Reported AC Temperature : " +data['Item']['AC_temp'] +"&degC</h7>";
                           document.getElementById('fan_data').innerHTML = "<h7 style='color:white;' > Last Reported Fan Speed: " +data['Item']['Fan_fanspeed'] +"</h7>";
                            document.getElementById('heater_data').innerHTML = "<h7 style='color:white;' > Last Reported Heater Temperature : " +data['Item']['Heater_temp'] +"&degC</h7>";
                          var avg_temp = (parseInt(data['Item']['AC_temp'])+ parseInt(data['Item']['Fan_fanspeed'] ) + parseInt(data['Item']['Heater_temp'] ))/2;                             
                          document.getElementById('stat_data').innerHTML = "<h7 style='color:white;' > Average Current Regulated Temperature : " +avg_temp+"&degC</h7><br>";
 document.getElementById('stat_data').innerHTML =  document.getElementById('stat_data').innerHTML+  "<h7 style='color:white;' > All Reports Reported Last at : <b> " +datetime.toUTCString()+"</b></h7><br>";
                             document.getElementById('monitor').innerHTML =   "<h7 style='color:white;' > AC is currently <b>" +data['Item']['AC_status']+"</b></h7><br>";
                              document.getElementById('monitor').innerHTML =  document.getElementById('monitor').innerHTML + "<h7 style='color:white;' >Fan is currently <b>" +data['Item']['Fan_status']+"</b></h7><br>";
                               document.getElementById('monitor').innerHTML =   document.getElementById('monitor').innerHTML  + "<h7 style='color:white;' > Heater is currently <b>" +data['Item']['Heater_status']+"</b></h7><br>";
                            rtemp.push(parseInt(data['Item']['room_temp']));
                            actemp.push(parseInt(data['Item']['AC_temp']));
                            fantemp.push(parseInt(data['Item']['Fan_fanspeed']));
                            heatertemp.push(parseInt(data['Item']['Heater_temp']));
                         
        }
    });


Plotly.newPlot(document.getElementById('temp_canvas'), [{
	x: [0,5,10,15,20,25,30,35,40,45,50],
	y: rtemp}], {
	margin: { t: 0 } , xaxis : {title : {text :"Time"} }, yaxis :  {title : {text :"Temp/Fan Speed"} } });

Plotly.newPlot(document.getElementById('ac_canvas'), [{
	x: [0,5,10,15,20,25,30,35,40,45,50],
	y: actemp }], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} } } );

Plotly.newPlot(document.getElementById('fan_canvas'), [{
	x:  [0,5,10,15,20,25,30,35,40,45,50],
	y: fantemp}], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} }});

Plotly.newPlot(document.getElementById('heater_canvas'), [{
	x:  [0,5,10,15,20,25,30,35,40,45,50],
	y:  heatertemp}], {
	margin: { t: 0 }, xaxis : {title : {text :"Time"} },  yaxis :  {title : {text :"Temp/Fan Speed"} } });

}


function logout()
{
window.location.href = "logout.html";
sessionStorage.clear();
}


