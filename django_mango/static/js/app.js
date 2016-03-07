// Defining the models and collections
var ArticleModel = Backbone.Model.extend({
    idAttribute: "slug",
    urlRoot: '/articles'
});
var ArticleCollection = Backbone.Collection.extend({
    url: '/articles',
    model: ArticleModel
});

var articles = new ArticleCollection;

// Defining the views

// Detail view to show the article details
var ArticleDetailView = Backbone.View.extend({
    model: '',
    el: $("#ArticleViewArea"),
    render: function() {
        var template = _.template($("script.ArticleDetailTemplate").html());
        this.$el.html(template({
            article: this.model.attributes,
        }));
        return this;
    }
});

// View to show random article preview on the header
var RandomArticlePreviewView = Backbone.View.extend({
    model: '',
    el: $("#ArticleViewArea"),
    initialize: function(args) {
        this.render()
    },
    render: function() {
        this.$el.html('')
        var template = _.template($("script.ArticleRandomPreviewTemplate").html());
        this.$el.html(template({
            article: this.model.attributes,
        }));
        return this;
    }
});

// View to display the top 10 blog posts
var ArticleListView = Backbone.View.extend({
    model: ArticleCollection,
    el: $("#ArticleViewArea"),
    initialize: function() {
        this.render();
    },
    render: function() {
        var template = _.template($("script.ArticleTopListTemplate").html());
        this.$el.append(template({
            articles: this.model
        }));
        return this
    }
});


// Defining the router paths
var AppRouter = Backbone.Router.extend({
    routes: {
        "": "index",
        ":slug": "viewArticle",
    }
});

var app_router = new AppRouter;

// route to load the article list view
app_router.on('route:index', function() {
    if(article){
        article = null
        fetch_recommended_articles()
    }

    // Get the preview article
    var preview_article = new ArticleModel()
    preview_article.url = 'articles/preview/'
    preview_article.fetch({
        success: function(model, response, options) {
            var random_article = new RandomArticlePreviewView({
                model: model
            })
        }
    });

    // Fetch the top 10 posts
    articles.fetch({
        success: function(collection, response, options) {
            var blog_view = new ArticleListView({
                model: collection.models
            });
        },
        error: function(){
            $("#ArticleViewArea").html("<b>Not able to reach the server, try again later<b/>")
            $("#AppLoading").removeClass('hidden');
        }
    });
    document.title = "Top 10 Blogs | Mevin Babu"
});

// Route to load the details page
var article = null
app_router.on('route:viewArticle', function(slug) {
    article = new ArticleModel({
        slug: slug
    })

    // Fetch the article to view
    article.fetch({
        success: function(model, response, options) {
            var article_view = new ArticleDetailView({
                model: model,
            })
            article_view.render()
            document.title = model.attributes.title + " | " + model.attributes.author
            fetch_recommended_articles()
        }
    })
});


// make the URLs bookmarkable
Backbone.history.start();

// Hack to fix the backbone same URL bug
$("a.list-group-item").on('click', function(){
    if(Backbone.history.fragment == ''){
        app_router.navigate('/');
        Backbone.history.loadUrl(Backbone.history.fragment);
    }
})