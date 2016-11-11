// -----------------------------------------------------------------------------
// Slides
var slideIndex = -1;
var lastSlideIndex = slideIndex;
var slides = [];
var slides_interval = null;

function initSlides() {
  slides = document.getElementsByClassName("slide");
  slideIndex = -1;
  lastSlideIndex = slideIndex;
  if (slides_interval !== null) {
    clearInterval(slides_interval);
    slides_interval = null;
  }

  if (slides.length === 1) {
    slides[0].className = "slide-single";
  } else {
    var i;
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }

    nextSlide();
    slides_interval = setInterval(nextSlide, 18000)
  }
}

function nextSlide() {
  lastSlideIndex = slideIndex;
  slideIndex += 1;
  if (slideIndex >= slides.length) slideIndex = 0;
  slides[slideIndex].style.display = "flex";
  setTimeout(clearLastSlide, 2000);
}

function clearLastSlide() {
  if (lastSlideIndex != -1) slides[lastSlideIndex].style.display = "none";
}

// -----------------------------------------------------------------------------
// Now playing
var playIndex = -1;
var playing = [];
var playing_label = document.getElementsByClassName("playing-label")[0];
var playing_label_width = playing_label.offsetWidth;
var playing_label_height = playing_label.offsetHeight;
var playing_div = document.getElementById("playing");
playing_div.style.width = (632 - playing_label_width) + "px";
playing_div.style.left = (playing_label_width + 16) + "px";
playing_div.style.height = playing_label_height + "px";
var playing_interval = null;

function initPlaying() {
  playing = document.getElementsByClassName("playing");
  playIndex = -1;
  if (playing_interval !== null) {
    clearInterval(playing_interval);
    playing_interval = null;
  }

  if (playing.length > 0) {
    var i;
    for (i = 0; i < playing.length; i++) {
        playing[i].style.width = (632 - playing_label_width) + "px";
    }
  }

  if (playing.length === 1) {
    playing[0].className = "playing-single";
  } else {
    nextPlaying();
    playing_interval = setInterval(nextPlaying, 8000);
  }
}

function nextPlaying() {
  var i;
  playIndex += 1;
  for (i = 0; i < playing.length; i++) {
    playing[i].style.display = "none";
  }
  if (playIndex >= playing.length) playIndex = 0;
  playing[playIndex].style.display = "block";
}

// -----------------------------------------------------------------------------
// Now making
var makeIndex = -1;
var making = [];
var making_label = document.getElementsByClassName("making-label")[0];
var making_label_width = making_label.offsetWidth;
var making_label_height = making_label.offsetHeight;
var making_div = document.getElementById("making");
making_div.style.width = (632 - making_label_width) + "px";
making_div.style.left = (making_label_width + 16) + "px";
making_div.style.height = making_label_height + "px";
var making_interval = null;

function initMake() {
  making = document.getElementsByClassName("making");
  makeIndex = -1;
  if (making_interval !== null) {
    clearInterval(making_interval);
    making_interval = null;
  }

  if (making.length === 1) {
    making[0].className = "making-single";
  } else {
    var i;
    for (i = 0; i < making.length; i++) {
        making[i].style.width = (632 - making_label_width) + "px";
    }

    nextMake();
    making_interval = setInterval(nextMake, 8000);
  }
}

function nextMake() {
  var i;
  makeIndex += 1;
  for (i = 0; i < making.length; i++) {
    making[i].style.display = "none";
  }
  if (makeIndex >= making.length) makeIndex = 0;
  making[makeIndex].style.display = "block";
}

// -----------------------------------------------------------------------------
socket = new WebSocket("ws://" + window.location.host);
socket.onmessage = function(e) {
    console.log(e)
    var i;
    var msg = JSON.parse(e.data);
    if (msg.type == "slides") {
      var slideshow = document.getElementById("slideshow");
      var slide_inner = "";
      for (i = 0; i < msg.text.length; i++) {
        slide_inner = slide_inner + "<figure class=\"slide\"> <img src=" + msg.text[i][0] + " class=\"alignnone size-full wp-image-172\" /> <figcaption>" + msg.text[i][1] + "</figcaption> </figure>";
      }
      slideshow.innerHTML = slide_inner;
      initSlides();
    }
    if (msg.type == "play") {
      var play = document.getElementById("playing");
      var play_inner = "";
      for (i = 0; i < msg.text.length; i++) {
        play_inner = play_inner + "<p class=\"playing\">" + msg.text[i] + "</p>";
      }
      play.innerHTML = play_inner;
      initPlaying();
    }
    if (msg.type == "make") {
      var make = document.getElementById("making");
      var make_inner = "";
      for (i = 0; i < msg.text.length; i++) {
        make_inner = make_inner + "<p class=\"making\">" + msg.text[i] + "</p>";
      }
      make.innerHTML = make_inner;
      initMake();
    }
    if (msg.type == "hello") {
      var hello = document.getElementById("hello");
      hello.innerText = msg.text;
    }
}
