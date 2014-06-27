$(document).ready(function() {
  loadImages();
});

$(document).keypress(function(e){
  if (e.keyCode == 97){
    //A, pick left
    rankImages($('#img-left').attr('data-id'), $('#img-right').attr('data-id'));
  }
  else if (e.keyCode == 115){
    //S, pick right
    rankImages($('#img-right').attr('data-id'), $('#img-left').attr('data-id'));
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

$("#img-left").click(function(e){
  rankImages($('#img-left').attr('src'), $('#img-right').attr('src'));
});

$("#img-right").click(function(e){
  rankImages($('#img-right').attr('src'), $('#img-left').attr('src'));
});


function clearImages(){
  $('#img-left').attr('src', '/static/loading.gif');
  $('#img-right').attr('src', '/static/loading.gif');
  $('#img-left').attr('data-id', '');
  $('#img-right').attr('data-id', '');
  $('#text-left').text('');
  $('#text-right').text('');
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
            $('#img-left').attr('src', result.a.image_url);
            $('#img-right').attr('src', result.b.image_url);
            $('#img-left').attr('data-id', result.a.product_id);
            $('#img-right').attr('data-id', result.b.product_id);
            $('#text-left').text(result.a.text);
            $('#text-right').text(result.b.text);
          }
  });
};

