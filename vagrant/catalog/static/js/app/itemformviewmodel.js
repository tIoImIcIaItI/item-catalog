/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var ItemFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(ItemFormViewModel, FormViewModel);

	document.addEventListener("DOMContentLoaded", function() {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('item-form');
		var formVm = new ItemFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
