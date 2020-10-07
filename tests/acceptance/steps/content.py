from behave import *

from tests.acceptance.page_model.base_page import BasePage
from tests.acceptance.page_model.blog_page import BlogPage

use_step_matcher("re") # coming from behave library

@then("There is a title shown on the page")
def step_impl(context):
    page = BasePage(context.browser)
    assert page.title.is_displayed()


#@step - means that a step can be used as then/when etc.
@then('The title tag has content "(.*)"')
def step_impl(context, content):
    page = BasePage(context.browser)
    assert page.title.text == content


@then("I can see there is a post section on the page")
def step_impl(context):
    page = BlogPage(context.browser)
    assert page.posts_section.is_displayed()


@then('I can see there is a post with title "(.*)" in the post section')
def step_impl(context, title):
    page = BlogPage(context.browser)
    posts_with_title = [post for post in page.posts if post.text == title]

    assert len(posts_with_title) > 0
    # all evaluates to true if all elements in a list are displayed
    # any evaluates to true if any element from a list is displayed
    assert all([post.is_displayed() for post in posts_with_title])