"Classes made for specific purposes"

import logging
import json
from httpx import HTTPError, Response
from .networking import NetworkClient
from .exceptions import NetworkError, NoResults, AlreadyExists, InvalidArgs, RateLimited
from .utils import convert_post_tags

logger = logging.getLogger(__name__)
default_session = NetworkClient()
class Fetcher:
    """
    Deals with retrieving content in a universal way
    """
    def __init__(self, networkclient = default_session):
        self.endpoint = ""
        self.session = networkclient
        self.type_name = "item"
        self.fetch_limit = 320
        
    def strip_dict_container(self, contained_item) -> list[dict]:
        """
        some requests will have a single dictionary surrounding the list of objects, some wont, so this fixes that and removes the dict if it exists
        """
        try:
            item = contained_item[list(contained_item)[0]]
        except TypeError:
            logger.debug("Dict does not surround objects")
            item = contained_item
        except IndexError:
            logger.debug("No dict container and list empty (most likely no results for fetched items)")
            item = contained_item
        return item
        
    def get(self, get_options:dict, fetch_count:int = 320, return_request:bool = False) -> list | Response:
        """
        Retrieves up to 320 items from the fetcher specified endpoint
        """
        logger.debug(f"get args: '{get_options}' fetch count: '{fetch_count}'")
        
        if fetch_count > 320:
            fetch_count = 320
            logger.debug("Fetch count over limit, reduced to 320")
        
        options = {**get_options, 'limit': fetch_count}
        
        try:
            request = self.session.get(url = self.endpoint, params = options)
            logger.debug(f"request status {request.status_code}")
            request.raise_for_status()
        except HTTPError:
            logger.error("Network error occurred")
            raise NetworkError
        
        decoded_request = self.strip_dict_container(json.loads(request.text))
        if len(decoded_request) < 1:
            logger.warning("Nobody here but us chickens!")
            raise NoResults(f"Request options: {get_options}")
        
        if return_request:
            return request
        return decoded_request
            
    def looped_get(self, get_options:dict, fetch_count:int = 320, fetch_all:bool = False) -> list:
        """
        Bulk fetches items from fetcher specified endpoint.
        Only works with items that have an "id" attribute
        """
        
        initial_fetch = self.get(get_options, fetch_count, False)
        objects_list = initial_fetch
        page = 0
        
        while True:
            last_object_id = initial_fetch[-1]['id']
            page += 1
            logger.debug(f"Fetching page: {page}")
            
            try:
                loop_objects_list = self.get({**get_options, 'page': f"b{last_object_id}"}, 320, False)
            except NoResults:
                if fetch_all:
                    logger.info(f"Fetched {len(loop_objects_list)} {self.type_name}s")
                else:
                    logger.info(f"Failed to fetch all items. Count: {len(loop_objects_list)}")
                break
            
            for item in loop_objects_list:
                if len(objects_list) >= fetch_count and not fetch_all:
                    break
                objects_list.append(item)
                
            if len(objects_list) >= fetch_count and not fetch_all:
                break
        
        if fetch_all:
            logger.info(f"Fetched {len(objects_list)} {self.type_name}s")
        else:
            logger.info(f"Fetched {len(objects_list)} out of {fetch_count} {self.type_name}s")
        return objects_list 
    

class PostCache:
    "No worky, dont use"
    def __init__(self, post_limit = 1000):
        self.post_list = []
        self.post_limit = post_limit
        
    def add_post(self, post):
        if self.search_cache(id=post['id']) != None:
            logger.debug(f"Post {post['id']} already cached")
            return
        
        if len(self.post_list) >= self.post_limit:
            removed_post_id = self.post_list.pop(-1)['id']
            logger.debug(f"Removed post {removed_post_id} from cache. Reason: cache full")
            
        self.post_list.append(post)
        
    def search_cache(self, id = None, tags = None):
        if id == None and tags == None:
            logger.error("No id or tags provided to search for, returning empty list")
            return []
        if id != None and tags == None:
            results = next((item for item in self.post_list if item['id'] == id), None)
        else:
            tag_list = str(tags).split()
            results = []
            for post in self.post_list:
                post = convert_post_tags(post)
                search = list(filter(lambda tag: tag in tag_list, post['all_tags']))
                if search == tag_list: results.append(post)
        return results


