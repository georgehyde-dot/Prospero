from .boardgamegeek import BGGClient
import json
def call_bgg(method, modifiers):
    bgg = BGGClient()
    kwargs = {modifier_name: modifier_value for modifier_name, modifier_value in modifiers.items()}
    print(kwargs)
    if hasattr(bgg, method):
        method_to_call = getattr(bgg, method)
        #print(method_to_call)
        try:
            response = method_to_call(**kwargs)
            result = {}

            if method == 'game':
                game_name = response.name
                game_data = {
                    'comments': [{'username': comment.commenter, 'comment': comment.comment, 'rating': comment.rating} for comment in response.comments],
                    # Extract other relevant game data here
                    'name': game_name,

                }
                result['game'] = game_data
                


            elif method == 'plays':
                # Extract plays data
                plays_data = {
                    'total_plays': response.plays_count,
                    'players': [player.username for play in response.plays for player in play.players]
                }
                result['plays'] = plays_data

            elif method == 'hot_items':
                # Extract hot items data
                hot_items_data = [{'name': item.name, 'rank': item.rank} for item in response.items]
                result['hot_items'] = hot_items_data

            elif method == 'user':
                user_data = {
                    'id': response.id,
                    'name': response.name,
                    'firstname': response.firstname,
                    # Add other user details here
                }
                result['user'] = user_data
            #print(result)
            
            return result

        except Exception as e:
            return {'error': str(e)}
    else:
        return {'error': 'Invalid method name'}
#Method Name: game, Modifiers: {'game_id': 328687, 'comments': True, 'name': True}    
response = call_bgg('game',{'game_id': 328687, 'comments': True, 'name': True})
with open("usabel.txt", 'a') as file:
    for item in response.items():
        file.write(f'{str(item)}\n')