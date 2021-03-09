import unittest

from main import main

class TestCommandParsing(unittest.TestCase):
    def test_getFirstCommandWorksOnSimpleStrings(self):
        command, newData = main.getFirstCommandFromData(b'QUERY: A1\n')
        self.assertEqual(command, b'QUERY: A1')
        self.assertEqual(newData, b'')

        command, newData = main.getFirstCommandFromData(b'BUY: A1\n')
        self.assertEqual(command, b'BUY: A1')
        self.assertEqual(newData, b'')

        command, newData = main.getFirstCommandFromData(b'RESERVE: A1\n')
        self.assertEqual(command, b'RESERVE: A1')
        self.assertEqual(newData, b'')

        #This function shouldnt care if the commands are valid
        command, newData = main.getFirstCommandFromData(b'ARBITRARY: A1\n')
        self.assertEqual(command, b'ARBITRARY: A1')
        self.assertEqual(newData, b'')

        command, newData = main.getFirstCommandFromData(b'MALFORMED{}[ssafafasf\n')
        self.assertEqual(command, b'MALFORMED{}[ssafafasf')
        self.assertEqual(newData, b'')

    def test_getFirstCommandWorksWhenRepeated(self):
        inData = b'QUERY: A1\nRESERVE: A1\nBUY: A1\n'
        command, newData = main.getFirstCommandFromData(inData)
        self.assertEqual(command, b'QUERY: A1')
        self.assertEqual(newData, b'RESERVE: A1\nBUY: A1\n')
        inData = newData

        command, newData = main.getFirstCommandFromData(inData)
        self.assertEqual(command, b'RESERVE: A1')
        self.assertEqual(newData, b'BUY: A1\n')
        inData = newData

        command, newData = main.getFirstCommandFromData(inData)
        self.assertEqual(command, b'BUY: A1')
        self.assertEqual(newData, b'')
        inData = newData

    def test_getFirstCommandReturnsNoneWhenNoNewLinesExist(self):
        inData = b'QUERY: A1'
        command, newData = main.getFirstCommandFromData(inData)
        self.assertEqual(command, None)
        self.assertEqual(newData, inData)

        inData = b''
        command, newData = main.getFirstCommandFromData(inData)
        self.assertEqual(command, None)
        self.assertEqual(newData, inData)
    
class TestParseCommand(unittest.TestCase):
    def test_validCommandsReturnCorrectly(self):
        v,p = main.parseCommand(b'QUERY: A1')
        self.assertEqual(v, b'QUERY')
        self.assertEqual(p, b'A1')
        
        v,p = main.parseCommand(b'RESERVE: A1')
        self.assertEqual(v, b'RESERVE')
        self.assertEqual(p, b'A1')

        v,p = main.parseCommand(b'BUY: A1')
        self.assertEqual(v, b'BUY')
        self.assertEqual(p, b'A1')

    def test_invalidVerbsReturnNone(self):
        v,p = main.parseCommand(b'FAKE: A1')
        self.assertEqual(v, None)
        self.assertEqual(p, None)
        
        v,p = main.parseCommand(b'WRONG: A1')
        self.assertEqual(v, None)
        self.assertEqual(p, None)

    def test_invalidFormattedCommandsReturnNone(self):
        v,p = main.parseCommand(b'BUY: A1: B2')
        self.assertEqual(v, None)
        self.assertEqual(p, None)
        
        v,p = main.parseCommand(b'QUERY A1')
        self.assertEqual(v, None)
        self.assertEqual(p, None)

    def test_noSeatReturnsNone(self):
        v,p = main.parseCommand(b'BUY: ')
        self.assertEqual(v, None)
        self.assertEqual(p, None)
        
        v,p = main.parseCommand(b'QUERY: ')
        self.assertEqual(v, None)
        self.assertEqual(p, None)

class TestProcessingCommands(unittest.TestCase):

    def test_validSingleCommandsAreAppendedToDataOut(self):
        data = {'out': b'', 'in': b'QUERY: A1\n'}
        main.processAllCommands(data)
        self.assertEqual(data['out'], b'FREE\n')
        self.assertEqual(data['in'], b'')
        
        data = {'out': b'', 'in': b'RESERVE: A1\n'}
        main.processAllCommands(data)
        self.assertEqual(data['out'], b'OK\n')
        self.assertEqual(data['in'], b'')

    def test_chainedCommandProcessCorrectly(self):
        data = {'out': b'', 'in': b'QUERY: B1\nRESERVE: B1\nBUY: B1\nQUERY: B1\n'}
        main.processAllCommands(data)
        self.assertEqual(data['out'], b'FREE\nOK\nOK\nSOLD\n')
        self.assertEqual(data['in'], b'')

    def test_incompleteCommandsReturnFail(self):
        data = {'out': b'', 'in': b'QUERY: C1\nRESE: C1\nBUY: C1\nQUERY: C1\n'}
        main.processAllCommands(data)
        self.assertEqual(data['out'], b'FREE\nFAIL\nFAIL\nFREE\n')
        self.assertEqual(data['in'], b'')

    def test_trailingDataIsPreserved(self):
        data = {'out': b'', 'in': b'QUERY: D1\nRESERVE: D1\nBUY:'}
        main.processAllCommands(data)
        self.assertEqual(data['out'], b'FREE\nOK\n')
        self.assertEqual(data['in'], b'BUY:')

if __name__ == '__main__':
    unittest.main()