class PostHandler(Fetcher):
    def __init__(self, network_client = default_session):
        super().__init__(network_client)
        self.endpoint = "/posts.json"
        self.type_name = "post"
        
    def get_posts(self, tags:str, fetch_count:int = 320, fetch_all:bool = False):
        logger.info(f"Fetching {fetch_count} posts with the tags: '{tags}'")
        if fetch_all or fetch_count <= 320:
            posts = self.get(get_options = {'tags': tags}, fetch_count = fetch_count)
        else:
            posts = self.looped_get(get_options = {'tags': tags}, fetch_count = fetch_count)
        logger.info("Fetch done")
        return posts

    def vote(self, post_id:int, vote:int) -> int:
        endpoint = f"/posts/{post_id}/votes.json"
        if vote not in [1, -1, 0]:
            logger.warn("Invalid vote, must be '1', '-1' or '0'")
            return 0
        
        try:
            request = self.session.post(endpoint, params={'score': vote})
            request.raise_for_status()
        except HTTPError:
            logger.error(f"Failed to upvote post {post_id} due to network error. Request status code: {request.status_code}")
            raise NetworkError
        
        new_score = json.loads(request.text)['our_score']
        logger.info(f"Voted {vote} on post {post_id}. New vote: {new_score}")
        return new_score
    
    def favorite(self, post_id:int, favorite:bool) -> bool:
        if favorite:
            try:
                request = self.session.post("/favorites.json", params={'post_id': post_id})
                request.raise_for_status()
            except HTTPError:
                if request.status_code == 422:
                    logger.warning(f"Post {post_id} already favorited")
                    return True
                raise NetworkError
            
            logger.info(f"Post {post_id} favorited")
            return True
        
        try:
            request = self.session.delete(f"/favorites/{post_id}.json")
            request.raise_for_status()
        except HTTPError:
            logger.error(f"A network error occurred. Request status code: {request.status_code}")
            raise NetworkError
        
        post = self.get({'tags':f'id:{post_id}'})[0]
        return post['is_favorited']
        
    def edit(self, 
                  post_id, 
                  tag_diff: type[str] = None, 
                  source_diff: type[str] = None, 
                  parent_id: type[int] = None, 
                  description: type[str] = None, 
                  rating: type[str] = None, 
                  edit_reason: type[str] = None) -> list[dict]:
        post_data = {}
        if tag_diff != None: post_data = {**post_data, 'post[tag_string_diff]':tag_diff}
        if source_diff != None: post_data = {**post_data, 'post[source_diff]': source_diff}
        if parent_id != None: post_data = {**post_data, 'post[parent_id]': parent_id}
        if description != None: post_data = {**post_data, 'post[description]': description}
        if rating != None: post_data = {**post_data, 'post[rating]': rating}
        if edit_reason != None: post_data = {**post_data, 'post[edit_reason]': edit_reason}
        
        try:
            request = self.session.patch(f"/posts/{post_id}.json", params=post_data)
            request.raise_for_status()
        except HTTPError:
            logger.error(f"A network error occurred. Request status code: {request.status_code}")
            raise NetworkError
        logger.info(f"Edited post {post_id} successfully")
        return [self.strip_dict_container(json.loads(request.text))]
    
    def upload(self, 
                    tags:str, 
                    rating:str, 
                    source:str, 
                    description:str = None, 
                    upload_file = None, 
                    direct_url:str = None, 
                    parent_id:int = None) -> list[dict] | int:
        post_data = {
            'upload[tag_string]': tags,
            'upload[rating]': rating,
            'upload[source]': source
        }
        if description != None: post_data = {**post_data, 'upload[description]': description}
        if parent_id != None: post_data = {**post_data, 'upload[parent_id]': parent_id}
        
        if upload_file != None:
            post_file = {'upload[file]': upload_file}
        elif direct_url != None:
            post_data = {**post_data, 'upload[direct_url]': direct_url}
        else:
            logger.error("Upload failed, no file or direct url given")
            return []
        
        try:
            if upload_file != None:
                request = self.session.post("/uploads.json", data=post_data, files=post_file)
            else:
                request = self.session.post("/uploads.json", data=post_data)
            request.raise_for_status()
        except HTTPError:
            if request.status_code == 412:
                error_status = json.loads(request.text)
                logger.error(f"Upload failed, post already exists. Id: {error_status['post_id']}")
                raise AlreadyExists(int(error_status['post_id']))
            
            logger.error(f"Upload failed, a network error occurred. Request status code: {request.status_code}")
            raise NetworkError
        
        status = json.loads(request.text)
        logger.info(f"Post uploaded successfully! Id: {status['post_id']}")
        try:
            return self.get({'tags': f"id:{status['post_id']}"})
        except NoResults:
            logger.warning("Failed to get post after upload")
            return []


