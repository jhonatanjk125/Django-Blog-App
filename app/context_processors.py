def theme(request):
    """Retrieves wether the user is currently in light or dark mode to render the right choice"""
    if 'dark_mode' in request.session:
        dark_mode = request.session.get('dark_mode')
        return {'dark_mode':dark_mode}
    return {'dark_mode': False}