/*
Javscript file to inject recommended articles in a page
to the page

author: Mevin

How to use
----------
Include the tag where you want the section to load
<div class="row" id="what-to-read-next"></div>

Include the template
{% include "read_next.html"%}

Include the JS library
<script src="/static/js/recommended_article.js"></script>
*/

var CURRENT_PAGE = 1
var MAX_ITEMS = 4

function fetch_recommended_articles() {
    compiled_template = _.template($('#what-to-read-next-template').html())
    var recommendedArticles = new ArticleCollection()
    recommendedArticles.url = '/articles/recommend/'

    // Get the current post the user reading
    // We don't have to show the same post as recommendation
    // hence sending the id of the post and the category to get more relevant ones
    function getUserReadingData() {
        if (article) {
            return {
                current_article: article.attributes.slug,
                category: article.attributes.category_slug,
                page: CURRENT_PAGE
            }
        } else {
            return {
                page: CURRENT_PAGE
            }
        }
    }

    function render_to_template(collection, response, options) {
        $('#what-to-read-next').html('')
        template = compiled_template(collection)
        $('#what-to-read-next').append(template)
        $('span.related-posts-discover-btn').on('click', onSlideChange)
    }

    // On slide change, fetch and display the next 4 set of posts
    function onSlideChange() {
        direction = $(this).attr("data-page")
        direction == 'next' ? ++CURRENT_PAGE : --CURRENT_PAGE
        if (recommendedArticles.length < MAX_ITEMS || CURRENT_PAGE <= 1) {
            CURRENT_PAGE <= 1 ? CURRENT_PAGE = 1 : CURRENT_PAGE--
        }
        recommendedArticles.fetch({
            data: getUserReadingData(),
            processData: true,
            success: render_to_template
        })
        console.log(CURRENT_PAGE)
    }

    // Do the initial fetch of articles
    recommendedArticles.fetch({
        data: getUserReadingData(),
        processData: true,
        success: render_to_template
    });

}
// Automatically load after eveything is loaded in the page
window.onload = fetch_recommended_articles
