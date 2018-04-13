$(document).ready(function () {
  // jQuery is only used for the application front-end and does not
  // perform any data processing

  // Materialize CSS initializers wrap around jQuery
  // These initializers allow sidenav, tabs, modal, and select to
  // be hidden/triggered on events such as button clicks, etc.

  // Hides sidenav by default, button click on menu icon triggers open
  $('.sidenav').sidenav()

  // Allows tabs to be hidden and slideable
  $('.tabs').tabs()

  // Hides modal by default, allows modal to be opened on button click
  $('.modal').modal()

  // Hides select options into a dropdown menu
  $('select').formSelect()
})
