class Solution(object):
    def initializeSudoku(self,board):
        done = []
        for i in range(9):
            for j in range(9):
                if board[i][j]!=".":
                    done.append([i,j])
                else:
                    board[i][j] = ['1','2','3','4','5','6','7','8','9']
        self.solveSudoku(board=board, done=done)
    def solveSudoku(self, board, done, before=0):
        for d in range(max(0,80-before)):
            if len(done)<=d:
                print("not one solution")
                pboard(board)
                for i in range(9):
                    for j in range(9):
                        if isinstance(board[i][j],list):
                            board[i][j] = board[i][j][0]
                            done.clear()
                            done.append([i,j])
                            return False
            i,j = done[d]
            v = board[i][j]
            bb = [(i//3)*3,(j//3)*3]
            for c in range(9):
                # if c != j:
                if isinstance(board[i][c],list):
                    if v in board[i][c]:
                        board[i][c].remove(v)
                        if len(board[i][c])==1:
                            board[i][c] = board[i][c][0]
                            done.append([i,c])
                # if c != i:
                if isinstance(board[c][j],list):
                    if v in board[c][j]:
                        board[c][j].remove(v)
                        if len(board[c][j])==1:
                            board[c][j] = board[c][j][0]
                            done.append([c,j])
                boxc = [ bb[0] + (c//3) , bb[1] + (c%3) ]
                ci, cj = boxc
                # if boxc != [i,j]:
                if isinstance(board[ci][cj],list):
                    if v in board[ci][cj]:
                        board[ci][cj].remove(v)
                        if len(board[ci][cj])==1:
                            board[ci][cj] = board[ci][cj][0]
                            done.append([ci,cj])
        pboard(board)


def pboard(board):
    for row in board:
        for column in row:
            if isinstance(column,list): column="."
            print(f"{column} ", end='')
        print("",end='\n')

def getinputsudoku():
    board = []
    for i in range(9):
        board.append([])
        row = str(input(f"Write Rows {i+1}: "))
        "".join(row.split())
        tlist = []
        for j in range(9):
            tlist.append(row[j])
        board[i] = tlist
    error = str(input("error? Y/N: "))
    if error.lower()=="y":
        try:
            i = int(input("row: "))
            j = int(input("column: "))
            change = str(input("change to: "))
            print(i,j,change)
            board[i-1][j-1] = str(change)
        except:
            return None
    return board


s = Solution()

# sudoku = getinputsudoku()
sudoku = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]
sudoku = s.initializeSudoku(sudoku)