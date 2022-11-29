function closeMessage(el) {
  el.addClass('is-hidden');
}

$('.js-messageClose').on('click', function(e) {
  closeMessage($(this).closest('.Message'));
});

$('#js-helpMe').on('click', function(e) {
  alert('Help you we will, young padawan');
  closeMessage($(this).closest('.Message'));
});

$('#js-authMe').on('click', function(e) {
  alert('Okelidokeli, requesting data transfer.');
  closeMessage($(this).closest('.Message'));
});

$('#js-showMe').on('click', function(e) {
  alert("You're off to our help section. See you later!");
  closeMessage($(this).closest('.Message'));
});

$(document).ready(function() {
  setTimeout(function() {
    closeMessage($('#js-timer'));
  }, 9000);
});


/* LOGIN - MAIN.JS - dp 2017 */
// LOGIN TABS
$(function () {
  var tab = $(".tabs h3 a");
  tab.on("click", function (event) {
    event.preventDefault();
    tab.removeClass("active");
    $(this).addClass("active");
    tab_content = $(this).attr("href");
    $('div[id$="tab-content"]').removeClass("active");
    $(tab_content).addClass("active");
  });
});

// SLIDESHOW
$(function () {
  $("#slideshow > div:gt(0)").hide();
  setInterval(function () {
    $("#slideshow > div:first")
      .fadeOut(1000)
      .next()
      .fadeIn(1000)
      .end()
      .appendTo("#slideshow");
  }, 3850);
});

// CUSTOM JQUERY FUNCTION FOR SWAPPING CLASSES
(function ($) {
  "use strict";
  $.fn.swapClass = function (remove, add) {
    this.removeClass(remove).addClass(add);
    return this;
  };
})(jQuery);

// SHOW/HIDE PANEL ROUTINE (needs better methods)
// I'll optimize when time permits.
$(function () {
  $(".agree,.forgot, #toggle-terms, .log-in, .sign-up").on(
    "click",
    function (event) {
      event.preventDefault();
      var terms = $(".terms"),
        recovery = $(".recovery"),
        close = $("#toggle-terms"),
        arrow = $(".tabs-content .fa");
      if (
        $(this).hasClass("agree") ||
        $(this).hasClass("log-in") ||
        ($(this).is("#toggle-terms") && terms.hasClass("open"))
      ) {
        if (terms.hasClass("open")) {
          terms.swapClass("open", "closed");
          close.swapClass("open", "closed");
          arrow.swapClass("active", "inactive");
        } else {
          if ($(this).hasClass("log-in")) {
            return;
          }
          terms.swapClass("closed", "open").scrollTop(0);
          close.swapClass("closed", "open");
          arrow.swapClass("inactive", "active");
        }
      } else if (
        $(this).hasClass("forgot") ||
        $(this).hasClass("sign-up") ||
        $(this).is("#toggle-terms")
      ) {
        if (recovery.hasClass("open")) {
          recovery.swapClass("open", "closed");
          close.swapClass("open", "closed");
          arrow.swapClass("active", "inactive");
        } else {
          if ($(this).hasClass("sign-up")) {
            return;
          }
          recovery.swapClass("closed", "open");
          close.swapClass("closed", "open");
          arrow.swapClass("inactive", "active");
        }
      }
    }
  );
});

// DISPLAY MSSG
$(function () {
  $(".recovery .button").on("click", function (event) {
    event.preventDefault();
    $(".recovery .mssg").addClass("animate");
    setTimeout(function () {
      $(".recovery").swapClass("open", "closed");
      $("#toggle-terms").swapClass("open", "closed");
      $(".tabs-content .fa").swapClass("active", "inactive");
      $(".recovery .mssg").removeClass("animate");
    }, 2500);
  });
});

// DISABLE SUBMIT FOR DEMO
$(function () {
  $(".button").on("click", function (event) {
    $(this).stop();
    event.preventDefault();
    return false;
  });
});

// LIGHT OR DARK MODE
const toggleButton = document.querySelector(".dark-light");

toggleButton.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  _run('/usr/share/bigbashview/bcc/shell/setbgcolor.sh "' + document.body.classList.contains('light-mode') + '"');
});



//show the confirmation div
  function customInstall() {
    document.getElementById("confirm").hidden=false
    document.getElementById("customSystem").hidden=true
  }

  function customInstallConfirm() {
    document.getElementById("installConfirm").hidden=false
    document.getElementById("customSystem").hidden=true
    document.getElementById("confirm").hidden=true
  }

  
  //hide the confirmation div
  function confirmNo() {
    document.getElementById("confirm").hidden=true
    document.getElementById("installConfirm").hidden=true
    document.getElementById("customSystem").hidden=false
  }

// Select all checkbox
function selects(){  
    var ele=document.getElementsByName('pkg_rm');  
    for(var i=0; i<ele.length; i++){  
        if(ele[i].type=='checkbox')  
            ele[i].checked=true;  
    }  
}  
function deSelect(){  
    var ele=document.getElementsByName('pkg_rm');  
    for(var i=0; i<ele.length; i++){  
        if(ele[i].type=='checkbox')  
            ele[i].checked=false;  
          
    }  
}   

//Other desktop
popup = {
  init: function(){
    $('figure').click(function(){
      popup.open($(this));
    });
    
    $(document).on('click', '.popup img', function(){
      return false;
    }).on('click', '.popup', function(){
      popup.close();
    })
  },
  open: function($figure) {
    $('.gallery').addClass('pop');
    $popup = $('<div class="popup" />').appendTo($('body'));
    $fig = $figure.clone().appendTo($('.popup'));
    $bg = $('<div class="bg" />').appendTo($('.popup'));
    $close = $('<div class="close"><svg><use xlink:href="#close"></use></svg></div>').appendTo($fig);
    $shadow = $('<div class="shadow" />').appendTo($fig);
    src = $('img', $fig).attr('src');
    $shadow.css({backgroundImage: 'url(' + src + ')'});
    $bg.css({backgroundImage: 'url(' + src + ')'});
    setTimeout(function(){
      $('.popup').addClass('pop');
    }, 10);
  },
  close: function(){
    $('.gallery, .popup').removeClass('pop');
    setTimeout(function(){
      $('.popup').remove()
    }, 100);
  }
}

popup.init()
