
import src

def main():
    toChessNotation()


def toChessNotation():
    m = src.Move((6, 4), (4, 4), None)
    print(m.convertToChessNotation())
        
    
    
if __name__ == "__main__":
    main()