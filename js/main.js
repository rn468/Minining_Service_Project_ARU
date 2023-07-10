// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'https://api.github.com/search/repositories?q=Aarch64', true)

//searching with keyword Aarch64
//request.open('GET','https://api.github.com/search/repositories?q=Aarch64',true)


request.onload = function () {
  // Begin accessing JSON data here
  var data = JSON.parse(this.response);

  var statusHTML = '';
  $.each(data.items, function(i, status) {//each function to loop,data is the response from server,function that processes key-value pair
    statusHTML += '<tr>';
    statusHTML += '<td>' + status.id + '</td>';
    statusHTML += '<td>' + status.name + '</td>';
    statusHTML += '<td>' + status.html_url + '</td>';
    statusHTML += '<td>' + status.language + '</td>';
    statusHTML += '<td>' + status.commits_url + '</td>';
    statusHTML += '<td>' + status.pulls_url + '</td>';
    statusHTML += '</tr>';
  }); 
  $('tbody').html(statusHTML);


  $.post(data,function (result){
    var blob=new Blob([result]);
    var link=document.createElement('a');
    link.href=window.URL.createObjectURL(blob);
    link.download="myFileName.txt";
    link.click();
  });


  //$.post('/create_binary_file.php', postData, function(retData) {                  // download file in php format that will store url to create downloadable data
  //  $("body").append("<iframe src='" + retData.url+ "' style='display: none;' ></iframe>");
  //}); 
}

// Send request
request.send();