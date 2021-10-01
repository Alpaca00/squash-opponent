Feature: user login
  @fixture.browser.chrome
  Scenario: can user login
     Given launch chrome browser
      When open home page at opponent web application of internationalization UA
        Then I will see the account details
          And close browser

  @slow
  @fixture.browser.chrome
  Scenario: input incorrect login
    Given launch chrome browser and execute steps from scenario can user login, I get Given and When
      When I enter valid email and invalid password "qwerty"
      Then I will see flash message about "Invalid password." at login page
