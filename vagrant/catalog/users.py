import json

from flask import make_response, redirect, render_template, request, \
    session as login_session

from database_setup import User, DBSession

session = DBSession()


class UserUtils(object):
    """ Miscellaneous functions for managing the larger authentication process.
    """

    @staticmethod
    def is_authenticated():
        """
        Returns True iff the user's account information has been recorded
        in the active session.
        :rtype: Boolean
        """
        return 'user_id' in login_session

    @staticmethod
    def render_user_template(template_name_or_list, **kwargs):
        """
        Wraps calls to render_template, ensuring that user and authentication
        data is available to templates
        """
        authenticated = UserUtils.is_authenticated()

        if 'authenticated' not in kwargs:
            kwargs['authenticated'] = authenticated

        if 'user_handle' not in kwargs:
            if authenticated:
                kwargs['handle'] = UserUtils.get_user_handle()

        return render_template(template_name_or_list, **kwargs)

    @staticmethod
    def get_user_handle():
        """
        Returns the alias by which we'll refer to the the signed in user.
        This will be an email, or username, or first name, etc. depending
        on the best information available from the 3rd-party user account.
        :rtype: String
        """
        if not UserUtils.is_authenticated():
            return None

        return \
            login_session['username'] \
            if 'username' in login_session and len(
                login_session['username']) > 0 \
            else login_session['email']

    @staticmethod
    def unset_preauthentication_url():
        """
        Clears the record of the page from which 
        the user initiated authentication
        """
        del login_session['return-to-url']

    @staticmethod
    def set_preauthentication_url():
        """
        Records the page from which 
        the user initiated authentication
        """
        login_session['return-to-url'] = request.referrer

    @staticmethod
    def get_preauthentication_url():
        """
        Returns the URL from which 
        the user initiated authentication, or the application root
        :rtype: String
        """
        if 'return-to-url' in login_session:
            url = login_session.get('return-to-url')
            if url:
                return url

        return '/'

    @staticmethod
    def respond_with_preauthentication_url():
        """
        Returns JSON indicating the page from which 
        the user initiated authentication
        """
        response = make_response(
            json.dumps({'redirect': UserUtils.get_preauthentication_url()}),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    @staticmethod
    def return_to_preauthentication_url():
        """
        Redirects to the page from which 
        the user initiated authentication 
        """
        url = UserUtils.get_preauthentication_url()
        UserUtils.unset_preauthentication_url()
        return redirect(url)

    @staticmethod
    def create_user(fields):
        """
        Creates and returns a new user in the data repository given a 
        dictionary containing the user's username, email, and picture
        :rtype: User
        """
        user = User(
            name=fields['username'],
            email=fields['email'],
            picture=fields['picture'])
        session.add(user)
        session.commit()

        return session.query(User).filter_by(email=fields['email']).one()

    @staticmethod
    def try_get_user_by_email(email):
        """
        Retrieves and returns a user by email from the data repository,
        or None if the user is not found
        :type email: String
        :rtype: User
        """
        try:
            return session.query(User).filter_by(email=email).one()
        except:
            return None

    @staticmethod
    def get_authenticated_user_id():
        """
        Returns the user ID value from the current session,
        or None if the user is not signed in
        """
        if 'user_id' in login_session:
            return login_session['user_id']
        else:
            return None
