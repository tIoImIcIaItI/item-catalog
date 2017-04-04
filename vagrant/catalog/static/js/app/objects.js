/*globals Object */

(function (global) {
	'use strict';

	// Consolidate steps used to wire up a sub-class's prototype.
	// From what I've gleaned from other's countless online discussions, books, courses, etc.
	// of this matter, this is the most complete set of steps needed to yield sensible answers
	// to all queries about the object's 'identity' and of course provide access
	// to the base class functionality.
	global.subclass = function (sub, base) {

		sub.prototype = Object.create(base.prototype); // inherit a copy of the base class's prototype chain
		sub.prototype.base = base.prototype; // report being derived from the given base class
		sub.prototype.constructor = sub; // report being constructed from this most-specific subclass
	};

	// ReSharper disable once ThisInGlobalContext
}(this));