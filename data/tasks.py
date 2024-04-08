from data.models import SearchLog, Game, Play, User, Comment, Rating, HotItem
import json
from celery import shared_task
from datetime import date
import logging
logger = logging.getLogger(__name__)

@shared_task
def process_search_log(search_log_id):
    try:
        logger.info(f"It got this far 1")
        search_log = SearchLog.objects.get(id=search_log_id)
        request_data = json.loads(search_log.search_request)
        method = request_data.get('method')
        logger.info(f"The method is {method}")
        game_id = request_data.get('game_id')
        
        

        if method == 'hot_items':
            process_hot_items(search_log.search_response)
        elif method == 'game':
            logger.info("Processing game")
            process_games(search_log.search_response, game_id)
        elif method == 'play':
            process_plays(search_log.search_response, game_id)
        elif method == 'user':
            process_user(search_log.search_response)
        else: 
            logger.info("No Method found")
            return False
    except Exception as e:
        logger.info(f"Exception {e}\nSearch Log ID {search_log_id}")


def process_hot_items(response):
    hot_items_data = json.loads(response).get('hot_items', [])
    current_date = date.today()

    for item in hot_items_data:
        game_name = item.get('name')
        rank = item.get('rank')

        # Get or create a game instance
        game, created = Game.objects.get_or_create(game_name=game_name)

        # Check if a HotItem for this game already exists for today
        hot_item, created = HotItem.objects.get_or_create(
            game=game,
            date_collected=current_date,
            defaults={'rank': rank}  # Used only when creating a new instance
        )

        # Update the rank if the hot item already existed
        if not created:
            hot_item.rank = rank
            hot_item.save()

def process_games(game_data, game_id):
    game_json = json.loads(game_data)
    # logger.info(f'Game JSON: {game_json}')
    game_name = game_json['game']['name']
    logger.info(game_name)
    game, created = Game.objects.get_or_create(game_name=game_name,game_id=game_id )

    for comment_data in game_json['game']['comments']:
        username = comment_data['username']
        comment_text = comment_data['comment']
        rating_value = comment_data['rating']
        logger.info(f"Comment Data: {comment_text}")

        if not username or not comment_text:
            # Skip processing this comment if essential information is missing
            continue
        logger.info(f'Trying to create User {username}')
        user, user_created = User.objects.get_or_create(username=username)
        user.save()
        # Create or update the comment
        logger.info(f'Trying to create Comment {comment_text}')
        comment, comment_created = Comment.objects.get_or_create(username=username, game=game, comment=comment_text, source='BGG')
        
        comment.save()
        logger.info(f"Comment saved? {comment_text}")

        # Process rating if it's a valid number
        if rating_value and rating_value != "n/a":
            logger.info("Adding Rating")
            rating, rating_created = Rating.objects.get_or_create(username=username, game=game, rating=rating_value, comment=comment_text)
            rating.save()
            logger.info(f"Rating Save {rating}")
    # Save the game
    game.save()
    return game, comment, rating
def process_plays(search_response, game_id):
    response_data = json.loads(search_response)
    players = response_data.get('plays', {}).get('players', [])

    game = Game.objects.get(game_id=game_id)

    for player_name in players:
        if player_name: 
            user, _ = User.objects.get_or_create(username=player_name)
            Play.objects.create(user=user, game=game)


def process_user(response):
    # Implementation for processing user data
    return


def parse_comments():
    ...