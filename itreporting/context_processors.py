"""
Context processors for making data available to all templates
"""
from itreporting.services import NewsService
import logging

logger = logging.getLogger(__name__)


def news_feed(request):
    """
    Context processor to add latest news to all templates
    """
    try:
        news_service = NewsService()
        news_articles = news_service.get_latest_news(limit=5)  # Get 5 articles for sidebar
    except Exception as e:
        # If news service fails, return empty list to prevent 500 errors
        logger.warning(f"News service failed: {str(e)}")
        news_articles = []
    
    return {
        'news_articles': news_articles,
    }

