$(() => {
  'use strict'

  var $menu = $('#main > nav > menu')
  var $doc = $('#main > .documentation')

  var $toggleConstraintButton = $menu.find('.constraint_toggle')

  var $expandables = $('h2.declaration:not(.enum)').filter(function() {
    var $decl = $(this)

    var $def = $decl.next('.definition')

    if ($def.length === 0) {
      // No definition, so this doesn't expand.
      return false
    }

    if ($def.children(':not(.summary)').length === 0) {
      // The defition is there, but has nothing but a summary.
      // Don't expand it.
      return false
    }

    return true
  })

  function toggleConstraintsOn() {
    localStorage.setItem('constraints_on', 'true')
    $toggleConstraintButton.addClass('toggled')

    $doc.removeClass('hide_template_constraints')
  }

  function toggleConstraintsOff() {
    localStorage.setItem('constraints_on', 'false')
    $toggleConstraintButton.removeClass('toggled')

    $doc.addClass('hide_template_constraints')
  }

  $toggleConstraintButton.click(() => {
    if (localStorage.getItem('constraints_on') === 'false') {
      toggleConstraintsOn()
    } else {
      toggleConstraintsOff()
    }
  })

  $expandables.click(function() {
    var $elem = $(this)
    var $elemDef = $elem.next('.definition')

    if ($elem.hasClass('open')) {
      // Close this and all children.
      $elem.add($elemDef.find('.declaration')).removeClass('open')
      $elemDef.add($elemDef.find('.definition')).removeClass('open')
    } else {
      // Open just this one up.
      $elem.addClass('open')
      $elemDef.addClass('open')
    }
  })

  $expandables.addClass('expandable')

  if (localStorage.getItem('constraints_on') === 'false') {
    toggleConstraintsOff()
  }
})
