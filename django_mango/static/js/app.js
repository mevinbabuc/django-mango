/*
Shared storage, can be moved to another file
when this becomes bigger
*/
articleStorage = {
    data: {
        articles: {},
        active: false,
        query: null
    },
    store: function(data){
        this.data.articles = data
    },
    get: function(){
        return this.articles
    }
}

// Defining the view
var blogIndexView = Vue.extend({
    template: '#blog-list-view-area',
    components: {
        topArticles: topArticleListComponent,
        randomPreview: randomPreviewArticleComponent,
        recommendArticle: recommendedArticleComponent
    }
});

var blogDetailView = Vue.extend({
    template: '#blog-detail-view-area',
    components: {
        articleDetail: articleDetailComponent,
        recommendArticle: recommendedArticleComponent
    },
    route: {
        // Reuse the component by refreshing the data
        canReuse: false,
    },
});

var blogSearchView = Vue.extend({
    template: '#blog-search-view-area',
    components: {
        topArticles: topArticleListComponent,
        recommendArticle: recommendedArticleComponent
    }
})

// Initializing and defining the router
var router = new VueRouter({});
router.map({
    '/': {
        name: 'index',
        component: blogIndexView,
    },
    '/:slug': {
        name: 'detail',
        component: blogDetailView,
    },
    '/search': {
        name: 'search',
        component: blogSearchView,
    }
});

router.beforeEach(function (transition) {
    // After each route change, take the user to the top of the page
    window.scrollTo(0, 0)
    transition.next()
})

var App = Vue.extend({})
router.start(App, '#app')