from celery import shared_task
from wordcloud import WordCloud
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def import_word_cloud(full_text):
    # Generate a word cloud image
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = None, 
                min_font_size = 10).generate(full_text)

    # Plot the WordCloud image                        
    
    logger.info('About to save')
    visualize_path = os.path.join(settings.MEDIA_ROOT, 'visualize')
    logger.info(f'Path is {visualize_path}')
    os.makedirs(visualize_path, exist_ok=True)

    # Save the image in the media directory
    wordcloud_image_path = os.path.join(visualize_path, 'wordcloud.png')
    wordcloud.to_file(wordcloud_image_path)
    return wordcloud_image_path