from behave import *
from selenium import webdriver

from tests.acceptance.page_model.blog_page import BlogPage
from tests.acceptance.page_model.home_page import HomePage
from tests.acceptance.page_model.new_post_page import NewPostPage

use_step_matcher("re") # it allows our steps to receive arguments from .feature file (test scenario)

@given ("I am on the homepage")
def step_impl(context):
    # it opens a new Chrome Window, so we have to pass the ref to it by the use of context
    context.browser = webdriver.Chrome() # browser should be renamed to driver to make better sense
    page = HomePage(context.browser)
    context.browser.get(page.url)

@given ("I am on the blog page")
def step_impl(context):
    context.browser = webdriver.Chrome()
    page = BlogPage(context.browser)
    context.browser.get(page.url)

@given ("I am on the new post page")
def step_impl(context):
    context.browser = webdriver.Chrome()
    page = NewPostPage(context.browser)
    context.browser.get(page.url)

# by the use of the decorators, we can have functions that have the same names
# code is driven by steps from test scenario .feature, not by the natural workflow
@then ("I am on the blog page")
def step_impl(context): # it gets the updated context
    expected_url = BlogPage(context.browser).url
    assert context.browser.current_url == expected_url

@then ("I am on the homepage")
def step_impl(context): # it gets the updated context
    expected_url = HomePage(context.browser).url
    assert context.browser.current_url == expected_url