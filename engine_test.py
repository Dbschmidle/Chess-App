"""
Unit testing for the Engine.py file.

Tests should be written BEFORE writting the method code
"""

import src

def main():
    a, b, c = test_convertToRankFile()
    printPassed(a, b, c)
    a, b, c = test_convertToChessNotation()
    printPassed(a, b, c)


def printPassed(fname: str, numPassed: int, numTests: int):
    print(fname +": "+ str(numPassed)+"/"+str(numTests)+" tests passed.")


def test_convertToRankFile() -> tuple[str, int, int]:
    fname = "convertToRankFile"
    gamestate = src.GameState()
    m = src.Move((6, 4), (4, 4), gamestate.board)
    
    test_inputs = {
        0: [6, 4],
        1: [4, 4],
        2: [0, 0]
    }
    
    expected_outputs = {
        0: "e2",
        1: "e4",
        2: "a8"
    }
    
    passed = 0
    numTests = len(expected_outputs)
    
    
    for testNum in test_inputs:
        actual_output = m.convertToRankFile(test_inputs[testNum][0], test_inputs[testNum][1])
        
        if (actual_output == expected_outputs[testNum]):
            passed += 1
            
        else:
            print("Test #"+str(testNum)+" failed. \n\tExpected: "+str(expected_outputs[testNum])+" \n\tActual: "+actual_output)
            
    return fname, passed, numTests
    

def test_convertToChessNotation() -> tuple[str, int, int]:
    fname = "convertToChessNotation"
    gamestate = src.GameState()
    m = src.Move((6, 4), (4, 4), gamestate.board)
    
    test_inputs = {
        0: [[6, 4], [4, 4]],
        1: [[1, 0], [3, 0]]
    }
    
    expected_outputs = {
        0: "e2e4",
        1: "a7a5",
    }
    
    passed = 0
    numTests = len(expected_outputs)
    
    
    for testNum in test_inputs:
        m.fromRow = test_inputs[testNum][0][0]
        m.fromCol = test_inputs[testNum][0][1]
        m.toRow = test_inputs[testNum][1][0]
        m.toCol = test_inputs[testNum][1][1]
        
        actual_output = m.convertToChessNotation()
        
        if (actual_output == expected_outputs[testNum]):
            passed += 1
            
        else:
            print("\""+fname+"\""+ ": Test "+str(testNum)+" failed. \n\tExpected: "+str(expected_outputs[testNum])+" \n\tActual: "+actual_output)
            
    return fname, passed, numTests

    
if __name__ == "__main__":
    main()