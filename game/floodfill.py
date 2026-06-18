from collections import deque

from settings import MIN_MATCH, cols_for_row


class FloodFill:

    @staticmethod
    def find_color_group(board, start_row, start_col):

        start = board.get(start_row, start_col)

        if start is None:
            return []

        target_color = start.color
        visited = set()
        q = deque([(start_row, start_col)])
        result = []

        while q:
            row, col = q.popleft()

            if (row, col) in visited:
                continue

            visited.add((row, col))

            bubble = board.get(row, col)

            if bubble is None or bubble.color != target_color:
                continue

            result.append((row, col))

            for nr, nc in board.neighbors(row, col):
                q.append((nr, nc))

        return result

    @staticmethod
    def remove_group(board, cells):

        for row, col in cells:
            board.remove(row, col)

    @staticmethod
    def find_connected_to_ceiling(board):

        """천장(0행)에 직접 붙은 공에서만 연결을 탐색."""

        visited = set()
        q = deque()

        for col in range(cols_for_row(0)):
            if board.get(0, col):
                q.append((0, col))

        while q:
            row, col = q.popleft()

            if (row, col) in visited:
                continue

            visited.add((row, col))

            for nr, nc in board.neighbors(row, col):
                if board.get(nr, nc) is not None:
                    q.append((nr, nc))

        return visited

    @staticmethod
    def find_floating_cells(board):

        connected = FloodFill.find_connected_to_ceiling(board)
        floating = []

        for row in range(len(board.grid)):
            for col in range(cols_for_row(row)):
                if board.get(row, col) is None:
                    continue

                if (row, col) not in connected:
                    floating.append((row, col))

        return floating

    @staticmethod
    def remove_floating_once(board):

        floating = FloodFill.find_floating_cells(board)

        for row, col in floating:
            board.remove(row, col)

        return len(floating)

    @staticmethod
    def remove_all_floating(board):

        """천장과 끊긴 블록(매달린 공)을 연쇄적으로 제거."""

        total = 0

        while True:
            n = FloodFill.remove_floating_once(board)

            if n == 0:
                break

            total += n

        return total

    @staticmethod
    def resolve_turn(board, row, col):

        group = FloodFill.find_color_group(
            board,
            row,
            col,
        )

        matched_count = 0
        floating_count = 0

        if len(group) >= MIN_MATCH:
            matched_count = len(group)
            FloodFill.remove_group(board, group)
            floating_count = FloodFill.remove_all_floating(board)

        return matched_count, floating_count
