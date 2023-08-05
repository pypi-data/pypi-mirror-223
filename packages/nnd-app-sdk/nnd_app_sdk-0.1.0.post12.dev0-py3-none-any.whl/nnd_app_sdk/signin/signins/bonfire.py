from nnd_app_sdk.signin.base import SignInBase


class BonfireSignIn(SignInBase):
    domain = "bonfire.com"

    def domain_sign_in(self):
        self.driver.get("https://pd.bonfire.com/login/")

        email = self.wait_for(
            "/html/body/div/div/section/ui-view/div/div/section/form/div[1]/input"
        )
        email.send_keys(self.credentials.username)

        password = self.wait_for(
            "/html/body/div/div/section/ui-view/div/div/section/form/div[2]/input"
        )
        password.send_keys(self.credentials.password)

        sign_in_button = self.wait_for(
            "/html/body/div/div/section/ui-view/div/div/section/form/div[3]/div[2]/button"
        )
        sign_in_button.click()

        # wait for production header to load, in order to make sure that cookies have
        # been loaded
        dashboard_header = self.wait_for(
            "/html/body/div/div/section/ui-view/div/header/div/div[1]/a/h1"
        )
        assert dashboard_header.text == "Production.Dashboard"