class PoolHandler(Fetcher):
    def __init__(self, network_client = default_session):
        super().__init__(network_client)
        self.endpoint = "/pools.json"
        self.type_name = "pool"
        self.categories = [
            "series",
            "collection"
        ]
        self.order = [
            "name",
            "created_at",
            "updated_at",
            "post_count",
        ]
    
    def filter_args(self, args:dict):
        #? might move this to the utils module
        args_to_be_removed = [] #* this is needed since updating the dict while looping through it causes a RuntimeError
        for arg, arg_value in args.items():
            if arg_value == None:
                args_to_be_removed.append(arg)
                
        for arg in args_to_be_removed:
            args.pop(arg)
        return args
    
    def validate_args(self, args:dict):
        # for use with the create and edit functions
        try:
            if len(args["pool[post_ids][]"]) > 1000:
                logger.warning("Too many posts, limit is 1000")
                raise InvalidArgs
        except KeyError:
            pass
        
        try:
            if args["pool[category]"] not in self.categories:
                logger.warning(f"Category invalid, must be one of the following {str(self.categories)}")
                raise InvalidArgs
        except KeyError:
            pass
        
        try:
            if len(args["pool[name]"]) > 250:
                logger.warning("Name is too long, character limit is 250")
                raise InvalidArgs
        except KeyError:
            pass
        
        try:
            if len(args["pool[description]"]) > 10000:
                logger.warning("Description is too long, character limit is 10000")
        except KeyError:
            pass
        
        try:
            int(args["pool[name]"])
        except ValueError:
            pass
        except KeyError:
            pass
        else:
            logger.warning("Name cannot contain only numbers")
            raise InvalidArgs
        
    def get_pools(self, name_search:str = None,  description_search:str = None, creator_name_search:str = None, search_category:str = "series", search_order:str = "updated_at", fetch_count:int = 320, pool_id:int = None, creator_id:int = None, is_active:bool = None, fetch_all:bool = False) -> list:
        request_args = {"search[name_matches]": name_search, 
                "search[description_matches]": description_search, 
                "search[creator_name]": creator_name_search, 
                "search[category]": search_category, 
                "search[order]": search_order, 
                "search[id]": pool_id, 
                "search[creator_id]": creator_id,
                "search[is_active]": is_active}
        
        
        request_args = self.filter_args(request_args)
            
        if search_category not in self.categories and search_category != "":
            logger.warning(f"Search category invalid, must be one of the following {str(self.categories)}")
            raise InvalidArgs
        if search_order not in self.order and search_order != "":
            logger.warning(f"Search order invalid, must be one of the following {str(self.order)}")
            raise InvalidArgs
        
        if fetch_all or fetch_count <= 320:
            pools = self.get(get_options = request_args, fetch_count = fetch_count)
        else:
            pools = self.looped_get(get_options = request_args, fetch_count = fetch_count, fetch_all = fetch_all)
        logger.info(f"{len(pools)} pools found")
        return pools

    def create(self, name:str, description:str, category:str, post_ids:list[int] = []):
        request_args = {"pool[name]": name, "pool[description]": description, "pool[category]": category}
        if post_ids != []:
            request_args = {**request_args, "pool[post_ids][]": post_ids}
        
        self.validate_args(request_args)
        
        try:
            request = self.session.post(self.endpoint, params = request_args)
            request.raise_for_status()
        except HTTPError:
            if request.status_code == 422:
                status_message = json.loads(request.text)["errors"]
                try:
                    if status_message["name"][0] == "has already been taken":
                        logger.error("Pool name already taken")
                        raise AlreadyExists
                except KeyError:
                    if status_message["creator"][0] == "have reached the hourly limit for this action":
                        logger.error("Rate limited, try again in an hour")
                        raise RateLimited
            else:
                logger.error(f"Failed to create pool, a network error occurred. Request status code: {request.status_code}")
                raise NetworkError
        pool = self.strip_dict_container([json.loads(request.text)])
        logger.info(f"Pool made successfully! id: {pool['id']}")
        return pool
    
    def edit(self, id:int, name:str = None, description:str = None, post_ids:list[int] = None, is_active:bool = None, category:str = None):
        request_args = {"pool[description]": description, "pool[post_ids][]": post_ids, "pool[is_active]": is_active, "pool[category]": category}
        
        request_args = self.filter_args(request_args)
        self.validate_args(request_args)
        
        try:
            request = self.session.put(f"/pools/{id}.json", params = request_args)
            request.raise_for_status()
        except HTTPError:
            #! just going to spit out any errors that happen for now since the site i used to find out the error responses is down i think, i'll figure it out myself later
            logger.error("Unknown error occurred.")
            raise NetworkError(f"Raw response data: {request.text}")
        
        logger.info(f"Edited pool {id} successfully")
        return self.get({"search[id]": id})
    
    def revert(self, id:int, version_id:int):
        """Revert pool to a previous state (may or may not work)"""
        try:
            request = self.session.put(f"/pools/{id}/revert.json", params = {"version_id": version_id})
            request.raise_for_status()
        except HTTPError:
            #! just going to spit out any errors that happen for now since the site i used to find out the error responses is down i think, i'll figure it out myself later
            logger.error("Unknown error occurred.")
            raise NetworkError(f"Raw response data: {request.text}")
        
        logger.info(f"Reverted pool {id} to version {version_id}")
        return self.get({"search[id]": id})
