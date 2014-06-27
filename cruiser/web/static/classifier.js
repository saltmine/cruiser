$(document).ready(function() {
  loadImage();
});

$(document).keypress(function(e){
  if (e.keyCode == 97){
    //A, fail it
    classifyImage(0);
  }
  else if (e.keyCode == 115){
    //S, pass it
    classifyImage(1);
  }
});


function classifyImage(keep) {
  if ($('#main-img').attr('data-id') != '') {
    $.ajax({url:"/save_classify/",
            data: {"save_image": keep,
                   "to_classify_id": $('#main-img').attr('data-id')},
            success: loadImage
    });
    $('#main-img').attr('src', '/static/loading.gif');
    $('#main-img').attr('data-id', '');
    $('#text').text('');
  }
};


function loadImage() {
  $.ajax({url:"/get_classify/",
          success:function(result){
            $('#main-img').attr('src', result.to_classify.image_url);
            $('#main-img').attr('data-id', result.to_classify.product_id);
            $('#text').text(result.to_classify.text);
            $('#remaining').text(result.to_classify_count);
          }
  });
};
