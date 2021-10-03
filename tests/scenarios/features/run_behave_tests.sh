
#behave --tags=fixture.browser.chrome --tags=ua tests/scenarios/features/opponent_app_user_login.feature
behave --define hidden=headless --tags=fixture.browser.chrome --tags=ua tests/scenarios/features/*.feature
#behave --lang-list
#behave --help
