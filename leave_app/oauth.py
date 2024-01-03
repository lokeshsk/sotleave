from flask import request
from O365 import Account


@route('/stepone')
def auth_step_one():
    # callback = absolute url to auth_step_two_callback() page, https://domain.tld/steptwo
    callback = url_for('auth_step_two_callback', _external=True)  # Flask example

    account = Account(credentials)
    url, state = account.con.get_authorization_url(requested_scopes=my_scopes,
                                                   redirect_uri=callback)

    # the state must be saved somewhere as it will be needed later
    my_db.store_state(state) # example...

    return redirect(url)

@route('/steptwo')
def auth_step_two_callback():
    account = Account(credentials)

    # retreive the state saved in auth_step_one
    my_saved_state = my_db.get_state()  # example...

    # rebuild the redirect_uri used in auth_step_one
    callback = 'my absolute url to auth_step_two_callback'

    # get the request URL of the page which will include additional auth information
    # Example request: /steptwo?code=abc123&state=xyz456
    requested_url = request.url  # uses Flask's request() method

    result = account.con.request_token(requested_url,
                                       state=my_saved_state,
                                       redirect_uri=callback)
    # if result is True, then authentication was succesful
    #  and the auth token is stored in the token backend
    if result:
        return render_template('auth_complete.html')