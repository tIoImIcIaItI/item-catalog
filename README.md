# Item Catalog Submission

## Project Description

 A web application that provides a list of items within a variety of categories, and integrates third party user registration and authentication.

## Reviewing the Code

The [`vagrant/catalog/`](vagrant/catalog/) folder contains the server-side (Python) application code.
The [`vagrant/catalog/templates`](vagrant/catalog/templates) folder contains the server-side (Jinja2) HTML template files.
The [`vagrant/catalog/static/`](vagrant/catalog/static/) folder contains the custom client-side (JavaScript) application code and static assets, as well as, vendor libraries and assets.

3rd-party components and frameworks are used as follows.

- Flask is used to serve the HTTP endpoints.
- SQLAlchemy provides the data store API.
- UIKit provides foundational styling and utility CSS classes (ex. alerts, error styling).
- Font Awesome provides scalable icons/glyphs.
- jQuery 3 is used only as a dependency of UIKit.

## Building the App

All files needed to run the application have been prepared and are included in the distribution.
A pre-populated database is provided also.

## Running the App

1. Install Vagrant and VirtualBox, then launch the Vagrant VM (`vagrant up`).

2. Within the VM, run [`catalog/project.py`](vagrant/catalog/project.py) with a Python 2.7 interpreter.

3. Browse to [`http://localhost:5000/`](http://localhost:5000/) in a modern web browser.

## Using the App

The user is initially presented with a list of all categories. Clicking a category presents the details of that categroy, notably the list of associated items. Clicking an item presents its details.

Authentication and user account details are managed via Google's services.

### Business Rules (Application Logic)

#### Functionality for Non-authenticated Users
- View all categories and items
- Sign up and sign in

#### Additional Functionality for Authenticated Users
- Create categories and items
- Edit categories and items they created
- Delete empty categories they created (i.e. those with no associated items) 
- Delete items they created
- Sign out

### Validation

Form input validation occurs on input, change, blur and submit.
Each form input will change color and display an error message if validation fails.
Aria attributes are used to mark invalid fields.
Browsers that do not block invalid form submittal will instead display an alert.
All browsers will show validation errors if an invalid form submit is attempted.

### Accessibility

Aria attributes and HTML semantic elements have been used throughout, for both static and dynamic content.
Error conditions and user alerts are announced via the aria `alert` role.
Contrast has been verified sufficient.
Visual states, icons, images, etc. are accessibly labeled.
Tab order and inclusion has been managed such that only and all interactive elements are navigable.
Interactive elements are of a minimum size.
Microdata has been added to rendered items for search engine and other automated parsers.

### Error Handling

For the HTML endpoints, recoverable errors or user issues will display an alert banner, marked up with aria.

For the JSON endpoints, HTTP error codes are returned appropriately.

### Known Issues

- There are no limits on the number of categories or items displayed (ex. paging very many items).

## API (JSON) Endpoints

The following API endpoints provide access to category and item data in JSON format.
User account details are not provided.

- GET	`/api/categories/`

	Example: [`/api/categories/`](http://localhost:5000/api/categories/)

- GET	`/api/categories/<int:category_id>/`

	Example: [`/api/categories/1`](http://localhost:5000/api/categories/1)

- GET	`/api/categories/<int:category_id>/items/`

	Example: [`/api/categories/1/items`](http://localhost:5000/api/categories/1/items)

- GET	`/api/categories/<int:category_id>/items/<int:item_id>/`

	Example: [`/api/categories/1/items/1`](http://localhost:5000/api/categories/1/items/1)

## HTML Endpoints:

The following endpoints serve the application's HTML interface.

- GET, POST	`/categories/create`

	Example: [`/categories/create`](http://localhost:5000/categories/create)

- GET	`/`, `/categories/`

	Example: [`/categories/`](http://localhost:5000/categories/)

- GET	`/categories/<int:category_id>/`

	Example: [`/categories/1`](http://localhost:5000/categories/1)

- GET, POST	`/categories/<int:category_id>/update`

	Example: [`/categories/1/update`](http://localhost:5000/categories/1/update)

- GET, POST	`/categories/<int:category_id>/delete`

	Example: [`/categories/1/delete`](http://localhost:5000/categories/1/delete)


- GET, POST	`/categories/<int:category_id>/items/create`

	Example: [`/categories/1/items/create`](http://localhost:5000/categories/1/items/create)

- GET	`/categories/<int:category_id>/items/<int:item_id>/`

	Example: [`/categories/1/items/1/`](http://localhost:5000/categories/1/items/1/)

- GET, POST	`/categories/<int:category_id>/items/<int:item_id>/edit`

	Example: [`/categories/1/items/1/edit`](http://localhost:5000/categories/1/items/1/edit)

- GET, POST	`/categories/<int:category_id>/items/<int:item_id>/delete`

	Example: [`/categories/1/items/1/delete`](http://localhost:5000/categories/1/items/1/delete)


## Attributions

The client-side forms framework was carried forward from my [Meet-Up Event Planner](https://github.com/tIoImIcIaItI/Meet-Up-Event-Planner.git) Udacity project.

The following 3rd-party sources were used in building the app and/or its execution.

### Source Code

- Google Authentication: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/0041345408/modules/348776022975461/lessons/3967218625/concepts/39518891870923#)
- Input Dirty Class:  [Google](https://developers.google.com/web/fundamentals/design-and-ui/input/forms/provide-real-time-validation?hl=en)
- Element.remove(): [Stack Overflow](http://stackoverflow.com/questions/3387427/remove-element-by-id)
- Element.prependChild(): [CallMeNick](http://callmenick.com/post/prepend-child-javascript)
- insertAfter(): [Stack Overflow](http://stackoverflow.com/a/4793630/6452184)
- Array.includes(): [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes)
- Standard Polyfills: [MDN](https://developer.mozilla.org)
- Random Number Utilities: [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random)
