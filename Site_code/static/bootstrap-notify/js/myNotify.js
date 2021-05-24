"use strict";

function notifySuccess(text)
{
  if(text == undefined)
  {
    text = ""
  }
  $.notify(
    {
      // options
      //icon: 'fas fa-times',
      title: '<b>Success:</b>',
      message: text,
    },
    {
      // settings
      element: 'body',
      type: "success",
      allow_dismiss: true,
      newest_on_top: true,
      placement:
      {
        from: "top",
        align: "center"
      },
      offset:
      {
        x: 20,
        y: 80,
      },
      delay: 5000,
      mouse_over: 'pause',
      icon_type: 'class',
    });
}

function notifyInfo(text)
{
  $.notify(
    {
      // options
      //icon: 'fas fa-times',
      title: '<b>Info:</b>',
      message: text,
    },
    {
      // settings
      element: 'body',
      type: "info",
      allow_dismiss: true,
      newest_on_top: true,
      placement:
      {
        from: "top",
        align: "center"
      },
      offset:
      {
        x: 20,
        y: 80,
      },
      delay: 5000,
      mouse_over: 'pause',
      icon_type: 'class',
    });
}

function notifyWarning(text)
{
  $.notify(
    {
      // options
      //icon: 'fas fa-times',
      title: '<b>Warning:</b>',
      message: text,
    },
    {
      // settings
      element: 'body',
      type: "warning",
      allow_dismiss: true,
      newest_on_top: true,
      placement:
      {
        from: "top",
        align: "center"
      },
      offset:
      {
        x: 20,
        y: 80,
      },
      delay: 5000,
      mouse_over: 'pause',
      icon_type: 'class',
    });
}

function notifyDanger(text)
{
  $.notify(
    {
      // options
      //icon: 'fas fa-times',
      title: '<b>Error:</b>',
      message: text,
    },
    {
      // settings
      element: 'body',
      type: "danger",
      allow_dismiss: true,
      newest_on_top: true,
      placement:
      {
        from: "top",
        align: "center"
      },
      offset:
      {
        x: 20,
        y: 80,
      },
      delay: 5000,
      mouse_over: 'pause',
      icon_type: 'class',
    });
  }
