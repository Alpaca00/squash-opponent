Feature: User login
  @ua
  @fixture.browser.chrome
  Scenario: Can user login
     Given Launch chrome browser
      When Open home page at opponent web application of internationalization UA
        Then I will see the account details
          And Close browser

  @ua
  @fixture.browser.chrome
  Scenario: Input incorrect login
    Given Launch chrome browser and execute steps from scenario can user login, I get Given and When
      When I enter valid email and invalid password "qwerty"
      Then I will see flash message about "Invalid password." at login page
