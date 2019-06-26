var $ken = $('.ken');
var $kenPos, $fireballPos;

var punch = function(){ // 普通攻击
  $ken.addClass('punch'); //修改class属性吗，为啥?
  setTimeout(function() { $ken.removeClass('punch'); }, 150);  // 设置时间，1.5毫秒就移除这个class类
};
var kick = function(){
  $ken.addClass('kick');
  setTimeout(function() { $ken.removeClass('kick'); }, 500);
};
var rkick = function(){
  $ken.addClass('reversekick');
  setTimeout(function() { $ken.removeClass('reversekick'); }, 500); 
};
var tatsumaki = function(){
  $ken.addClass('tatsumaki');
  setTimeout(function() { $ken.addClass('down'); }, 1500); 
  setTimeout(function() { $ken.removeClass('tatsumaki down'); }, 2000);
};
var hadoken = function(){
  $ken.addClass('hadoken'); 
  setTimeout(function() { $ken.removeClass('hadoken'); }, 500); // 角色的动作结束，但是波还是在的
  setTimeout(function() {
      var $fireball = $('<div/>', { class:'fireball' });
      $fireball.appendTo($ken);  // 追加到子节点下
              
      var isFireballColision = function(){ // 判断是不是到了隔屏幕75的距离
          return $fireballPos.left + 75 > $(window).width() ? true : false;
      };
  
      var explodeIfColision = setInterval(function(){ // setInterval是重复跑的意思吗

          $fireballPos = $fireball.offset();
          //console.log('fireballInterval:',$fireballPos.left);
  
          if (isFireballColision()) {
              $fireball.addClass('explode').removeClass('moving').css('marginLeft','+=22px'); 
              clearInterval(explodeIfColision);
              setTimeout(function() { $fireball.remove(); }, 500); 
          }
  
      }, 50);
  
      setTimeout(function() { $fireball.addClass('moving'); }, 20);  // 20是这个波出现后，0.2毫秒，添加moving状态
              
      setTimeout(function() { 
          $fireball.remove(); 
          clearInterval(explodeIfColision);
      }, 3020);  // 3秒后无论是否达到爆炸程度，都直接消失，强行移除
  
  }, (250));
};
var shoryuken = function(){
  $ken.addClass('shoryuken');
  setTimeout(function() { $ken.addClass('down'); }, 500); 
  setTimeout(function() { $ken.removeClass('shoryuken down'); }, 1000);
};
var jump = function(){
  $ken.addClass('jump');
  setTimeout(function() { $ken.addClass('down'); }, 500); 
  setTimeout(function() { $ken.removeClass('jump down'); }, 1000); 
};
var kneel = function(){
  $ken.addClass('kneel');
};
var walkLeft = function(){
  $ken.addClass('walk').css({ marginLeft:'-=10px' });
};
var walkRight = function(){
  $ken.addClass('walk').css({ marginLeft:'+=10px' });
};

// on click events
$('#a').click(punch);
$('#z').click(kick);
$('#e').click(rkick);
$('#q').click(tatsumaki);
$('#s').click(hadoken);
$('#d').click(shoryuken);
$('#up').click(jump);
$('#down').on('mousedown mouseup', function(e){
    if (e.type == 'mousedown') { kneel(); }
    else { $ken.removeClass('kneel'); }
});
$('#left').on('mousedown mouseup', function(e){
    if (e.type == 'mousedown') { walkLeft(); }
    else { $ken.removeClass('walk'); }
});
$('#right').on('mousedown mouseup', function(e){
    if (e.type == 'mousedown') { walkRight(); }
    else { $ken.removeClass('walk'); }
});

// on keydown events
$(document).on('keydown keyup', function(e) {
    if (e.type == 'keydown') { 

        // s - hadoken
        if (e.keyCode == 83 
            && !$ken.hasClass('tatsumaki') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('punch') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('reversekick')
        ) { 
            hadoken();
        }

        // d - shoryuken
        if (e.keyCode == 68 
            && !$ken.hasClass('tatsumaki')
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('punch') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('reversekick')
            && !$ken.hasClass('jump')
        ) { 
            shoryuken();
        }

        // q - tatsumaki senpuu kyaku
        if (e.keyCode == 81 
            && !$ken.hasClass('tatsumaki') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('punch') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('reversekick')
            && !$ken.hasClass('jump')
        ) { 
            tatsumaki();
        }

        // a - punch
        if (e.keyCode == 65 
            && !$ken.hasClass('punch') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('tatsumaki') 
        ) { 
            punch(); 
        }

        // e - kick
        if (e.keyCode == 90 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('tatsumaki')
        ) { 
            kick(); 
        }

        // r - reverse kick
        if (e.keyCode == 69 
            && !$ken.hasClass('reversekick') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('tatsumaki')
        ) { 
            rkick();
        }

        // up - jump
        if (e.keyCode == 38 
            && !$ken.hasClass('jump') 
            && !$ken.hasClass('reversekick') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('tatsumaki')
        ) { 
            jump();
        }

        // down - kneel
        if (e.keyCode == 40 
            && !$ken.hasClass('kneel') 
            && !$ken.hasClass('jump') 
            && !$ken.hasClass('reversekick') 
            && !$ken.hasClass('kick') 
            && !$ken.hasClass('hadoken') 
            && !$ken.hasClass('shoryuken') 
            && !$ken.hasClass('tatsumaki')
        ) { 
            kneel();
        }
    
    
        // ← flip 
        //if (e.keyCode == 37) $ken.addClass('flip');
        // → unflip 
        //if (e.keyCode == 39) $ken.removeClass('flip');
        // ←← →→ walking
        if (e.keyCode == 37) { walkLeft(); }
        if (e.keyCode == 39) { walkRight(); }
    }
    else { // keyup
        $ken.removeClass('walk kneel');
    }
    return false;
    //console.log(e.keyCode);
});
