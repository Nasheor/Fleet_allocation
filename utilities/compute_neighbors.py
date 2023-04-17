import math

def divide_and_compute_neighbors(n, k):
    def divide_grid():
        cells_per_community = (n * n) // k
        community_width = math.isqrt(cells_per_community)
        community_height = cells_per_community // community_width

        num_communities_row_col = int(math.sqrt(k))

        communities = []
        for i in range(num_communities_row_col):
            for j in range(num_communities_row_col):
                top_left_x = i * community_width
                top_left_y = j * community_height
                communities.append(((top_left_x, top_left_y), (top_left_x + community_width - 1, top_left_y + community_height - 1)))

        return communities, num_communities_row_col

    def get_neighbors_with_diagonal(communities, num_communities_row_col):
        neighbors = {}

        for i in range(num_communities_row_col):
            for j in range(num_communities_row_col):
                community_index = i * num_communities_row_col + j
                community_neighbors = []

                directions = [
                    (-1, 0),  # North
                    (1, 0),   # South
                    (0, -1),  # West
                    (0, 1),   # East
                    (-1, -1), # North-West
                    (-1, 1),  # North-East
                    (1, -1),  # South-West
                    (1, 1),   # South-East
                ]

                for direction in directions:
                    neighbor_i = i + direction[0]
                    neighbor_j = j + direction[1]

                    if 0 <= neighbor_i < num_communities_row_col and 0 <= neighbor_j < num_communities_row_col:
                        neighbor_index = neighbor_i * num_communities_row_col + neighbor_j
                        community_neighbors.append(neighbor_index+1)

                neighbors[community_index+1] = community_neighbors

        return neighbors

    communities, num_communities_row_col = divide_grid()
    neighbors = get_neighbors_with_diagonal(communities, num_communities_row_col)

    return communities, neighbors

# Testing with a grid size 10000 and 16 communities
# grid_size = 10000
# num_communities = 16
#
# communities, neighbors = divide_and_compute_neighbors(grid_size, num_communities)
#
# input_file = '../ride_sharing_framework/2_Instances/Instance_to_solve/d_metropolis.in'
# print(neighbors)
# # Open the file in append mode
# with open(input_file, "a") as file:
#     # Write data to the file
#     for i, community_neighbors in neighbors.items():
#         file.write(f"{' '.join(str(x) for x in community_neighbors)}\n")
