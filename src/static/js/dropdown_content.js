function dropDown() {
  document.getElementById('user-menu').classList.toggle('show');
}

window.onclick = function(event) {
  if (!event.target.matches('.drop-button')) {
    let dropdowns = document.getElementsByClassName('dropdown-content');
    let i;
    for (i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

$('#historyButton').click(function(e) {
  $('#modalContainer').fadeIn(500);
  $('.modal').removeClass('transform-out').addClass('transform-in');

  e.preventDefault();
});



$('#modalContainer').click(function(e) {
  if (e.target.id == 'modalContainer') {
    $('#modalContainer').fadeOut(500);
    $('.modal').removeClass('transform-in').addClass('transform-out');

    e.preventDefault();    
  }
});

$('#modalSkip').click(function(e) {
  if (e.target.id == 'modalSkip' || e.target.id == 'modalCloseIcon') {
    $('#modalContainer').fadeOut(500);
    $('.modal').removeClass('transform-in').addClass('transform-out');

    e.preventDefault();
  }
});

function showMessages() {
  $('#modalContainerMessages').fadeIn(500);
  $('.modal-messages').removeClass('transform-out').addClass('transform-in');

}

$('#modalContainerMessages').click(function(e) {
  if (e.target.id == 'modalContainerMessages') {
    $('#modalContainerMessages').fadeOut(500);
    $('.modal-messages').removeClass('transform-in').addClass('transform-out');

    e.preventDefault();
  }
});

$('#modalMessagesSkip').click(function(e) {
  if (e.target.id == 'modalMessagesSkip' || e.target.id == 'modalMessagesCloseIcon') {
    $('#modalContainerMessages').fadeOut(500);
    $('.modal-messages').removeClass('transform-in').addClass('transform-out');

    e.preventDefault();
  }
});
