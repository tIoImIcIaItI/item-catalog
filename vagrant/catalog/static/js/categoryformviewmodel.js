/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var CategoryFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(CategoryFormViewModel, FormViewModel);

	document.addEventListener("DOMContentLoaded", function() {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('category-form');
		var formVm = new CategoryFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
