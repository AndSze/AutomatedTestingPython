from behave import *

from tests.acceptance.page_model.base_page import BasePage
from tests.acceptance.page_model.new_post_page import NewPostPage

use_step_matcher("re") # it allows our steps to receive arguments from .feature file (test scenario)

# "(.*)" group regex . means any character, * means any number of expresions, but they have to be in quotation marks
# then the regex from "(.*)" will be passed to link_id (this is a feature from "re" user step matcher
# regular expressions matcher
@when('I click on the "(.*)" link')
def step_impl(context, link_text):
    page = BasePage(context.browser)
    links = page.navigation

    maching_links = [l for l in links if l.text == link_text]

    if len(maching_links) > 0:
        maching_links[0].click()
    else:
        raise RuntimeError()

@when('I enter "(.*)" in the "(.*)" field')
def step_impl(context, content, field_name):
    page = NewPostPage(context.browser)
    page.form_field(field_name).send_keys(content)

@when('I press the submit button')
def step_impl(context):
    page = NewPostPage(context.browser)
    page.submit_button.click()
