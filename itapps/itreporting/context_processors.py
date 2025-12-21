"""
Context processors for making data available to all templates
"""
from itreporting.services import NewsService


def news_feed(request):
    """
    Context processor to add latest news to all templates
    """
    news_service = NewsService()
    news_articles = news_service.get_latest_news(limit=5)  # Get 5 articles for sidebar
    
    return {
        'news_articles': news_articles,
    }

