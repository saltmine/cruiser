$(document).ready(function() {
  loadImages();
});

$(document).keypress(function(e){
  if (e.keyCode == 97){
    //A, pick left
    $('.pc.card-left').addClass('pc-selected');
    rankImages($('.cruiser-img.card-left').attr('data-id'), $('.cruiser-img.card-right').attr('data-id'));
  }
  else if (e.keyCode == 115){
    //S, pick right
    $('.pc.card-right').addClass('pc-selected');
    rankImages($('.cruiser-img.card-right').attr('data-id'), $('.cruiser-img.card-left').attr('data-id'));
  }
});

$("#del-left").click(function(e){
  $.ajax({url:"/set_ignored/",
          data: {"to_ignore": $('#img-left').attr('data-id')},
          success: loadImages
  });
  clearImages();
});

$("#del-right").click(function(e){
  $.ajax({url:"/set_ignored/",
          data: {"to_ignore": $('#img-right').attr('src')},
          success: loadImages
  });
  clearImages();
});

$(".cruiser-img.card-left").click(function(e){
  $('.pc.card-left').addClass('pc-selected');
  rankImages($('.cruiser-img.card-left').attr('src'), $('.cruiser-img.card-right').attr('src'));
});

$(".cruiser-img.card-right").click(function(e){
  $('.pc.card-right').addClass('pc-selected');
  rankImages($('.cruiser-img.card-right').attr('src'), $('.cruiser-img.card-left').attr('src'));
});


function clearImages(){
  $('.cruiser-img').attr('src', '/static/loading.gif');
  $('.cruiser-img').attr('data-id', '');
  $('.cruiser-text').text('');
  $('.cruiser-link').attr('href', '#');
};


function rankImages(winner, loser) {
  $.ajax({url:"/save_comparison/",
          data: {"winner": winner,
                 "loser": loser},
          success: loadImages
  });
  clearImages();
};


function loadImages() {
  $.ajax({url:"/get_comparison/",
          success:function(result){
            $('.cruiser-img.card-left').attr('src', result.a.image_url);
            $('.cruiser-img.card-right').attr('src', result.b.image_url);
            $('.cruiser-img.card-left').attr('data-id', result.a.product_id);
            $('.cruiser-img.card-right').attr('data-id', result.b.product_id);
            $('.cruiser-text.card-left').text(result.a.text);
            $('.cruiser-text.card-right').text(result.b.text);
            $('.cruiser-link.card-left').attr('href', result.a.link);
            $('.cruiser-link.card-right').attr('href', result.b.link);
            $('.pc-selected').removeClass('pc-selected');
          }
  });
};

