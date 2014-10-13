require 'jasmine-given'

describe "the dashboard", ->
  describe "visiting the home page", ->
    Given -> browser.get "/"

    describe "click on rules", ->
      # Given -> element(By.model("credentials.username")).sendKeys "Ralph"
      # Given -> element(By.model("credentials.password")).sendKeys "Wiggum"
      When  -> element(By.sometthing('a[href="/rules"]')).click()
      Then  -> expect(element(By.binding("message")).getText()).toEqual("Mouse Over these images to see a directive at work")
