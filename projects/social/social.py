import random

class Queue:
    def __init__(self):
        self.storage = []

    def enqueue(self, item):
        self.storage.append(item)

    def dequeue(self):
        return self.storage.pop(0)

    def size(self):
        return len(self.storage)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(num_users):
            self.add_user(user)

    # create a list with all possible friendship combinations
        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users):
                friendships.append((user, friend))

        # shuffle the list, 
        # mutate in place with: random.shuffle(array)

        # or, Fisher-Yates shuffle!
        for idx in range(len(friendships)):
         # randint will give us an integer in this range, inclusive (includes last number)
            rand_idx = random.randint(0, len(friendships) - 1)  
            # I think this syntax for swapping items is sweet
            friendships[idx], friendships[rand_idx] = friendships[rand_idx], friendships[idx]

        # then grab the first N elements from the list.
        total_friendships = num_users * avg_friendships
        pairs_needed = total_friendships // 2 # bc add_friendship makes 2 at a time
        random_friendships = friendships[:pairs_needed]

        # Create friendships
        for friendship in random_friendships:
            self.add_friendship(friendship[0], friendship[1])

    def populate_graph_linear(self, num_users, avg_friendships):
        """
        just keep getting "random" friendships and if they've already been added, 
        just find another pair? no need to make full set of all possible friends and 
        just run til we hit required # of friendships
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user_id in range(num_users):
            self.add_user(user_id)

        total_friendships = num_users * avg_friendships

        friendships_made = 0 
        failures = 9

        while friendships_made < total_friendships:
            user_id = random.randint(1,self.last_id)
            friend_id = random.randint(1,self.last_id)

            
            # what if the ids are the same?  --> Use condiitonal but where?
            # what if we've already made this friendship? --> Use conditional but where? 

            if user_id != friend_id and friend_id not in self.friendships[user_id]:
                self.add_friendship(user_id,friend_id)
                friendships_made += 1
            else:
                failures += 1



    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.

        Shortest path --> We have to do a BFS
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = Queue()
        path = [user_id]
        q.enqueue(path)

        while q.size() > 0:
            current_path = q.dequeue()
            current_user = current_path[-1]

            if current_user not in visited:
                visited[current_user] = current_path
                friends = self.friendships[current_user]

                for friend in friends:
                    path_copy = current_path[:]
                    path_copy.append(friend)
                    q.enqueue(path_copy)


        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    #sg.populate_graph(10, 2) This already works but what happens
    sg.populate_graph(1000,5)
    print(sg.friendships[1])
    connections = sg.get_all_social_paths(1)
    print(len(connections)-1)

    total_paths = 0
    for friend_id in connections:
        total_paths += len(connections[friend_id])

    average_path_length = total_paths / len(connections)

    print("Average path length: ", average_path_length)