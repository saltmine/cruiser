$(document).ready(function() {
  loadImage();
});

$(document).keypress(function(e){
  if (e.keyCode == 97){
    //A, fail it
    $('.pc.classify-card').addClass('pc-reject');
    setTimeout(function() {
      $('.pc.classify-card').removeClass('pc-accept');
      $('.pc.classify-card').removeClass('pc-reject');
    }, 200);
    classifyImage(0);
  }
  else if (e.keyCode == 115){
    //S, pass it
    $('.pc.classify-card').addClass('pc-accept');
    setTimeout(function() {
      $('.pc.classify-card').removeClass('pc-accept');
      $('.pc.classify-card').removeClass('pc-reject');
    }, 200);
    classifyImage(1);
  }
});


function classifyImage(keep) {
  if ($('.cruiser-img.classify-card').attr('data-id') != '') {
    $.ajax({url:"/save_classify/",
            data: {"save_image": keep,
                   "to_classify_id": $('.cruiser-img.classify-card').attr('data-id')},
            success: loadImage
    });
    $('.cruiser-img.classify-card').attr('src', '/static/loading.gif');
    $('.cruiser-img.classify-card').attr('data-id', '');
    $('.cruiser-text.classify-card').text('');
    $('.cruiser-link.classify-card').attr('href', '#');
  }
};


function loadImage() {
  $.ajax({url:"/get_classify/",
          success:function(result){
            $('.cruiser-img.classify-card').attr('src', result.to_classify.image_url);
            $('.cruiser-img.classify-card').attr('data-id', result.to_classify.product_id);
            $('.cruiser-text.classify-card').text(result.to_classify.text);
            $('.cruiser-link.classify-card').attr('href', result.to_classify.link);
            $('#remaining').text(result.to_classify_count);
          }
  });
};
